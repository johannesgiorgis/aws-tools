#!/usr/bin/env python3
"""
Get log events from AWS Cloudwatch Logs
"""

import argparse
import logging

from support.logging_configurator import LoggingConfigurator
from support.aws import Aws
from support.common import Util

# from aws.glue import Glue
from aws.cloudwatchlogs import CloudWatchLogs


logger = logging.getLogger(__name__)


def main():
    """
    main program
    """
    args = setup_args()
    Util.check_debug_mode(args)

    cloudwatchlogs = CloudWatchLogs(args.profile)
    cloudwatchlogs.describe_log_streams(args.log_group_name, descending=True, limit=1)
    log_stream_names = cloudwatchlogs.get_log_stream_names()

    for log_stream_name in log_stream_names:
        logger.info("Log_stream_name: %s" % log_stream_name)
        cloudwatchlogs.get_log_events(args.log_group_name, log_stream_name)
        cloudwatchlogs.show_log_events_messages()


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument(
        "-p", "--profile", choices=Aws.get_profiles(), default="default"
    )
    parser.add_argument(
        "-n",
        "--log_group_name",
        help="log group name",
        required=True,
    )
    parser.add_argument(
        "-e", "--environment", help="environment", choices=["dev", "stg"], default=""
    )
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    LoggingConfigurator.configure_logging()
    logger.debug("Script Started")
    main()
    logger.debug("Script Completed")
