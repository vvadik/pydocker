import logging

from dotenv import load_dotenv
import os

load_dotenv()

LOGS_LEVEL: str = os.environ.get("LOGS_LEVEL", "INFO")
logging.basicConfig()
logging.root.setLevel(LOGS_LEVEL)

DOCKER_HOST: str = os.environ.get("DOCKER_HOST", "unix:///var/run/docker.sock")
