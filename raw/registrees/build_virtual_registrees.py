import attr
import datetime


import gotowebinar_api
import plot

api = gotowebinar_api.Api()

URL_PATH = "../../content/virtual_conf_stats/_index.md"
HEADER = """---
title: "Virtual Convention Registration Stats"
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
<h1 style="color: #000000;">Virtual Convention Registration Stats</h1>
"""
TABLE_HEADER = """
<h2>Registrees</h2>
<table id="registreeTable" class="tablesorter" border="1" padding=1>
<thead>
<tr>
<th>
Name
</th>
<th>
Club
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


with open(URL_PATH, "w") as fh:
    fh.write(HEADER)
    fh.write("<ul>")
    fh.write(f"<li><strong>Number of Registrees</strong>: {len(api.registrees)}</li>\n")
    fh.write("</ul>")

    fh.write(TABLE_HEADER)
    lines = [(f"{d['last_name']}, {d['first_name']}", d["club"]) for d in api.registrees.values()]
    lines.sort()
    for (name, club) in lines:
        fh.write(f"<tr><td>{name}</td><td>{club}</td></tr>\n")
    fh.write(TABLE_FOOTER)

    reg_dates = [datetime.datetime.fromisoformat(d["date"]).date() for d in api.registrees.values()]
    reg_dates.sort()
    plot.plot_registration_dates(reg_dates, "../../static/img/virtual_registrations_over_time.png")
    fh.write('<div style="text-align:center"><img src="/img/virtual_registrations_over_time.png"></div>')
    fh.write(FOOTER)
