from collections import Counter

import attr
import sqlalchemy as sa


URL_PATH = '../../content/registrees/_index.md'
HEADER = '''---
title: Registration Stats
draft: false
---

'''
TABLE_HEADER = '''<h2>Registrees</h2>
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script type="text/javascript" src="https://cdnjs.com/libraries/jquery.tablesorter"></script>

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
FOOTER = '''    </tbody>
</table>

<script type="text/javascript">
    $(function() {
        $("#registreeTable").tablesorter();
    });
</script>

'''

TABLES = {
    "registree": ("md410_2020_conv", "registree"),
    "club": ("md410_2020_conv", "club"),
}

@attr.s
class Registree(object):
    last_name = attr.ib()
    first_names = attr.ib()
    club = attr.ib()
    is_lion = attr.ib()

    def __attrs_post_init__(self):
        self.name = f"{self.first_names.strip()} {self.last_name.strip()}"

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
            f"postgresql+psycopg2://{self.user}@{self.host}/{self.dbname}"
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
        res = self.engine.execute(sa.select([tr.c.reg_num, tr.c.first_names, tr.c.last_name, tr.c.is_lion])).fetchall()
        registrees = []
        
        for r in res:
            club = None
            if r.is_lion:
                try:
                    club = self.engine.execute(sa.select([tc.c.club],
                                                         tc.c.reg_num == r.reg_num)).fetchone()[0]
                except Exception as e:
                    club = None
            registrees.append(Registree(r.last_name.strip(), r.first_names.strip(), club, r.is_lion))
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


db = DB()
registrees = db.get_registrees()
(club_freq_name, club_freq_num) = Counter([r.club for r in registrees]).most_common(1)[0]
with open(URL_PATH, 'w') as fh:
    fh.write(HEADER)
    fh.write('''
<ul>
''')
    fh.write(f'<li><strong>Number of Registrees</strong>: {len(registrees)}</li>\n')
    fh.write('\n')
    fh.write(f'<li><strong>Number of Clubs</strong>: {len(set([r.club for r in registrees]))}</li>\n')
    fh.write('\n')
    fh.write(f'<li><strong>Club With Most Attendees</strong>: {club_freq_name} ({club_freq_num} registrees)\n')
    fh.write('''
</ul>
''')
    
    fh.write(TABLE_HEADER)
    for registree in registrees:
        fh.write(f"<tr><td>{registree.name}</td><td>{registree.club}</td></tr>")
    fh.write(FOOTER)
