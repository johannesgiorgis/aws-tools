"""
AWS
"""

from configparser import ConfigParser
from pathlib import Path
from typing import List

import boto3


class Aws:
    aws_credentials = str(Path.home()) + "/" + ".aws/credentials"

    @staticmethod
    def get_profiles() -> List[str]:
        config = ConfigParser()
        config.read(Aws.aws_credentials)
        return config.sections()

    @staticmethod
    def create_client(profile_name: str, client_name: str) -> boto3.client:
        session = Aws.create_session(profile_name)
        return session.client(client_name)

    @staticmethod
    def create_session(profile_name: str) -> boto3.session:
        return boto3.Session(profile_name=profile_name)
