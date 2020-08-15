"""
AWS Glue
"""

import logging

from typing import List

import boto3

from aws.aws import Aws

logger = logging.getLogger(__name__)


class Glue(Aws):
    def __init__(self, session: boto3.session):
        self.session = session
        self.client = self._create_client(session)
        self.crawlers: List[str] = []

    def _create_client(self, session: boto3.session):
        return session.client("glue")

    def batch_get_crawlers(self, crawler_names: List[str]):
        logger.debug("Batch getting crawlers...")

        resp = self.client.batch_get_crawlers(CrawlerNames=crawler_names)
        self.crawlers.extend(resp["Crawlers"])

        logger.debug("Batch getting crawlers...")

    def get_batch_list_of_crawlers(self, crawler_names: List[str]) -> List[dict]:
        self.batch_get_crawlers(crawler_names)
        return self.crawlers

    def list_crawlers(self, filter: str = ""):
        logger.debug("Listing crawlers...")
        got_all_crawlers = False
        next_token = ""
        while not got_all_crawlers:
            resp = self.client.list_crawlers(NextToken=next_token)

            if filter:
                for crawler_name in resp["CrawlerNames"]:
                    if filter in crawler_name:
                        self.crawlers.append(crawler_name)
            else:
                self.crawlers.extend(resp["CrawlerNames"])

            next_token = resp.get("NextToken", None)

            if not next_token:
                got_all_crawlers = True
        logger.debug("Completed listing crawlers!")

    def get_list_of_crawlers(self, filter: str = "") -> List[str]:
        self.list_crawlers(filter)
        return self.crawlers
