import argparse
import logging
import signal
from argparse import Namespace
from datetime import datetime
from src.docker_manager import DockerManager
from src.cloudwatch_manager import CloudWatchManager

logger = logging.getLogger()


def parse_arguments() -> Namespace:
    parser = argparse.ArgumentParser(
        description="Управление Docker контейнером и логирование в AWS CloudWatch"
    )
    parser.add_argument("--docker-image", required=True, help="Название Docker образа для использования")
    parser.add_argument(
        "--bash-command",
        required=True,
        help="Команда Bash для выполнения в Docker контейнере",
    )
    parser.add_argument("--aws-cloudwatch-group", required=True, help="Название группы AWS CloudWatch")
    parser.add_argument(
        "--aws-cloudwatch-stream",
        required=True,
        help="Название потока в группе AWS CloudWatch",
    )
    parser.add_argument("--aws-access-key-id", required=True, help="AWS Access Key ID")
    parser.add_argument("--aws-secret-access-key", required=True, help="AWS Secret Access Key")
    parser.add_argument("--aws-region", required=True, help="Регион AWS")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    def signal_handler(signum, frame):
        logger.info("Signal received:", signum)
        docker_manager.stop_container()
        docker_manager.remove_container()
        logger.info("Graceful shutdown.")
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    docker_manager = DockerManager()
    cw_manager = CloudWatchManager(args.aws_access_key_id, args.aws_secret_access_key, args.aws_region)

    cw_manager.create_log_group(args.aws_cloudwatch_group)
    cw_manager.create_log_stream(args.aws_cloudwatch_group, args.aws_cloudwatch_stream)

    docker_manager.run_container(args.docker_image, args.bash_command)

    logs = docker_manager.get_logs()
    if logs:
        for log in logs:
            log_message = {
                "timestamp": int(datetime.utcnow().timestamp() * 1000),
                "message": log.decode("utf-8").strip(),
            }
            cw_manager.put_log_events(args.aws_cloudwatch_group, args.aws_cloudwatch_stream, [log_message])


if __name__ == "__main__":
    main()
