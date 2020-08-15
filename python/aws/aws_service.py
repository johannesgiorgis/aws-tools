"""
AWS Service
"""

from abc import ABC, abstractmethod

import boto3


class AwsService(ABC):
    """
    Aws Service Base Class
    """

    @abstractmethod
    def __init__(self, profile_name: str, **kwargs):
        pass

    @abstractmethod
    def _create_client(self, **kwargs) -> boto3.client:
        pass
