#!/usr/bin/env python3
"""
List AWS Glue Crawlers
"""

import argparse
import logging

from typing import List

import boto3


from support.logging_configurator import LoggingConfigurator


logger = logging.getLogger(__name__)


def main():
    """
    main program
    """
    args = setup_args()
    check_debug_mode(args)
    client = boto3.client("glue")

    # get crawlers - filter by environment if provided
    crawlers = list_crawlers(client, filter=args.environment)
    logger.info("Found %d crawlers" % len(crawlers))
    display_crawlers(crawlers)


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument(
        "-e", "--environment", help="environment", choices=["dev", "stg"], default=""
    )
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


def check_debug_mode(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)


def list_crawlers(client: boto3.client, filter: str = "") -> List[str]:
    logger.debug("Listing crawlers...")

    crawlers = []
    next_token = ""
    got_all_crawlers = False
    while not got_all_crawlers:
        resp = client.list_crawlers(NextToken=next_token)
        # logger.debug(pp.pformat(resp["CrawlerNames"]))

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
