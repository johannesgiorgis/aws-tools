#!/usr/bin/env python3
"""
Describe AWS SSM Crawlers
"""

import argparse
import logging

from support.logging_configurator import LoggingConfigurator
from support.aws import Aws
from support.common import Util
from aws.ssm import SSM

logger = logging.getLogger(__name__)


def main():
    """
    main program
    """
    args = setup_args()
    Util.check_debug_mode(args)

    ssm = SSM(args.profile)
    ssm.describe_parameters(values=args.values)
    ssm.display_parameters_names()


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument(
        "-v", "--values", help="Filter Values", nargs="*", type=str, default=[]
    )
    parser.add_argument(
        "-p", "--profile", choices=Aws.get_profiles(), default="default"
    )
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    logger.debug("Script Started")
    LoggingConfigurator.configure_logging()
    main()
    logger.debug("Script Completed")
