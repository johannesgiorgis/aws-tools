"""
AWS IAM Service
"""

import logging
import pprint

import boto3
import botocore

from aws.aws_service import AwsService
from support.aws import Aws

logger = logging.getLogger(__name__)


class IAM(AwsService):
    """
    IAM Client
    """

    def __init__(self, profile_name: str) -> None:
        self.profile_name = profile_name
        self.client_name = "iam"
        self.client = self._create_client()
        # api returns bytes - don't manipulate it
        self.credential_report: bytes = b""

    def _create_client(self, **kwargs) -> boto3.client:
        return Aws.create_client(self.profile_name, self.client_name)

    def generate_credential_report(self):
        response = self.client.generate_credential_report()
        logger.info(pprint.pformat(response))

    def get_credential_report(self):
        """
        Get generated credential report
        """
        try:
            resp = self.client.get_credential_report()
            self.credential_report = resp["Content"]
        except botocore.exceptions.ClientError as ex:
            logger.error(ex)
            if ex.response["Error"]["Code"] == "ReportNotPresent":
                logger.info("No credential report present. Please generate it first")
        except Exception as err:
            logger.error(err)
            raise
