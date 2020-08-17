#!/usr/bin/env python3
"""
AWS SSM
"""

import argparse
import logging

import pprint as pp

from aws.ssm import SSM
from support.logging_configurator import LoggingConfigurator
from support.aws import Aws
from support.common import Util

logger = logging.getLogger(__name__)


def main():
    args = setup_args()
    Util.check_debug_mode(args)

    ssm = SSM(args.profile)
    parameter = ssm.get_parameter(args.token, args.with_decryption)
    pp.pprint(parameter.display(show_full_info=args.full_info))


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("-t", "--token", help="token key", required=True)
    parser.add_argument("-w", "--with_decryption", help="decryption flag", action="store_true")
    parser.add_argument(
        "-f", "--full_info", help="get full JSON info of parameter", action="store_true"
    )
    parser.add_argument("-p", "--profile", choices=Aws.get_profiles(), default="default")
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    logger.debug("Script Started")
    LoggingConfigurator.configure_logging()
    main()
    logger.debug("Script Completed")
