"""
CSV Reader Class
"""

import csv

from typing import Dict, List


class CSVReader:
    @staticmethod
    def read_file(csv_file: str, skip_header: bool) -> List[str]:
        content = []
        with open(csv_file, "r") as file:
            reader = csv.reader(file)

            if skip_header:
                next(reader)

            for row in reader:
                content.append(row)
        return content

    @staticmethod
    def read_file_into_dict(csv_file: str) -> Dict[str, str]:
        content = []
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                content.append(row)
        return content