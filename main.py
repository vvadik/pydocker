import argparse
from src.docker_manager import docker_manager


def parse_arguments():
    """
    Парсит аргументы командной строки.
    """
    parser = argparse.ArgumentParser(
        description="Управление Docker контейнером и подготовка к логированию в AWS CloudWatch")
    parser.add_argument("--docker-image", required=True, help="Название Docker образа для использования")
    parser.add_argument("--bash-command", required=True, help="Команда Bash для выполнения в Docker контейнере")
    # Добавляем параметры, связанные с AWS, но без их реализации
    # parser.add_argument("--aws-cloudwatch-group", required=True, help="Название группы AWS CloudWatch")
    # parser.add_argument("--aws-cloudwatch-stream", required=True, help="Название потока в группе AWS CloudWatch")
    # parser.add_argument("--aws-access-key-id", required=True, help="AWS Access Key ID")
    # parser.add_argument("--aws-secret-access-key", required=True, help="AWS Secret Access Key")
    # parser.add_argument("--aws-region", required=True, help="Регион AWS")
    return parser.parse_args()


def main():
    args = parse_arguments()

    # Запускаем контейнер
    logs = docker_manager.run_container(args.docker_image, args.bash_command)

    # Печатаем логи для проверки (позднее логи будут отправляться в CloudWatch)
    if logs:
        for log in logs:
            print(log.decode('utf-8').strip())


if __name__ == "__main__":
    main()
