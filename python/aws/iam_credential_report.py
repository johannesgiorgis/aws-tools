"""
AWS IAM Credential Report
"""

from datetime import datetime
from io import StringIO
import logging
import pytz

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class IAMCredentialReport:
    """
    IAM Credential Report
    """

    def __init__(self, profile_name: str, initial_credential_report: bytes):
        self.profile_name = profile_name
        # aws iam api returns bytes
        self.initial_credential_report: bytes = initial_credential_report
        # convert bytes to dataframe upon initialization
        self.df: pd.DataFrame = self._convert_bytes_to_dataframe()

    def clean(self):
        """
        Cleans up the credential report to my preference :)
        """
        self._preprocess_dataframe()
        self._add_age_columns()
        self._reorder_columns()

    def _convert_bytes_to_dataframe(self) -> pd.DataFrame:
        """
        Converts bytes input into DataFrame
        """
        # convert bytes into input for pd.read_csv
        input_data = StringIO(str(self.initial_credential_report, "utf-8"))
        date_columns = [
            "user_creation_time",
            "password_last_used",
            "password_last_changed",
            "password_next_rotation",
            "access_key_1_last_rotated",
            "access_key_1_last_used_date",
            "access_key_2_last_rotated",
            "access_key_2_last_used_date",
        ]
        return pd.read_csv(input_data, parse_dates=date_columns)

    def _preprocess_dataframe(self):
        """
        Preprocess Dataframe
        """
        # root user has 'not_supported' for columns password_last_changed, password_next_rotation
        # user was found with 'no_information' for column password_last_used
        # this results in the above parse_dates command to not properly convert those columns
        # so we need to set these values to NaN and manually the columns to datetime format
        self.df = self.df.replace("no_information", np.NaN).replace("not_supported", np.NaN)
        self.df[
            ["password_last_used", "password_last_changed", "password_next_rotation"]
        ] = self.df[
            ["password_last_used", "password_last_changed", "password_next_rotation"]
        ].apply(
            pd.to_datetime
        )

    def _get_age_in_days(self, row):
        """
        Helper function to calculate age in terms of days
        """
        # https://stackoverflow.com/a/62080404
        # https://stackoverflow.com/questions/16103238/pandas-timedelta-in-days
        now = datetime.now(tz=pytz.UTC)
        return (now - row).days

    def _add_age_columns(self):
        """
        Adds calculated age columns to simplify identifying age of attribute
        """
        # new columns: original columns
        columns_map = {
            "user_age": "user_creation_time",
            "password_use_age": "password_last_used",
            "password_change_age": "password_last_changed",
            "access_key_1_use_age": "access_key_1_last_used_date",
            "access_key_1_rotation_age": "access_key_1_last_used_date",
            "access_key_2_use_age": "access_key_2_last_used_date",
            "access_key_2_rotation_age": "access_key_2_last_used_date",
        }

        for key, value in columns_map.items():
            self.df[key] = self.df[value].apply(self._get_age_in_days)

    def _reorder_columns(self):
        """
        Re-order columns so 'age' columns are next to their original columns
        """
        new_columns_order = [
            "user",
            "arn",
            "user_creation_time",
            "user_age",
            "password_enabled",
            "password_last_used",
            "password_use_age",
            "password_last_changed",
            "password_change_age",
            "password_next_rotation",
            "mfa_active",
            "access_key_1_active",
            "access_key_1_last_rotated",
            "access_key_1_rotation_age",
            "access_key_1_last_used_date",
            "access_key_1_use_age",
            "access_key_1_last_used_region",
            "access_key_1_last_used_service",
            "access_key_2_active",
            "access_key_2_last_rotated",
            "access_key_2_rotation_age",
            "access_key_2_last_used_date",
            "access_key_2_use_age",
            "access_key_2_last_used_region",
            "access_key_2_last_used_service",
            "cert_1_active",
            "cert_1_last_rotated",
            "cert_2_active",
            "cert_2_last_rotated",
        ]
        self.df = self.df[new_columns_order]

    def save_to_file(
        self,
        directory: str,
        file_format: str = "csv",
        file_name: str = "iam-credential-report",
        timestamp_format: str = "%Y-%m-%d-%H%M%S",
    ):
        """
        Save credential report to file
        """
        timestamp = datetime.now().strftime(timestamp_format)
        if file_format == "csv":
            csv_file = f"{directory}/{timestamp}-{self.profile_name}-{file_name}.csv"
            logger.info("Saving to CSV file as '%s'" % csv_file)
            self.df.to_csv(csv_file)
