"""
AWS Glue
"""

from datetime import datetime
import json
import logging

from typing import Dict, List

import boto3
from tabulate import tabulate

from aws.aws_service import AwsService
from support.aws import Aws

logger = logging.getLogger(__name__)


class Crawler:
    def __init__(
        self,
        Classifiers: list,
        Configuration: dict,
        CrawlElapsedTime: float,
        CreationTime: datetime,
        DatabaseName: str,
        LastCrawl: dict,
        LastUpdated: datetime,
        Name: str,
        Role: str,
        Schedule: dict,
        SchemaChangePolicy: dict,
        State: str,
        Targets: dict,
        Version: int,
    ):
        self.classifiers: list = Classifiers
        self.configuration: dict = Configuration
        self.crawl_elapsed_time: float = CrawlElapsedTime
        self.creation_time: datetime = CreationTime
        self.database_name: str = DatabaseName
        self.last_crawl: dict = LastCrawl
        self.last_updated: datetime = LastUpdated
        self.name: str = Name
        self.role: str = Role
        self.schedule: dict = Schedule
        self.schema_change_policy: dict = SchemaChangePolicy
        self.state: str = State
        self.targets: dict = Targets
        self.version: int = Version

    def __repr__(self):
        return json.dumps(self.values())

    def values(self) -> Dict[str, str]:
        return {"Name": self.name, "State": self.state}


class Glue(AwsService):
    def __init__(self, profile_name: str):
        self.profile_name = profile_name
        self.client_name = "glue"
        self.client = self._create_client()
        self.crawler_names: List[str] = []
        self.crawlers: List[Crawler] = []

    def _create_client(self) -> boto3.client:
        return Aws.create_client(self.profile_name, self.client_name)

    def batch_get_crawlers(self, crawler_names: List[str]):
        logger.debug("Batch getting crawlers...")

        resp = self.client.batch_get_crawlers(CrawlerNames=crawler_names)
        converted: List[Crawler] = self._convert_crawler_dict_to_class(resp["Crawlers"])
        self.crawlers.extend(converted)

        logger.debug("Completed batch getting crawlers!")

    def _convert_crawler_dict_to_class(self, crawlers: List[dict]) -> List[Crawler]:
        """
        Converts dictionary representation of Crawler to Crawler class
        """
        converted: List[Crawler] = []
        for crawler in crawlers:
            converted.append(Crawler(**crawler))
        return converted

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
                self.crawler_names.extend(resp["CrawlerNames"])

            next_token = resp.get("NextToken", None)

            if not next_token:
                got_all_crawlers = True

        logger.info("Found %d crawlers" % len(self.crawlers))
        logger.debug("Completed listing crawlers!")

    def display_crawler_names(self):
        for crawler_name in self.crawler_names:
            print(crawler_name)

    def display_crawlers(self):
        headers = list(self.crawlers[0].values().keys())
        table = [crawler.values().values() for crawler in self.crawlers]
        print(tabulate(table, headers, tablefmt="simple"))

    def get_crawler_names_by_state(self, state: str = "READY"):
        crawlers_in_state: List[Crawler] = []
        state = state.upper()
        logger.debug("Getting crawlers in state '%s'..." % state)
        for crawler in self.crawlers:
            if crawler.state == state:
                crawlers_in_state.append(crawler.name)
        logger.debug("Completed getting crawlers in state '%s'" % state)
        return crawlers_in_state

    def start_crawlers(self, crawlers: List[str]):
        logger.info("Starting %d crawlers..." % len(crawlers))

        for crawler_name in crawlers:
            self.start_crawler(crawler_name)
        logger.info("Completed %d starting crawlers" % len(crawlers))

    def start_crawler(self, crawler_name: str):
        logger.info("Starting crawler '%s'..." % crawler_name)
        resp = self.client.start_crawler(Name=crawler_name)
        logger.debug("Completed starting crawler: %s" % resp)
