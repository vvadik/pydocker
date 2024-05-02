import logging

import docker
from docker.errors import (
    ContainerError,
    ImageNotFound,
    APIError,
    NotFound,
    DockerException,
)
from docker.models.containers import Container

import config

logger = logging.getLogger(__name__)


class DockerManager:
    def __init__(self, **kwargs) -> None:
        self.client = docker.DockerClient(base_url=config.DOCKER_HOST, **kwargs)
        self._container: Container | None = None

    def run_container(self, image: str, command: str | list[str], **kwargs) -> None:
        """
        Starts Docker container.
        """
        try:
            self._container = self.client.containers.run(image, command, detach=True, **kwargs)
        except ImageNotFound:
            logger.error("The specified image was not found or there are insufficient permissions.")
        except ContainerError as e:
            logger.error(f"Error while executing command in container: {e}")
        except APIError as e:
            logger.error(f"API Docker Error: {e}")

    def get_logs(self):
        """
        Retrieves logs from the Docker container, if available.
        """
        if self._container:
            try:
                return self._container.logs(stream=True)
            except NotFound:
                logger.error("Error: The container has been removed or does not exist.")
            except DockerException as e:
                logger.error(f"Error retrieving logs: {e}")
        else:
            logger.error("No container is currently running.")

    def stop_container(self) -> None:
        """
        Stopping container.
        """
        try:
            if self._container:
                self._container.stop()
        except APIError as e:
            logger.error(f"API Docker Error while stopping container: {e}")

    def remove_container(self) -> None:
        """
        Deleting container.
        """
        try:
            if self._container:
                self._container.remove()
        except APIError as e:
            logger.error(f"API Docker Error while deleting container: {e}")
