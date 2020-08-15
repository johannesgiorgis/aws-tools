#!/usr/bin/env python3
"""
Describe AWS SSM Crawlers
"""

import argparse
import logging

from typing import List

import boto3

from support.logging_configurator import LoggingConfigurator
from support.aws import Aws
from aws.ssm import SSM

logger = logging.getLogger(__name__)


def main():
    """
    main program
    """
    args = setup_args()
    check_debug_mode(args)

    ssm = SSM(args.profile)

    # get parameters - filter by environment if provided
    # parameters = describe_parameters(ssm, values=args.values)
    parameters = ssm.get_describe_parameters(values=args.values)
    logger.info("Found %d parameters" % len(parameters))
    display_parameters(parameters)


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("-v", "--values", help="Filter Values", nargs="*", type=str, default=[])
    parser.add_argument("-p", "--profile", choices=Aws.get_profiles(), required=True)
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


def check_debug_mode(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)


def display_parameters(parameters: List[str]):
    for parameter in parameters:
        print(parameter["Name"])


if __name__ == "__main__":
    logger.debug("Script Started")
    LoggingConfigurator.configure_logging()
    main()
    logger.debug("Script Completed")
