#!/usr/bin/env python3
"""
List AWS Glue Crawlers
"""

import argparse
import logging

from support.logging_configurator import LoggingConfigurator
from support.aws import Aws
from support.common import Util
from aws.glue import Glue


logger = logging.getLogger(__name__)


def main():
    """
    main program
    """
    args = setup_args()
    Util.check_debug_mode(args)

    glue = Glue(args.profile)
    glue.list_crawlers(args.filter)
    glue.display_crawler_names()


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument(
        "-f", "--filter", help="string filter to look for in crawler names", default=""
    )
    parser.add_argument("-p", "--profile", choices=Aws.get_profiles(), default="default")
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    LoggingConfigurator.configure_logging()
    logger.info("Script Started")
    main()
    logger.info("Script Completed")
