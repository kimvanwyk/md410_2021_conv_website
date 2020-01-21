from collections import Counter
from decimal import Decimal, getcontext
import os

import attr
import sqlalchemy as sa

import plot

getcontext().prec = 20
TWOPLACES = Decimal(10) ** -2

PUBLIC_URL_PATH = '../../content/registrees/_index.md'
FULL_URL_PATH = '../../content/full_stats/_index.md'
PUBLIC_HEADER = '''---
title: Registration Stats
draft: false
---

'''
FULL_HEADER = '''<html>
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
'''
PUBLIC_TABLE_HEADER = '''<h2>Registrees</h2>

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
        </tr>
    </thead>
    <tbody>
'''
FULL_TABLE_HEADER = '''<h2>Registrees</h2>
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
NameBadge
</th>
<th>
InitiallyOwed
</th>
<th>
Paid
</th>
<th>
StillOwed
</th>
</tr>
</thead>
<tbody>
'''
TABLE_FOOTER = '''
</tbody>
</table>
'''
FOOTER = '''
</body>
</html>
'''

TABLES = {
    "registree": ("md410_2020_conv", "registree"),
    "club": ("md410_2020_conv", "club"),
    "partner_program": ("md410_2020_conv", "partner_program"),
    "full_reg": ("md410_2020_conv", "full_reg"),
    "partial_reg": ("md410_2020_conv", "partial_reg"),
    "pins": ("md410_2020_conv", "pins"),
    "payment": ("md410_2020_conv", "payment")
}

COSTS = {
    "full": 1285,
    "banquet": 500,
    "convention": 400,
    "theme": 450,
    "pins": 55
}

@attr.s
class Registree(object):
    last_name = attr.ib()
    reg_num = attr.ib()
    timestamp = attr.ib()
    first_names = attr.ib()
    club = attr.ib()
    cell = attr.ib()
    email = attr.ib()
    dietary = attr.ib()
    disability = attr.ib()
    name_badge = attr.ib()
    is_lion = attr.ib()
    first_mdc = attr.ib()
    mjf_lunch = attr.ib()
    pdg_breakfast = attr.ib()
    sharks_board = attr.ib()
    golf = attr.ib()
    sight_seeing = attr.ib()
    service_project = attr.ib()
    full = attr.ib()
    banquet = attr.ib()
    convention = attr.ib()
    theme = attr.ib()
    pins = attr.ib()
    partner_program = attr.ib()
    paid = attr.ib()
    initial_owed = attr.ib(default=0)
    still_owed = attr.ib(default=0)
    title = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.name = f"{self.first_names.strip()} {self.last_name.strip()}"
        self.initial_owed = Decimal(0).quantize(TWOPLACES)
        for k in COSTS:
            self.initial_owed += Decimal(getattr(self, k) * COSTS[k]).quantize(TWOPLACES)
        self.still_owed = self.initial_owed - self.paid

@attr.s
class DB(object):
    """ Handle postgres database interaction
    """

    host = attr.ib(default="localhost")
    port = attr.ib(default=5432)
    user = attr.ib(default="postgres")
    dbname = attr.ib(default="postgres")
    debug = attr.ib(default=False)

    def __attrs_post_init__(self):
        self.engine = sa.create_engine(
            f"postgresql+psycopg2://{self.user}:{os.getenv('PGPASSWORD')}@{self.host}:{self.port}/{self.dbname}"
        )
        md = sa.MetaData()
        md.bind = self.engine
        self.engine.autocommit = True
        self.tables = {}
        for (k, (schema, name)) in TABLES.items():
            self.tables[k] = sa.Table(name, md, autoload=True, schema=schema)

    def get_registrees(self):
        tr = self.tables["registree"]
        tc = self.tables["club"]
        tpp = self.tables["partner_program"]
        tfr = self.tables["full_reg"]
        tpr = self.tables["partial_reg"]
        tpy = self.tables["payment"]
        tp = self.tables["pins"]

        res = self.engine.execute(tr.select()).fetchall()
        registrees = []

        for r in res:
            registree = {}
            for d in dict(r):
                registree[d] = r[d]
            registree['club'] = None
            registree['partner_program'] = None
            if r.is_lion:
                try:
                    registree['club'] = self.engine.execute(sa.select([tc.c.club],
                                                         tc.c.reg_num == r.reg_num)).fetchone()[0]
                except Exception as e:
                    registree['club'] = None
            else:
                try:
                    registree['partner_program'] = bool(
                        self.engine.execute(
                            tpp.select(whereclause=tpp.c.reg_num == r.reg_num)
                        ).fetchone()[1]
                    )
                except Exception:
                    registree['partner_program'] = False

            try:
                registree['full'] = self.engine.execute(
                    sa.select([tfr.c.quantity], whereclause=tfr.c.reg_num == r.reg_num)
                ).fetchone()[0]
            except Exception:
                registree['full'] = 0

            try:
                partial = self.engine.execute(
                    tpr.select(whereclause=tpr.c.reg_num == r.reg_num)
                ).fetchone()
                registree['banquet'] = partial["banquet_quantity"]
                registree['convention'] = partial["convention_quantity"]
                registree['theme'] = partial["theme_quantity"]
            except Exception:
                registree['banquet'] = 0
                registree['convention'] = 0
                registree['theme'] = 0

            try:
                registree['pins'] = self.engine.execute(
                    sa.select([tp.c.quantity], whereclause=tp.c.reg_num == r.reg_num)
                ).fetchone()[0]
            except Exception:
                registree['pins'] = 0

            try:
                registree['paid'] = self.engine.execute(
                    sa.select([sa.func.sum(tpy.c.amount)], whereclause=tpy.c.reg_num == r.reg_num)
                ).fetchone()[0]
                if not registree['paid']:
                    registree['paid'] = Decimal(0).quantize(TWOPLACES)
                else:
                    registree['paid'] = Decimal(registree['paid']).quantize(TWOPLACES)
            except Exception:
                raise
                registree['paid'] = Decimal(0).quantize(TWOPLACES)

            registrees.append(Registree(**registree))
        registrees.sort()
        return registrees

    def set_reg_nums(self, reg_num):
        tp = self.tables["registree_pair"]
        res = self.engine.execute(sa.select([tp.c.first_reg_num, tp.c.second_reg_num],
                                            sa.or_(tp.c.first_reg_num == reg_num,
                                                   tp.c.second_reg_num == reg_num))).fetchone()
        if res:
            self.reg_nums = [res[0], res[1]]
        else:
            self.reg_nums = [reg_num]

class Stats(object):
    def __init__(self, registrees):
        self.registrees = registrees
        freq = Counter([r.club for r in self.registrees]).most_common()
        self.club_freq_num = freq[0][1]
        names = []
        for (name, num) in freq:
            if num == self.club_freq_num:
                names.append(name)
            else:
                break
        self.club_freq_name = ', '.join(names)
        self.num_clubs = len(set([r.club for r in self.registrees]))

    def build_public_stats(self):
        with open(PUBLIC_URL_PATH, 'w') as fh:
            fh.write(PUBLIC_HEADER)
            fh.write('<ul>')
            fh.write(f'<li><strong>Number of Registrees</strong>: {len(self.registrees)}</li>\n')
            fh.write('\n')
            fh.write(f'<li><strong>Number of Clubs</strong>: {self.num_clubs}</li>\n')
            fh.write('\n')
            fh.write(f'<li><strong>Club{"s" if ", " in self.club_freq_name else ""} With Most Attendees</strong>: {self.club_freq_name} ({self.club_freq_num} registrees)</li>\n')
            fh.write('</ul>')
            fh.write(PUBLIC_TABLE_HEADER)
            for registree in self.registrees:
                fh.write(f"<tr><td>{registree.name}</td><td>{registree.club if registree.is_lion else '(Partner in Service)'}</td></tr>")
            fh.write(TABLE_FOOTER)

    def build_full_stats(self):
        with open(FULL_URL_PATH, 'w') as fh:
            fh.write(FULL_HEADER)
            fh.write('<ul>')
            fh.write(f'<li><strong>Number of Registrees</strong><ul>\n')
            fh.write(f'<li><strong>Total</strong>: {len(self.registrees)}</li>\n')
            fh.write(f'<li><strong>Lions</strong>: {len([r for r in self.registrees if r.is_lion])}</li>\n')
            fh.write(f'<li><strong>Partners In Service</strong>: {len([r for r in self.registrees if not r.is_lion])}</li>\n')
            fh.write('</ul>\n')
            fh.write(f'<li><strong>Number of Clubs</strong>: {len(set([r.club for r in self.registrees]))}</li>\n')
            fh.write(f'<li><strong>Club{"s" if ", " in self.club_freq_name else ""} With Most Attendees</strong>: {self.club_freq_name} ({self.club_freq_num} registrees)</li>\n')
            fh.write('<li><strong>Registrations</strong></li><ul>')
            for a in ('full', 'banquet', 'convention', 'theme'):
                fh.write(f'<li><strong>{a.capitalize()}</strong>: {sum([getattr(r, a) for r in self.registrees])}\n')
            fh.write('</ul>')
            fh.write('<li><strong>Extra Items</strong></li><ul>\n')
            for a in ('pins', ):
                fh.write(f'<li><strong>{a.capitalize()}</strong>: {sum([getattr(r, a) for r in self.registrees])}\n')
            fh.write('</ul>')
            fh.write('<li><strong>Extra Activities</strong></li><ul>\n')
            for a in ("mjf_lunch","pdg_breakfast","sharks_board","golf","sight_seeing","service_project","partner_program",):
                fh.write(f'<li><strong>{" ".join([i.capitalize() if len(i) > 3 else i.upper() for i in a.split("_")])}</strong>: {sum([bool(getattr(r, a)) for r in self.registrees])}\n')
            fh.write('</ul>\n')
            fh.write(f'<li><strong>Total Owed:</strong> R{sum([r.initial_owed for r in self.registrees])}</li>\n')
            fh.write(f'<li><strong>Paid:</strong> R{sum([r.paid for r in self.registrees])}</li>\n')
            fh.write(f'<li><strong>Still Owed:</strong> R{sum([r.still_owed for r in self.registrees])}</li>\n')

            for attr in ('dietary', 'disability'):
                fh.write(f'<li><strong>{attr.capitalize()} Requirements</strong></li><ul>\n')
                items = []
                for r in self.registrees:
                    a = getattr(r, attr)
                    if a and (not any([c == a.strip().lower() for c in ('nil', 'none', 'n/a', 'n / a', 'any', 'na', 'no')])):
                        items.append(a)
                if not items:
                    items = ['None Recorded']
                else:
                    items = list(set(items))
                    items.sort()
                for d in items:
                    fh.write(f'<li>{d}</li>\n')
                fh.write('</ul>\n')
            fh.write('</ul>\n')

            fh.write(FULL_TABLE_HEADER)
            for registree in self.registrees:
                fh.write(f"""
<tr{' style="background-color: lightgreen"' if not registree.still_owed else ''}{' style="background-color: yellow"' if not registree.paid else ''}>
<td>{registree.reg_num}</td>
<td>{registree.name}</td>
<td>{registree.club if registree.is_lion else '(Partner in Service)'}</td>
<td>{registree.name_badge}</td>
<td>{registree.initial_owed}</td>
<td>{registree.paid}</td>
<td>{registree.still_owed}</td>
</tr>\n
    """)
            fh.write(TABLE_FOOTER)

            reg_dates = [r.timestamp for r in self.registrees]
            reg_dates.sort()
            plot.plot_registration_dates(reg_dates, '../../static/img/registrations_over_time.png')
            fh.write('<div style="text-align:center"><img src="/img/registrations_over_time.png"></div>')
            fh.write(FOOTER)

db = DB()
stats = Stats(db.get_registrees())
stats.build_public_stats()
stats.build_full_stats()
