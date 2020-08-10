#!/usr/bin/env python3
"""
List AWS Step Functions State Machines
"""

import argparse
import logging

from tabulate import tabulate
from typing import List

import boto3

from aws.stepfunctions import StepFunctions
from support.logging_configurator import LoggingConfigurator
from support.aws import Aws


logger = logging.getLogger(__name__)


def main():
    """
    main program
    """
    args = setup_args()
    check_debug_mode(args)
    print(args)

    client = Aws.create_client(args.profile, "stepfunctions")

    # get arm for state machine
    step_functions = StepFunctions(client)
    step_functions.list_state_machines()
    sm_by_name = step_functions.get_state_machines_by_name()

    # describe state machines
    # step_functions.list_state_machines_by_name(args.)
    for sm in args.state_machines:
        client.describe_state_machine(sm)

    state_machines = list_state_machines(client)
    logger.info("Found %d state machines" % len(state_machines))
    display_crawlers(state_machines)


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument(
        "-e", "--environment", help="environment", choices=["dev", "stg"], default=""
    )
    parser.add_argument(
        "-s",
        "--state_machines",
        help="state machines to execute",
        type=str,
        nargs="*",
        required=True,
    )
    parser.add_argument("-p", "--profile", choices=Aws.get_profiles(), default="default")
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


def check_debug_mode(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)


def list_state_machines(client: boto3.client) -> List[dict]:
    logger.debug("Listing step functions...")

    state_machines = []
    resp = client.list_state_machines()
    state_machines.extend(resp["stateMachines"])
    next_token = resp.get("NextToken", None)

    while next_token:
        resp = client.list_state_machines(nextToken=next_token)
        state_machines.extend(resp["stateMachines"])
        next_token = resp.get("NextToken", None)

    logger.debug("Completed listing state machines!")
    return state_machines


def display_crawlers(state_machines: List[dict]):
    headers = list(state_machines[0].keys())
    table = [list(state_machine.values()) for state_machine in state_machines]
    print(tabulate(table, headers, tablefmt="simple"))


if __name__ == "__main__":
    logger.debug("Script Started")
    LoggingConfigurator.configure_logging()
    main()
    logger.debug("Script Completed")
