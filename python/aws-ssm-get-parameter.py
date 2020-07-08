#!/usr/bin/env python3
"""
AWS SSM
"""

import argparse
import datetime
import json
import logging

import pprint as pp

import boto3

from support.logging_configurator import LoggingConfigurator

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# create handler
# c_handler = logging.StreamHandler()
# c_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
# LOG_FORMAT = "[%(asctime)s - %(levelname)-8s - %(module)s:%(name)s ] %(message)s"
# c_format = logging.Formatter(LOG_FORMAT)
# c_handler.setFormatter(c_format)

# Add handlers to the logger
# logger.addHandler(c_handler)


def main():
    args = setup_args()
    check_debug_mode(args)
    logger.debug(args)

    ssm = boto3.client("ssm")

    # get parameter
    parameter = get_parameter(ssm, args.token, args.with_decryption)

    print("=================================")
    if args.full_info:
        pp.pprint(json.dumps(parameter, default=myconverter))

    # extract value
    else:
        value = extract_parameter_value(parameter)
        print("Paramter Value:")
        print(value)


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("-t", "--token", help="token key", required=True)
    parser.add_argument("-w", "--with_decryption", help="decryption flag", action="store_true")
    parser.add_argument(
        "-f", "--full_info", help="get full JSON info of parameter", action="store_true"
    )
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


def check_debug_mode(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)


def get_parameter(ssm: boto3.client, token_key: str, decrypt: bool) -> dict:
    token_param = ssm.get_parameter(Name=token_key, WithDecryption=decrypt)
    return token_param["Parameter"]


def myconverter(date_obj) -> str:
    if isinstance(date_obj, datetime.datetime):
        return date_obj.__str__()


def extract_parameter_value(parameter: dict) -> str:
    return parameter["Value"].strip()


if __name__ == "__main__":
    logger.debug("Script Started")
    LoggingConfigurator.configure_logging()
    main()
    logger.debug("Script Completed")
