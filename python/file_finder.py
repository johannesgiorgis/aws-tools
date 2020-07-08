"""
File Finder
"""

import os


class FileFinder:
    @classmethod
    def resolve(cls, file_path: str):
        return os.path.join(cls.current_run_dir(), file_path)

    @classmethod
    def current_run_dir(cls):
        return os.path.dirname(os.path.abspath(__file__))
