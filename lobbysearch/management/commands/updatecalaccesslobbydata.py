"""
Download, clean and load lobbying tables from the latest CAL-ACCESS database.
"""
import os

from django.core.management import call_command
from calaccess_raw.management.commands import updatecalaccessrawdata

LOBBYING_FILE_NAMES = (
    "LPAY_CD.TSV",
    "CVR_LOBBY_DISCLOSURE_CD.TSV",
    "SMRY_CD.TSV",
)

class Command(updatecalaccessrawdata.Command):
    help = "Download, clean and load lobbying tables from the latest CAL-ACCESS database."

    def clean(self):
        """
        Clean up the raw data files from the state so they are ready to get loaded into the database.
        """
        if self.verbosity:
            self.header("Cleaning data files")

        tsv_list = [f for f in os.listdir(self.tsv_dir) if '.TSV' in f.upper()]

        # XXX Custom code here to filter to lobbying files only.
        tsv_list = [f for f in tsv_list if f in LOBBYING_FILE_NAMES]

        if self.resume:
            # get finished clean command logs of last update
            prev_cleaned = [
                x.file_name + '.TSV'
                for x in self.version.files.filter(clean_finish_datetime__isnull=False)
            ]
            self.log("{} files already cleaned.".format(len(prev_cleaned)))
            # remove these from tsv_list
            tsv_list = [x for x in tsv_list if x not in prev_cleaned]

        # Loop through all the files in the source directory
        for name in tsv_list:
            call_command(
                "cleancalaccessrawfile",
                name,
                verbosity=self.verbosity,
                keep_file=self.keep_files,
            )
