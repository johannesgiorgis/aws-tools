#!/usr/bin/env python3
"""
List AWS Glue Crawlers
"""

import argparse
import logging

from typing import List

from support.logging_configurator import LoggingConfigurator
from support.aws import Aws
from aws.glue import Glue


logger = logging.getLogger(__name__)


def main():
    """
    main program
    """
    args = setup_args()
    check_debug_mode(args)

    glue = Glue(args.profile)
    crawlers = glue.get_list_of_crawlers(args.filter)
    logger.info("Found %d crawlers" % len(crawlers))
    display_crawlers(crawlers)


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument(
        "-f", "--filter", help="string filter to look for in crawler names", default=""
    )
    parser.add_argument("-p", "--profile", choices=Aws.get_profiles(), default="default")
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


def check_debug_mode(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)


def display_crawlers(crawlers: List[str]):
    for crawler in crawlers:
        print(crawler)


if __name__ == "__main__":
    logger.debug("Script Started")
    LoggingConfigurator.configure_logging()
    main()
    logger.debug("Script Completed")
