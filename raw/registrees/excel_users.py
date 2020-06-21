""" Functions to retrieve registree data for the 2020
virtual MD410 Virtual Convention hosted on GoToWebinar
"""

import json
import os.path

import attr
import dateparser

from openpyxl import load_workbook

if 1:

    class ExcelSheet:
        def __init__(self):
            self.registrees = {}
            self.get_registrees()

        def get_registrees(self):
            wb = load_workbook(
                filename="/home/kimv/src/md410_2020_conv_website/raw/registrees/Service Knows No Boundaries Virtual Convention - Registration Report.xlsx"
            )
            skip = True
            for (n, row) in enumerate(wb["Sheet0"].values):
                if not skip:
                    self.registrees[n] = {
                        "first_name": row[0],
                        "last_name": row[1],
                        "date": dateparser.parse(row[3]).isoformat(),
                        "club": row[5],
                    }
                if row[0] == "First Name":
                    skip = False

    if __name__ == "__main__":
        sheet = ExcelSheet()
        print(sheet.registrees)
