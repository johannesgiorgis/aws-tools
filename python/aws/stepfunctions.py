"""
AWS Step Functions
"""

# import datetime
from datetime import datetime
import logging

import boto3

from typing import Dict, List

logger = logging.getLogger(__name__)


class StateMachine:
    def __init__(self, arn: str, name: str, sm_type: str, creation_date: datetime):
        self.arn: str = arn
        self.name: str = name
        self.type: str = sm_type
        self.creation_date: datetime = creation_date

    def values(self) -> List[str]:
        return [self.arn, self.name, self.type, self.creation_date]


class StepFunctions:
    def __init__(self, client: boto3.client):
        self.client = client
        self.state_machines: List[StateMachine] = []
        self.state_machines_by_name: Dict[str, StateMachine] = {}

    def get_state_machine_arn(self, state_machine_name: str) -> str:
        pass

    def filter_state_machines_by_name(self, names: List[str]) -> List[StateMachine]:
        desired_state_machines = []
        for sm in self.state_machines:
            if state_machine_name in sm.name:
                desired_state_machines.append(sm)
        return desired_state_machines

    def get_state_machines_by_name(self) -> Dict[str, StateMachine]:
        for sm in self.state_machines:
            self.state_machines_by_name[sm.name] = sm

    def list_state_machines(self):
        logger.debug("Listing state machines...")

        # Implemented in this duplicated manner as I was unable
        # to find a valid initial value for nextToken
        resp = self.client.list_state_machines()
        converted = self._convert_dict_to_state_machine(resp["stateMachines"])
        self.state_machines.extend(converted)
        next_token = resp.get("nextToken", None)

        while next_token:
            resp = self.client.list_state_machines(nextToken=next_token)
            converted = self._convert_dict_to_state_machine(resp["stateMachines"])
            self.state_machines.extend(converted)
            next_token = resp.get("nextToken", None)

        logger.debug("Completed listing state machines!")

    def _convert_dict_to_state_machine(self, state_machines: List[dict]) -> List[StateMachine]:
        """
        Converts dictionary representation of State Machine to StateMachine class
        """
        converted: List[StateMachine] = []
        for sm in state_machines:
            converted.append(
                StateMachine(
                    sm.get("stateMachineArn"),
                    sm.get("name"),
                    sm.get("type"),
                    sm.get("creationDate"),
                )
            )
        return converted

    def get_list_of_state_machines(self) -> List[StateMachine]:
        self.list_state_machines()
        logger.info("Found %d state machines" % len(self.state_machines))
        return self.state_machines
