#!/usr/bin/env python3
"""
AWS SSM - Copy Parameters to another AWS account
"""

import argparse
import sys
from typing import List
from aws.ssm import NewParameter, Parameter, SSM
import logging
import json
import pprint as pp

from support.aws import Aws
from support.common import Util
from support.logging_configurator import LoggingConfigurator

logger = logging.getLogger(__name__)


def main():
    args = setup_args()
    Util.check_debug_mode(args)

    logger.info(args.path)

    source_ssm = SSM(args.source_profile)
    source_ssm.get_parameters_by_path(
        path=args.path, recursive=args.recursive, decrypt=args.with_decryption
    )
    # source_ssm.display_parameters_names()
    source_ssm.display_parameters()

    if not args.start_copy:
        logger.warning("Simply checking - No SSM Parameters will be copied!")
        sys.exit(0)

    # start copy
    new_parameters = create_new_parameters_list(source_ssm.parameters)
    target_ssm = SSM(args.target_profile)
    target_ssm.put_parameters(new_parameters)


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("-p", "--path", required=True)
    parser.add_argument(
        "-s", "--source_profile", choices=Aws.get_profiles(), required=True
    )
    parser.add_argument(
        "-t", "--target_profile", choices=Aws.get_profiles(), required=True
    )
    parser.add_argument(
        "-r", "--recursive", help="recursive flag", action="store_true", default=True
    )
    parser.add_argument(
        "-w",
        "--with_decryption",
        help="decryption flag",
        action="store_true",
        default=True,
    )
    parser.add_argument("-c", "--start_copy", action="store_true")
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


def create_new_parameters_list(parameters: List[Parameter]) -> List[NewParameter]:
    new_parameters = [
        NewParameter(
            parameter.name,
            parameter.value,
            parameter.type,
        )
        for parameter in parameters
    ]
    return new_parameters


if __name__ == "__main__":
    logger.debug("Script Started")
    LoggingConfigurator.configure_logging()
    main()
    logger.debug("Script Completed")
