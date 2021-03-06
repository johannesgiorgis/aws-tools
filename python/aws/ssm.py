"""
AWS SSM Service
"""

from datetime import datetime
import logging

import boto3
from tabulate import tabulate
from botocore.exceptions import ClientError

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
        DataType: str = "",
    ):
        self.arn: str = ARN
        self.name: str = Name
        self.type: str = Type
        self.version: int = Version
        self.last_modified_date: datetime = LastModifiedDate
        self.data_type: str = DataType
        self.value: str = Value

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

    def values(self) -> List[str]:
        return [
            self.arn,
            self.name,
            self.type,
            self.version,
            self.last_modified_date,
            self.data_type,
        ]


class NewParameter:
    valid_type_values = ("String", "StringList", "SecureString")

    def __init__(
        self,
        Name: int,
        Value: str,
        Type: str,
        Description: str = "",
    ) -> None:
        self.Name: str = Name
        self.Value: str = Value
        self.Description: str = Description
        if Type not in NewParameter.valid_type_values:
            raise ValueError("Type is not a valid value")
        self.Type = Type


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
                "ParameterFilters": [
                    {"Key": "Name", "Option": "Contains", "Values": values}
                ],
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
        logger.debug("Parameter:%s" % token_param["Parameter"])
        return Parameter(**token_param["Parameter"])

    def get_parameters_by_path(
        self, path: str, recursive: bool, decrypt: bool, values: List[str] = []
    ):
        logger.debug("Getting parameters by path for %s..." % path)

        next_token = " "

        call_arguments = {
            "Path": path,
            "Recursive": recursive,
            "WithDecryption": decrypt,
            "NextToken": next_token,
        }

        if values:
            logger.info("Getting parameters that contain '%s'..." % values)
            additional_arguments = {
                "ParameterFilters": [
                    {"Key": "Name", "Option": "Contains", "Values": values}
                ],
            }
            call_arguments.update(additional_arguments)

        self.call_ssm_get_parameters_by_path(call_arguments)

    def call_ssm_get_parameters_by_path(self, arguments: dict):
        logger.debug("Calling get_parameters_by_path")

        got_all_parameters = False

        while not got_all_parameters:
            resp = self.client.get_parameters_by_path(**arguments)

            converted: list = self._convert_parameter_dict_to_class(resp["Parameters"])
            self.parameters.extend(converted)
            next_token = resp.get("NextToken", None)
            logger.debug("Next Token: %s" % next_token)

            if not next_token:
                got_all_parameters = True

            arguments["NextToken"] = next_token
        logger.info("Found %d parameters" % len(self.parameters))

    def _convert_parameter_dict_to_class(
        self, parameters: List[dict]
    ) -> List[Parameter]:
        """
        Converst dictionary representation of Parameter to Parameter class
        """
        converted: List[Parameter] = []
        for parameter in parameters:
            converted.append(Parameter(**parameter))
        return converted

    def display_parameters(self):
        print("Displaying parameters without values")
        if self.parameters:
            headers = list(vars(self.parameters[0]))
            table = [parameter.values() for parameter in self.parameters]
            print(tabulate(table, headers, tablefmt="simple"))

    def put_parameters(self, new_parameters: List[NewParameter]):
        """
        Add multiple new parameters to AWS SSM
        """
        # check if parameter already exists - skip if it does
        for new_parameter in new_parameters:

            try:
                token = self.get_parameter(new_parameter.Name, decrypt=False)
                logger.error("Parameter '%s' already exists!" % new_parameter.Name)

            # except self.client.ParameterNotFound:
            except ClientError as error:
                if error.response["Error"]["Code"] == "ParameterNotFound":
                    logger.warning(
                        "Parameter Not Found. Creating new parameter for '%s'..."
                        % new_parameter.Name
                    )
                    self.put_parameter(new_parameter)
                else:
                    raise error

    def put_parameter(self, new_parameter: NewParameter):
        """
        Add a parameter to AWS SSM
        """
        resp = self.client.put_parameter(
            Name=new_parameter.Name,
            Value=new_parameter.Value,
            Type=new_parameter.Type,
            Description=new_parameter.Description,
        )
        logger.info(resp)
