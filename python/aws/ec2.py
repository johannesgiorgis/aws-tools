"""
AWS EC2 Service
"""

import logging
from typing import List

import boto3

from aws.aws_service import AwsService
from support.aws import Aws

logger = logging.getLogger(__name__)


class SecurityGroup(AwsService):
    def __init__(self, profile_name: str):
        self.profile_name = profile_name
        self.client_name = "ec2"
        self.client = self._create_client()

    def _create_client(self) -> boto3.client:
        return Aws.create_client(self.profile_name, self.client_name)

    def describe_security_groups(self, group_names: List[str]):
        logger.debug("Describing security groups...")

        call_arguments = {"GroupNames": group_names}
        resp = self.client.describe_security_groups(**call_arguments)
        print(resp)
