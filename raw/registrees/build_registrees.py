from collections import Counter
from decimal import Decimal, getcontext
import os

import attr
from md410_2021_conv_common_online import db
import sqlalchemy as sa

import plot

getcontext().prec = 20
TWOPLACES = Decimal(10) ** -2

PUBLIC_URL_PATH = "../../content/registrees/_index.md"
FULL_URL_PATH = "../../content/full_stats/_index.md"
PUBLIC_HEADER = """---
title: Registration Stats
draft: false
---

"""
FULL_HEADER = """---
title: "Full Registration Stats"
date: 2019-07-14T16:19:07+02:00
draft: false
---

<html>
<head>
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script type="text/javascript" src="https://cdnjs.com/libraries/jquery.tablesorter"></script>
<script type="text/javascript">
    $(function() {
        $(".registreeTable").tablesorter();
    });
</script>
</head>
<body>
<h1 style="color: #000000;">Full Registration Stats</h1>
"""
PUBLIC_TABLE_HEADER = """<h2>Registrees</h2>

<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script type="text/javascript" src="https://cdnjs.com/libraries/jquery.tablesorter"></script>
<script type="text/javascript">
    $(function() {
        $(".registreeTable").tablesorter();
    });
</script>

<table id="registreeTable" class="tablesorter">
    <thead>
        <tr>
            <th>
                Name
            </th> 
            <th>
                Club
            </th>
            <th>
                District
            </th>
        </tr>
    </thead>
    <tbody>
"""
FULL_TABLE_HEADER = """<h2>Registrees</h2>
<table id="registreeTable" class="tablesorter" border="1" padding=1>
  <thead>
    <tr>
      <th>
        RegistrationNumber
      </th>
      <th>
        Name
      </th>
      <th>
        Club
      </th>
      <th>
        District
      </th>
      <th>
        Voter
      </th>
      <th>
        Attending District Convention
      </th>
      <th>
        Attending MD410 Convention
      </th>
    </tr>
  </thead>
<tbody>
"""
TABLE_FOOTER = """
</tbody>
</table>
"""
FOOTER = """
</body>
</html>
"""


class Stats(object):
    def __init__(self):
        self.dbh = db.DB()
        self.registrees = self.dbh.get_registrees()
        self.registrees.sort(key=lambda x: x.last_name)
        freq = Counter([r.club for r in self.registrees]).most_common()
        if freq:
            self.club_freq_num = freq[0][1]
        else:
            freq = []
            self.club_freq_num = 0
        names = []
        for (name, num) in freq:
            if num == self.club_freq_num:
                names.append(name)
            else:
                break
        self.club_freq_name = ", ".join(names)
        self.num_clubs = len(set([r.club for r in self.registrees]))
        self.district_nums = Counter(
            [r.district for r in self.registrees if r.attending_district_convention]
        )
        self.district_voter_nums = Counter(
            [
                r.district
                for r in self.registrees
                if (r.voter and r.attending_district_convention)
            ]
        )
        self.num_410_attendees = sum(
            [r.attending_md_convention for r in self.registrees]
        )
        self.num_410_voters = sum(
            [
                r.attending_md_convention
                for r in self.registrees
                if (r.voter and r.attending_md_convention)
            ]
        )

    def build_public_stats(self):
        with open(PUBLIC_URL_PATH, "w") as fh:
            fh.write(PUBLIC_HEADER)
            fh.write("<ul>")
            fh.write(
                f"<li><strong>Number of Registrees</strong>: {len(self.registrees)}</li>\n"
            )
            fh.write("\n")
            fh.write(f"<li><strong>Number of Clubs</strong>: {self.num_clubs}</li>\n")
            fh.write("\n")
            fh.write(
                f'<li><strong>Club{"s" if ", " in self.club_freq_name else ""} With Most Attendees</strong>: {self.club_freq_name} ({self.club_freq_num} registrees)</li>\n'
            )
            fh.write("</ul>")
            if self.registrees:
                fh.write(PUBLIC_TABLE_HEADER)
                for registree in self.registrees:
                    fh.write(
                        f"<tr><td>{registree.name}</td><td>{registree.club}</td><td>{registree.district}</td></tr>"
                    )
                fh.write(TABLE_FOOTER)

    def build_full_stats(self):
        with open(FULL_URL_PATH, "w") as fh:
            fh.write(FULL_HEADER)
            fh.write("<ul>")
            fh.write(
                f"<li><strong>Number of Registrees</strong>: {len(self.registrees)}</li>\n"
            )
            fh.write(f"<li><strong>Number of Clubs</strong>: {self.num_clubs}</li>\n")
            fh.write(
                f'<li><strong>Club{"s" if ", " in self.club_freq_name else ""} With Most Attendees</strong>: {self.club_freq_name} ({self.club_freq_num} registrees)</li>\n'
            )
            fh.write("\n")
            for (district, num) in self.district_nums.items():
                fh.write(
                    f"<li><strong>Number of District {district} Convention Attendees</strong>: {num}</li>\n"
                    f"<li><strong>Number of District {district} Convention Voters</strong>: {self.district_voter_nums[district]}</li>\n"
                )
            fh.write("\n")
            fh.write(
                f"<li><strong>Number of MD410 Convention Attendees</strong>: {self.num_410_attendees}</li>\n"
                f"<li><strong>Number of MD410 Convention Voters</strong>: {self.num_410_voters}</li>\n"
            )
            fh.write("\n")
            fh.write("</ul>\n")

            fh.write(FULL_TABLE_HEADER)
            for registree in self.registrees:
                fh.write(
                    f"""
<td>{registree.reg_num}</td>
<td>{registree.name}</td>
<td>{registree.club}</td>
<td>{registree.district}</td>
<td{' style="background-color: lightgreen"' if registree.voter else ''}>{"Yes" if registree.voter else "No"}</td>
<td{' style="background-color: lightgreen"' if registree.attending_district_convention else ''}>{"Yes" if registree.attending_district_convention else "No"}</td>
<td{' style="background-color: lightgreen"' if registree.attending_md_convention else ''}>{"Yes" if registree.attending_md_convention else "No"}</td>
</tr>\n
    """
                )
            fh.write(TABLE_FOOTER)

            reg_dates = [r.timestamp for r in self.registrees]
            reg_dates.sort()
            plot.plot_registration_dates(
                reg_dates, "../../static/img/registrations_over_time.png"
            )
            fh.write(
                '<div style="text-align:center"><img src="/img/registrations_over_time.png"></div>'
            )
            fh.write(FOOTER)


if __name__ == "__main__":
    stats = Stats()
    stats.build_public_stats()
    stats.build_full_stats()
