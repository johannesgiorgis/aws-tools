#!/usr/bin/env python3

"""
AWS IAM Get Credentials Report
reference: https://sweetcode.io/auditing-iam-users-aws-sweetcode/
"""

import argparse
import pathlib
import sys
from aws.iam_credential_report import IAMCredentialReport
from aws.iam import IAM
import logging

from support.aws import Aws
from support.common import Util
from support.logging_configurator import LoggingConfigurator

logger = logging.getLogger(__name__)


def main():
    args = setup_args()
    Util.check_debug_mode(args)

    logger.debug(args)

    iam = IAM(args.profile)

    if args.run:
        logger.info("Generating Credential Report...")
        iam.generate_credential_report()

    if args.get:
        logger.info("Getting Generated Credential Report...")
        iam.get_credential_report()
        if iam.credential_report:
            credential_report = IAMCredentialReport(args.profile, iam.credential_report)
            credential_report.clean()

            # save to current directory
            p = pathlib.Path()
            credential_report.save_to_file(p.cwd())


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-r",
        "--run",
        help="Run Generate Credential Report Command",
        action="store_true",
    )
    group.add_argument(
        "-g", "--get", help="Get Generated Credential Report", action="store_true"
    )
    parser.add_argument(
        "-p", "--profile", choices=Aws.get_profiles(), default="default"
    )
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    LoggingConfigurator.configure_logging()
    logger.debug("Script Started")
    main()
    logger.debug("Script Completed")
