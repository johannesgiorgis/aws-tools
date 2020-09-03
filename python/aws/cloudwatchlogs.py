"""
AWS Cloudwatch Logs
"""

import logging
import pprint
from datetime import datetime
from typing import List

import boto3
from tabulate import tabulate

from aws.aws_service import AwsService
from support.aws import Aws

logger = logging.getLogger(__name__)


class LogStream:
    def __init__(
        self,
        logStreamName: str,
        creationTime: datetime,
        firstEventTimestamp: int,
        lastEventTimestamp: int,
        lastIngestionTime: int,
        uploadSequenceToken: str,
        arn: str,
        storedBytes: int,
    ):
        self.log_stream_name: str = logStreamName
        self.creation_time: datetime = creationTime
        self.first_event_timestamp: datetime = firstEventTimestamp
        self.last_event_timestamp: int = lastEventTimestamp
        self.last_ingestion_time: int = lastIngestionTime
        self.upload_sequence_token: str = uploadSequenceToken
        self.arn: str = arn
        self.stored_bytes: int = storedBytes


class CloudWatchLogs(AwsService):
    def __init__(self, profile_name: str):
        self.profile_name = profile_name
        self.client_name = "logs"
        self.client = self._create_client()
        self.log_streams: List[LogStream] = []
        self.log_events: dict = {}

    def _create_client(self, **kwargs) -> boto3.client:
        return Aws.create_client(self.profile_name, self.client_name)

    def describe_log_streams(
        self,
        log_group_name: str,
        order_by: str = "LastEventTime",
        descending: bool = False,
        limit: int = 1,
    ):
        resp = self.client.describe_log_streams(
            logGroupName=log_group_name,
            orderBy=order_by,
            descending=descending,
            limit=limit,
        )

        logger.info(resp["logStreams"])

        converted: list = self._convert_log_stream_dict_to_class(resp["logStreams"])

        self.log_streams.extend(converted)

    def _convert_log_stream_dict_to_class(
        self, log_streams: List[dict]
    ) -> List[LogStream]:
        """
        Converts dictionary representation of Log Stream to LogStream class
        """
        converted: List[LogStream] = []
        for log_stream in log_streams:
            converted.append(LogStream(**log_stream))
        return converted

    def get_log_stream_names(self) -> List[str]:
        log_stream_names: List[str] = []
        for log_stream in self.log_streams:
            log_stream_names.append(log_stream.log_stream_name)
        return log_stream_names

    def get_log_events(
        self, log_group_name: str, log_stream_name: str, start_from_head: bool = False
    ):
        resp = self.client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            startFromHead=start_from_head,
        )
        self.log_events[log_group_name] = resp["events"]

    def show_log_events_messages(self):
        for log_group_name, events in self.log_events.items():
            logger.info("log_group_name:%s" % log_group_name)
            messages = self._get_messages_from_log_event(events)
            print(messages)

    def _get_messages_from_log_event(self, events: list) -> str:
        messages = [event["message"] for event in events]
        return "\n".join(messages)
