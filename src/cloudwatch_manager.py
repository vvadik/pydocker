from typing import Any

import boto3
from botocore.exceptions import ClientError
import logging


logger = logging.getLogger(__name__)


class CloudWatchManager:
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str) -> None:
        self.client = boto3.client(
            "logs",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def create_log_group(self, log_group_name: str) -> None:
        """Create log group in CloudWatch."""
        try:
            self.client.create_log_group(logGroupName=log_group_name)
            logger.info(f"Log group '{log_group_name}' created.")
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceAlreadyExistsException":
                logger.debug(f"Log group '{log_group_name}' already exists.")
            else:
                raise

    def create_log_stream(self, log_group_name: str, log_stream_name: str) -> None:
        """Create log stream in log group."""
        try:
            self.client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
            logger.info(f"Log stream '{log_stream_name}' created in log group '{log_group_name}'.")
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceAlreadyExistsException":
                logger.debug(
                    f"Log stream '{log_stream_name}' already exists in log group '{log_group_name}'."
                )
            else:
                raise

    def put_log_events(
        self,
        log_group_name: str,
        log_stream_name: str,
        log_events: list[dict[str, Any]],
    ) -> None:
        """Send logs into CloudWatch."""
        try:
            response = self.client.describe_log_streams(
                logGroupName=log_group_name, logStreamNamePrefix=log_stream_name
            )

            if "logStreams" in response and len(response["logStreams"]) > 0:
                next_token = response["logStreams"][0].get("uploadSequenceToken")
                self.client.put_log_events(
                    logGroupName=log_group_name,
                    logStreamName=log_stream_name,
                    logEvents=log_events,
                    sequenceToken=next_token,
                )
                logger.info("Log events sent.")
            else:
                logger.info(
                    f"No log stream found with the name {log_stream_name} in log group {log_group_name}."
                )
        except ClientError as e:
            logger.error(f"Failed to send log events: {e}")
