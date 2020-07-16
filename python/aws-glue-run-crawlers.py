#!/usr/bin/env python3
"""
Run AWS Glue Crawlers
"""

import argparse
import logging
import pprint as pp
import sys

from typing import List

import boto3

from support.logging_configurator import LoggingConfigurator
from support.aws import Aws

logger = logging.getLogger(__name__)


def main():
    """
    main program
    """
    args = setup_args()
    check_debug_mode(args)
    # client = boto3.client("glue")
    client = Aws.create_client(args.profile, "glue")
    print(args)

    # read file content
    crawlers = get_crawlers(args.input_file)
    logger.info("Going to run %d crawlers" % len(crawlers))

    # get crawlers in ready state
    crawlers_to_start = get_crawlers_in_state(client, crawlers, state="READY")

    if not args.start_crawlers:
        logger.warning("Simply monitoring - No crawlers will be started!")
        sys.exit(0)

    # start crawlers
    if crawlers_to_start:
        start_crawlers(client, crawlers_to_start)
    else:
        logger.info("No crawlers to start!")


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument(
        "-i", "--input_file", help="input file containing crawlers to run", required=True,
    )
    parser.add_argument("-s", "--start_crawlers", action="store_true")
    parser.add_argument("-p", "--profile", choices=Aws.get_profiles(), required=True)
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


def check_debug_mode(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)


def get_crawlers(input_file: str) -> List[str]:
    logger.debug("Reading file %s" % input_file)
    with open(input_file, "r") as file_obj:
        crawlers = file_obj.read().splitlines()
    logger.debug("Completed reading file %s" % input_file)
    return crawlers


def get_crawlers_in_state(client: boto3.client, crawlers: List[str], state: str = "READY"):
    state = state.upper()
    logger.info("Getting crawlers in state '%s'..." % state)
    crawlers_in_state = []
    for crawler_name in crawlers:
        crawler_info = get_crawler_status(client, crawler_name)
        crawler_state = crawler_info["Crawler"]["State"]

        if crawler_state == state:
            crawlers_in_state.append(crawler_name)
    # pp.pprint(crawlers_in_state)
    logger.info("Completed getting crawlers in state '%s'" % state)
    return crawlers_in_state


def start_crawlers(client: boto3.client, crawlers: List[str]):
    logger.info("Starting %d crawlers..." % len(crawlers))

    for crawler_name in crawlers:
        start_crawler(client, crawler_name)
    logger.info("Completed %d starting crawlers" % len(crawlers))


def get_crawler_status(client: boto3.client, crawler_name: str):
    crawler_info = client.get_crawler(Name=crawler_name)
    state = crawler_info["Crawler"]["State"]
    logger.info("%s: %s" % (crawler_name, state))
    return crawler_info


def start_crawler(client: boto3.client, crawler_name: str):
    logger.info("Starting crawler '%s'..." % crawler_name)
    resp = client.start_crawler(Name=crawler_name)
    logger.debug("Completed starting crawler: %s" % resp)


def list_crawlers(client: boto3.client, filter: str = "") -> List[str]:
    logger.debug("Listing crawlers...")

    crawlers = []
    next_token = ""
    got_all_crawlers = False
    while not got_all_crawlers:
        resp = client.list_crawlers(NextToken=next_token)

        if filter:
            for crawler_name in resp["CrawlerNames"]:
                if filter in crawler_name:
                    crawlers.append(crawler_name)
        else:
            crawlers.extend(resp["CrawlerNames"])

        next_token = resp.get("NextToken", None)

        if not next_token:
            got_all_crawlers = True
    logger.debug("Completed listing crawlers!")
    return crawlers


def display_crawlers(crawlers: List[str]):
    for crawler in crawlers:
        print(crawler)


if __name__ == "__main__":
    logger.debug("Script Started")
    LoggingConfigurator.configure_logging()
    main()
    logger.debug("Script Completed")
