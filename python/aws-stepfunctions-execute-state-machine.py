#!/usr/bin/env python3
"""
List AWS Step Functions State Machines
---

Currently no way to batch get step functions so need to
get full list of step functions that exist, then filter out
based on list provided by user to get the list of step functions
to execute.
This is also because start_execution() only takes stateMachineArn
"""

import argparse
import logging

from tabulate import tabulate
from typing import List

import boto3

from aws.stepfunctions import StepFunctions
from support.logging_configurator import LoggingConfigurator
from support.aws import Aws
from support.common import Util


logger = logging.getLogger(__name__)


def main():
    """
    main program
    """
    args = setup_args()
    Util.check_debug_mode(args)

    # get arm for state machine
    step_functions = StepFunctions(args.profile)
    step_functions.list_state_machines()
    step_functions.organize_state_machines_by_name()
    state_machines_arns = step_functions.get_state_machines_arns(
        args.state_machines_names
    )

    print(state_machines_arns)
    logger.info("Starting state machines %s" % state_machines_arns)

    step_functions.execute_state_machines(state_machines_arns)


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument(
        "-e", "--environment", help="environment", choices=["dev", "stg"], default=""
    )
    parser.add_argument(
        "-s",
        "--state_machines_names",
        help="state machines to execute",
        type=str,
        nargs="*",
        required=True,
    )
    parser.add_argument(
        "-p", "--profile", choices=Aws.get_profiles(), default="default"
    )
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


# def list_state_machines(client: boto3.client) -> List[dict]:
#     logger.debug("Listing step functions...")

#     state_machines = []
#     resp = client.list_state_machines()
#     state_machines.extend(resp["stateMachines"])
#     next_token = resp.get("NextToken", None)

#     while next_token:
#         resp = client.list_state_machines(nextToken=next_token)
#         state_machines.extend(resp["stateMachines"])
#         next_token = resp.get("NextToken", None)

#     logger.debug("Completed listing state machines!")
#     return state_machines


def display_crawlers(state_machines: List[dict]):
    headers = list(state_machines[0].keys())
    table = [list(state_machine.values()) for state_machine in state_machines]
    print(tabulate(table, headers, tablefmt="simple"))


if __name__ == "__main__":
    LoggingConfigurator.configure_logging()
    logger.debug("Script Started")
    main()
    logger.debug("Script Completed")
