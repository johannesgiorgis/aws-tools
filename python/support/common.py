"""
Common Utilities
"""

import argparse
import logging

logger = logging.getLogger(__name__)


class Util:
    @classmethod
    def check_debug_mode(cls, args: argparse):
        if args.debug:
            logger.setLevel(logging.DEBUG)

            for handler in logger.handlers:
                handler.setLevel(logging.DEBUG)
