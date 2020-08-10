"""
AWS Glue
"""

import logging

from typing import List

import boto3

logger = logging.getLogger(__name__)


class Glue:
    def __init__(self, client: boto3.client):
        self.client = client
        self.crawlers = []

    def batch_get_crawlers(self, crawler_names: List[str]):
        logger.debug("Batch getting crawlers...")

        resp = self.client.batch_get_crawlers(CrawlerNames=crawler_names)
        self.crawlers.extend(resp["Crawlers"])

        logger.debug("Batch getting crawlers...")

    def get_batch_list_of_crawlers(self, crawler_names: List[str]) -> List[dict]:
        self.batch_get_crawlers()
        return self.crawlers
