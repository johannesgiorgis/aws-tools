#!/usr/bin/env python3
"""
AWS SSM
"""

import argparse
import logging
import pprint as pp
from typing import List

from aws.ssm import SSM, NewParameter
from support.aws import Aws
from support.common import Util
from support.csv_reader import CSVReader
from support.logging_configurator import LoggingConfigurator

logger = logging.getLogger(__name__)


def main():
    args = setup_args()
    Util.check_debug_mode(args)

    new_parameters = create_new_parameters_list(args.input_file)

    ssm = SSM(args.profile)
    ssm.put_parameters(new_parameters)


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("-i", "--input_file", required=True)
    parser.add_argument("-p", "--profile", choices=Aws.get_profiles(), default="default")
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


def create_new_parameters_list(csv_file: str) -> List[NewParameter]:
    file_contents = CSVReader.read_file_into_dict(csv_file)
    new_parameters = [NewParameter(**content) for content in file_contents]
    return new_parameters


if __name__ == "__main__":
    logger.debug("Script Started")
    LoggingConfigurator.configure_logging()
    main()
    logger.debug("Script Completed")
