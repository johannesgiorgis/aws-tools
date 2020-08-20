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

    logger.info("Going to run %d crawlers" % len(args.crawler_names))
    glue = Glue(args.profile)
    glue.batch_get_crawlers(args.crawler_names)
    glue.display_crawlers()
    crawlers_to_start = glue.get_crawler_names_by_state(state="READY")

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
    parser.add_argument(
        "-c",
        "--crawler_names",
        nargs="+",
        type=str,
        help="crawler names",
        required=True,
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
