from dotenv import load_dotenv
import os

# load_dotenv()

DOCKER_HOST: str = os.environ.get("DOCKER_HOST", "unix:///var/run/docker.sock")
