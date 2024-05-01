import logging

import docker
from docker.errors import ContainerError, ImageNotFound, APIError, DockerException

import config

# todo: add black isort mypy

logger = logging.getLogger(__name__)


class DockerManager:
    def __init__(self, **kwargs):
        self.client = docker.DockerClient(base_url=config.DOCKER_HOST)

    def run_container(self, image: str, command: str | list[str]) -> None:
        """
        Запускает Docker контейнер с указанным образом и командой.
        Возвращает логи выполнения команды в контейнере.
        """
        try:
            container = self.client.containers.run(image, command, detach=True)
            logs = container.logs(stream=True)
            return logs
        except ImageNotFound:
            print("Ошибка: Указанный образ не найден.")
        except ContainerError as e:
            print(f"Ошибка выполнения команды в контейнере: {e}")
        except APIError as e:
            print(f"Ошибка API Docker: {e}")

    def stop_container(self, container_id):
        """
        Останавливает контейнер по указанному ID.
        """
        try:
            container = self.client.containers.get(container_id)
            container.stop()
        except APIError as e:
            print(f"Ошибка API Docker при остановке контейнера: {e}")

    def remove_container(self, container_id):
        """
        Удаляет контейнер по указанному ID.
        """
        try:
            container = self.client.containers.get(container_id)
            container.remove()
        except APIError as e:
            print(f"Ошибка API Docker при удалении контейнера: {e}")


docker_manager = DockerManager()
# todo проверить что енвы успевают подгрузиться
# todo что если нет имаджа

