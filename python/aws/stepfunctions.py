"""
AWS Step Functions
"""

from datetime import datetime
import logging

from typing import Dict, List

import boto3
from tabulate import tabulate

from aws.aws_service import AwsService
from support.aws import Aws

logger = logging.getLogger(__name__)


class StateMachine:
    def __init__(self, arn: str, name: str, sm_type: str, creation_date: datetime):
        self.arn: str = arn
        self.name: str = name
        self.type: str = sm_type
        self.creation_date: datetime = creation_date

    def values(self) -> List[str]:
        return [self.arn, self.name, self.type, self.creation_date]


class StepFunctions(AwsService):
    """
    Step Functions Client
    """

    def __init__(self, profile_name: str):
        self.profile_name = profile_name
        self.client_name = "stepfunctions"
        self.client = self._create_client()
        self.state_machines: List[StateMachine] = []
        self.state_machines_by_name: Dict[str, StateMachine] = {}

    def _create_client(self) -> boto3.client:
        return Aws.create_client(self.profile_name, self.client_name)

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
            converted: List[StateMachine] = self._convert_dict_to_state_machine(
                resp["stateMachines"]
            )
            self.state_machines.extend(converted)
            next_token = resp.get("nextToken", None)

        logger.info("Found %d state machines" % len(self.state_machines))
        logger.debug("Completed listing state machines!")

    def _convert_dict_to_state_machine(
        self, state_machines: List[dict]
    ) -> List[StateMachine]:
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

    def display_state_machines(self):
        if self.state_machines:
            headers = list(vars(self.state_machines[0]).keys())
            print("heders:", headers)
            table = [state_machine.values() for state_machine in self.state_machines]
            print("tables:", table[0])
            print(tabulate(table, headers, tablefmt="simple"))

    def organize_state_machines_by_name(self):
        for sm in self.state_machines:
            self.state_machines_by_name[sm.name] = sm

    def get_state_machines_arns(self, state_machine_names: List[str]) -> List[str]:
        state_machines_arns = []
        for sm_name in state_machine_names:
            state_machines_arns.append(self.state_machines_by_name[sm_name].arn)
        return state_machines_arns

    def execute_state_machines(self, state_machine_arns: List[str]):
        """
        execute state machines
        """
        logger.info(
            "Starting execution for %d state machines" % len(state_machine_arns)
        )
        for sm_arn in state_machine_arns:
            resp = self.client.start_execution(stateMachineArn=sm_arn)
            logger.info("resp:%s", resp)
