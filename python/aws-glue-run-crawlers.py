#!/usr/bin/env python3
"""
Run AWS Glue Crawlers
"""

import argparse
import logging
import sys


from aws.glue import Glue
from support.logging_configurator import LoggingConfigurator
from support.aws import Aws
from support.common import Util

logger = logging.getLogger(__name__)


def main():
    """
    main program
    """
    args = setup_args()
    Util.check_debug_mode(args)

    glue = Glue(args.profile)

    if args.crawler_names:
        logger.info("Going to run %d crawlers" % len(args.crawler_names))
        glue.batch_get_crawlers(args.crawler_names)

    if args.environment:
        logger.info("Going to run crawlers for %s environment" % args.environment)
        glue.list_crawlers(args.environment)
        glue.batch_get_crawlers(glue.crawler_names)

    glue.display_crawlers()
    crawlers_to_start = glue.get_crawler_names_by_state(state="READY")
    logger.info("Found %d crawlers to start" % len(crawlers_to_start))

    if not args.start_crawlers:
        logger.warning("Simply monitoring - No crawlers will be started!")
        sys.exit(0)

    # start crawlers
    if crawlers_to_start:
        glue.start_crawlers(crawlers_to_start)
    else:
        logger.info("No crawlers to start!")


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-c",
        "--crawler_names",
        nargs="+",
        type=str,
        help="crawler names",
    )
    group.add_argument(
        "-e",
        "--environment",
        help="runs all crawlers for specified environment or all environments",
        choices=["dev", "stg", "prod"],
    )
    parser.add_argument("-s", "--start_crawlers", action="store_true")
    parser.add_argument("-p", "--profile", choices=Aws.get_profiles(), required=True)
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    logger.debug("Script Started")
    LoggingConfigurator.configure_logging()
    main()
    logger.debug("Script Completed")
