#!/usr/bin/env python3
"""
Describe AWS SSM Crawlers
"""

import argparse
import logging
import pprint as pp

from typing import List

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
    """
    main program
    """
    args = setup_args()
    check_debug_mode(args)
    logger.debug(args)
    ssm = boto3.client("ssm")

    # get parameters - filter by environment if provided
    parameters = describe_parameters(ssm, values=args.values)
    logger.info("Found %d parameters" % len(parameters))
    display_parameters(parameters)


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("-v", "--values", help="Filter Values", nargs="*", type=str, default=[])
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


def check_debug_mode(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)


def describe_parameters(ssm: boto3.client, values: List[str] = []) -> List[str]:
    logger.debug("Describing parameters with values %s..." % values)

    parameters = []
    next_token = " "
    got_all_parameters = False

    if values:

        while not got_all_parameters:

            resp = ssm.describe_parameters(
                ParameterFilters=[{"Key": "Name", "Option": "Contains", "Values": values}],
                NextToken=next_token,
            )
            # logger.debug(pp.pformat(resp))
            parameters.extend(resp["Parameters"])
            next_token = resp.get("NextToken", None)
            logger.debug("Next Token: %s" % next_token)

            if not next_token:
                got_all_parameters = True

    # Get all parameters
    else:

        logger.info("Getting all parameters...")
        while not got_all_parameters:

            resp = ssm.describe_parameters(NextToken=next_token)
            # logger.debug(pp.pformat(resp))
            parameters.extend(resp["Parameters"])
            next_token = resp.get("NextToken", None)
            logger.debug("Next Token: %s" % next_token)

            if not next_token:
                got_all_parameters = True

    logger.debug("Completed describing parameters!")
    return parameters

    # parameters = []
    # next_token = ""
    # got_all_parameters = False
    # while not got_all_parameters:
    #     resp = ssm.describe_parameters(
    #         ParameterFilters=[{"Key": "Name", "Option": "Contains", "Values": values},],
    #     )
    #     logger.debug(pp.pformat(resp))

    #     if filter:
    #         for crawler_name in resp["CrawlerNames"]:
    #             if filter in crawler_name:
    #                 parameters.append(crawler_name)
    #     else:
    #         parameters.extend(resp["CrawlerNames"])

    #     next_token = resp.get("NextToken", None)

    #     if not next_token:
    #         got_all_parameters = True
    # logger.debug("Completed listing parameters!")
    # return parameters


def display_parameters(parameters: List[str]):
    for parameter in parameters:
        print(parameter["Name"])


if __name__ == "__main__":
    logger.debug("Script Started")
    LoggingConfigurator.configure_logging()
    main()
    logger.debug("Script Completed")
