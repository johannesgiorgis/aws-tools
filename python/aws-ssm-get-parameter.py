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


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
LOG_FORMAT = "[%(asctime)s - %(levelname)-8s - %(module)s:%(name)s ] %(message)s"
c_format = logging.Formatter(LOG_FORMAT)
c_handler.setFormatter(c_format)

# Add handlers to the logger
logger.addHandler(c_handler)


def main():
    args = setup_args()
    check_debug_mode(args)
    logger.debug(args)

    ssm = boto3.client("ssm")

    # get parameters
    parameters = get_parameters(ssm, args.token, args.with_decryption)
    pp.pprint(json.dumps(parameters, default=myconverter))


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("-t", "--token", help="token key", required=True)
    parser.add_argument("-w", "--with_decryption", help="decryption flag", action="store_true")
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


def check_debug_mode(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)


def get_parameters(ssm: boto3.client, token_key: str, decrypt: bool):
    token_param = ssm.get_parameter(Name=token_key, WithDecryption=decrypt)
    return token_param["Parameter"]


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


if __name__ == "__main__":
    main()
