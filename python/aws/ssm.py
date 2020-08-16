"""
AWS SSM Service
"""

from datetime import datetime
import logging

import boto3

from typing import List

from aws.aws_service import AwsService
from support.aws import Aws

logger = logging.getLogger(__name__)


class Parameter:
    def __init__(
        self,
        ARN: str,
        Name: str,
        Type: str,
        Value: str,
        Version: int,
        LastModifiedDate: datetime,
        DataType: str,
    ):
        self.arn: str = ARN
        self.name: str = Name
        self.type: str = Type
        self.value: str = Value
        self.version: int = Version
        self.last_modified_date: datetime = LastModifiedDate
        self.data_type: str = DataType

    def display(self, show_full_info: bool):

        if show_full_info:
            return {
                "Name": self.name,
                "Type": self.type,
                "Value": self.value,
                "Version": self.version,
                "LastModifiedDate": self.last_modified_date.__str__(),
                "ARN": self.arn,
                "DataType": self.data_type,
            }
        else:
            return self.value


class SSM(AwsService):
    """
    SSM Client
    """

    def __init__(self, profile_name: str):
        self.profile_name = profile_name
        self.client_name = "ssm"
        self.client = self._create_client()
        self.parameters = []

    def _create_client(self) -> boto3.client:
        return Aws.create_client(self.profile_name, self.client_name)

    def describe_parameters(self, values: List[str] = []):
        logger.debug("Describing parameters with values %s..." % values)

        next_token = " "

        if values:

            logger.info("Getting parameters that contain '%s'..." % values)
            call_arguments = {
                "ParameterFilters": [{"Key": "Name", "Option": "Contains", "Values": values}],
                "NextToken": next_token,
            }

        else:

            logger.info("Getting all parameters...")
            call_arguments = {
                "NextToken": next_token,
            }

        self.call_ssm_describe_parameters(call_arguments)

        logger.debug("Completed describing parameters!")

    def call_ssm_describe_parameters(self, arguments=dict):
        logger.debug("Calling describe parameters")

        got_all_parameters = False

        while not got_all_parameters:
            resp = self.client.describe_parameters(**arguments)
            # logger.debug(pp.pformat(resp))
            self.parameters.extend(resp["Parameters"])
            next_token = resp.get("NextToken", None)
            logger.debug("Next Token: %s" % next_token)

            if not next_token:
                got_all_parameters = True

            arguments["NextToken"] = next_token
        logger.info("Found %d parameters" % len(self.parameters))

    def get_describe_parameters(self, values: List[str] = []) -> List[str]:
        self.describe_parameters(values)
        return self.parameters

    def display_parameters_names(self):
        for parameter in self.parameters:
            print(parameter["Name"])

    def get_parameter(self, token_key: str, decrypt: bool) -> dict:
        token_param = self.client.get_parameter(Name=token_key, WithDecryption=decrypt)
        return Parameter(**token_param["Parameter"])
