"""
AWS Service
"""

from abc import ABC, abstractmethod

import boto3


class Aws(ABC):
    """
    Aws Base Class
    """

    @abstractmethod
    def __init__(self, kwargs):
        pass

    @abstractmethod
    def _create_client(self, session: boto3.session):
        pass
