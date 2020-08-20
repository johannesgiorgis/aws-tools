#!/usr/bin/env python3
"""
List AWS Step Functions State Machines
"""

import argparse
import logging

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
    step_functions = StepFunctions(profile_name=args.profile)
    step_functions.list_state_machines()
    step_functions.display_state_machines()


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument(
        "-p", "--profile", choices=Aws.get_profiles(), default="default"
    )
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    LoggingConfigurator.configure_logging()
    logger.info("Script Started")
    main()
    logger.info("Script Completed")
