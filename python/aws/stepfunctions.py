"""
AWS Step Functions
"""

import logging
import boto3

from typing import List

logger = logging.getLogger(__name__)


class StepFunctions:
    def __init__(self, client: boto3.client):
        self.client = client
        self.state_machines = []

    def get_state_machine_arn(state_machine_name: str) -> str:
        pass

    def list_state_machines(self):
        logger.debug("Listing state machines...")

        # Implemented in this duplicated manner as I was unable
        # to find a valid initial value for nextToken
        resp = self.client.list_state_machines()
        self.state_machines.extend(resp["stateMachines"])
        next_token = resp.get("nextToken", None)

        while next_token:
            resp = self.client.list_state_machines(nextToken=next_token)
            self.state_machines.extend(resp["stateMachines"])
            next_token = resp.get("nextToken", None)

        logger.debug("Completed listing state machines!")

    def get_list_of_state_machines(self) -> List[dict]:
        self.list_state_machines()
        return self.state_machines
