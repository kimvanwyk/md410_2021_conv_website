CLUBS = []
with open("clubs.txt", "r") as fh:
    CLUBS = [l.strip() for l in fh]


class HTML(object):
    def __init__(self):
        self.out = [
            "---",
            "title: Registration Form",
            "draft: false",
            "---",
            "",
            '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>',
            '<script src="/js/reg_form.js"></script>',
            '<form name="registration" method="POST" data-netlify="true" action="/registration_result">',
        ]
        self.level = 1

    def close(self):
        self.out.append(f'{"~" * self.level}The details of your registration will be sent to you, including a unique registration number. Payment details will also be included in that email. Please make all payments using your registration number as a reference.')
        self.out.append(f'{"~" * self.level}<br>')
        self.out.append(f'{"~" * self.level}<ul>')
        self.level += 1
        self.out.append(f'{"~" * self.level}<li><strong>Bank</strong>: ABC</li>') 
        self.out.append(f'{"~" * self.level}<li><strong>Branch</strong>: DEF</li>') 
        self.out.append(f'{"~" * self.level}<li><strong>Account Number</strong>: 12345</li>') 
        self.out.append(f'{"~" * self.level}<li><strong>Account Name</strong>: 2020 MD410 Convention</li>') 
        self.level -= 1
        self.out.append(f'{"~" * self.level}</ul>')
        self.out.append(f'{"~" * self.level}Your registration will be finalised on the payment of a deposit of R300 per attendee. Payments can be made in as many instalments as you wish, as long as full payment is received by 31 March 2020.')
        self.out.append(f'{"~" * self.level}<ul>')
        self.level += 1
        self.out.append(f'{"~" * self.level}<li>If your registration is cancelled before 1 April 2020, 90% of the payments you have made will be refunded.</li>')
        self.out.append(f'{"~" * self.level}<li>Cancellations after 1 April will not be refunded as the full expenses will already have been incurred for the registration.</li>')
        self.level -= 1
        self.out.append(f'{"~" * self.level}</ul>')
        self.out.append(f'{"~" * self.level}<center>')
        self.level += 1
        self.out.append(
            f'{"~" * self.level}<button type="submit">Submit Registration Form</button>'
        )
        self.level -= 1
        self.out.append(f'{"~" * self.level}</center>')
        self.level -= 1
        self.out.append("</form>")

    def render(self):
        return "\n".join([l.replace("~", "   ") for l in self.out])

    def open_containing_div(self, cls=None):
        if cls:
            cls_div = f' id="{cls}_div"'
            cls_fs = f' id="{cls}_fs"'
        else:
            cls_div = ""
            cls_fs = ""
        self.out.append(f"{'~' * self.level}<div{cls_div}>")
        self.level += 1
        self.out.append(f"{'~' * self.level}<fieldset{cls_fs} disabled>")
        self.level += 1

    def close_containing_div(self):
        self.level -= 1
        self.out.append(f"{'~' * self.level}</fieldset>")
        self.level -= 1
        self.out.append(f"{'~' * self.level}</div>")

    def open_form_item(self, tag, label, number=False):
        self.out.append(f'{"~" * self.level}<div class="form-group row">')
        self.level += 1
        self.out.append(
            f'{"~" * self.level}<label for="{tag}" class="col-sm-{"8" if number else "4"} col-form-label">'
        )
        self.level += 1
        self.out.append(f'{"~" * self.level}{label}: ')
        self.level -= 1
        self.out.extend(
            (
                f'{"~" * self.level}</label>',
                f'{"~" * self.level}<div class="col-sm-{"4" if number else "8"}">',
            )
        )
        self.level += 1

    def close_form_item(self):
        self.level -= 1
        self.out.append(f'{"~" * self.level}</div>')
        self.level -= 1
        self.out.append(f'{"~" * self.level}</div>')

    def add_header(self, text):
        self.out.append(f'{"~" * self.level}<h2>{text}</h2>')

    def add_label(self, tag, text, centre=False):
        self.out.append(f'{"~" * self.level}<div class="form-group row">')
        self.level += 1
        if centre:
            self.out.append(f'{"~" * self.level}<center>')
            self.level += 1
        self.out.append(f'{"~" * self.level}<label id={tag}>{text}</label>')
        self.level -= 1
        if centre:
            self.out.append(f'{"~" * self.level}</center>')
            self.level -= 1
        self.out.append(f'{"~" * self.level}</div>')

    def add_text(
        self, tag, label, help="", type="text", cls="", cost=None, disabled=False
    ):
        self.open_form_item(tag, label, number=type == "number")
        if help:
            help_attr = f' aria-describedby="{tag}_help"'
        else:
            help_attr = ""
        if cost:
            cost_attr = f" cost={cost}"
        else:
            cost_attr = ""
        base_class = "form-control"
        if cls:
            class_attr = f"{base_class} {cls}"
        else:
            class_attr = base_class
        inner = [
            f'{"~" * self.level}<input type="{type}" class="{class_attr}" id="{tag}" name="{tag}"{help_attr}{cost_attr}{" disabled" if disabled else ""}>'
        ]
        if help:
            inner.append(
                f'{"~" * self.level}<small id="{tag}_help" class="form-text text-muted">'
            )
            self.level += 1
            inner.append(f'{"~" * self.level}{help}')
            self.level -= 1
            inner.append(f'{"~" * self.level}</small>')
        self.out.extend(inner)
        self.close_form_item()

    def add_email(self, tag, label, help=""):
        self.add_text(tag, label, help=help, type="email")

    def add_checkbox(self, tag, label, help=""):
        if help:
            help_attr = f' aria-describedby="{tag}_help"'
        else:
            help_attr = ""
        self.out.append(f'{"~" * self.level}<div class="form-check">')
        self.level += 1
        self.out.extend(
            (
                f'{"~" * self.level}<input class="form-check-input" type="checkbox" value="{tag}" name="{tag}" id="{tag}"{help_attr}>',
                f'{"~" * self.level}<label class="form-check-label" for="{tag}">',
            )
        )
        self.level += 1
        self.out.append(f'{"~" * self.level}{label}')
        self.level -= 1
        self.out.append(f'{"~" * self.level}</label>')
        if help:
            self.out.append(
                f'{"~" * self.level}<small id="{tag}_help" class="form-text text-muted">'
            )
            self.level += 1
            self.out.append(f'{"~" * self.level}{help}')
            self.level -= 1
            self.out.append(f'{"~" * self.level}</small>')
        self.level -= 1
        self.out.append(f'{"~" * self.level}</div>')

    def add_selector(self, tag, label, items, help=""):
        self.open_form_item(tag, label)
        if help:
            help_attr = f' aria-describedby="{tag}_help"'
        else:
            help_attr = ""
        inner = [
            f'{"~" * self.level}<select class="form-control" id="{tag}" name="{tag}"{help_attr}>'
        ]
        self.level += 1
        inner.extend(
            [
                f'{"~" * self.level}<option value="{item}">{item}</option>'
                for item in items
            ]
        )
        self.level -= 1
        inner.append(f'{"~" * self.level}</select>')
        if help:
            inner.append(
                f'{"~" * self.level}<small id="{tag}_help" class="form-text text-muted">'
            )
            self.level += 1
            inner.append(f'{"~" * self.level}{help}')
            self.level -= 1
            inner.append(f'{"~" * self.level}</small>')
        self.out.extend(inner)
        self.close_form_item()

    def add_radios(self, name, options):
        self.out.append(f'{"~" * self.level}<div class="form-group row">')
        self.level += 1
        for (n, (k, v)) in enumerate(options.items()):
            self.out.append(f'{"~" * self.level}<div class="form-check">')
            self.level += 1
            self.out.append(
                f'{"~" * self.level}<input class="form-check-input" type="radio" name="{name}" id="{k}" value="{k}"{" checked" if n == 0 else ""}>'
            )
            self.out.append(
                f'{"~" * self.level}<label class="form-check-label" for="{k}">'
            )
            self.level += 1
            self.out.append(f'{"~" * self.level}{v}')
            self.level -= 1
            self.out.append(f'{"~" * self.level}</label>')
            self.level -= 1
            self.out.append(f'{"~" * self.level}</div>')
        self.level -= 1
        self.out.append(f'{"~" * self.level}</div>')

    def add_divider(self):
        self.out.append(f'{"~" * self.level}<hr>')


def make_attendee_fields(html, prefix, lion=True):
    html.add_text(
        f"{prefix}_first_names",
        "First Name(s)",
        "Attendee's first name or names. Please use a real name rather than a nickname - nicknames can however be used for the name badge later in this form.",
    )
    html.add_text(f"{prefix}_last_name", "Last Name")
    if lion:
        html.add_selector(f"{prefix}_club", "Lions Club", CLUBS)
    html.add_text(
        f"{prefix}_cell",
        "Cell Phone",
        "A cellphone number the attendee can be reached at if needed. This number may also be used for urgent SMSes for changes of plan during the convention.",
    )
    html.add_email(f"{prefix}_email", "Email Address")
    html.add_text(
        f"{prefix}_dietary",
        "Dietary Requirements",
        help="Please be VERY clear with these requirements. eg halal, kosher, vegetarian, allergic to dairy"
    )
    html.add_text(
        f"{prefix}_disability",
        "Special Access Requirements",
        help="Please indicate any requirements for wheel chair access or the like, if applicable",
    )
    html.add_text(
        f"{prefix}_name_badge",
        "Name Badge",
        help=f"The name to appear on the attendee's name badge. eg {'Joe Bloggs; Lion John Doe, ZC Wendy Bloggs, PDG Jane Doe' if lion else 'Joe Bloggs, Partner in Service Jane Doe'}",
    )

    html.add_checkbox(f"{prefix}_first_mdc", "This will be the attendee's first Multiple District Convention")

    html.add_checkbox(
        f"{prefix}_mjf_lunch",
        'Attendee will attend the <a href="/events/mjf_lunch">Melvin Jones Lunch</a>.',
        help="This lunch is only open to Melvin Jones Fellows and may carry an additional charge. Details will be provided closer to the time.",
    )

    html.add_checkbox(
        f"{prefix}_pdg_breakfast",
        'Attendee will attend the <a href="/events/pdgs_breakfast">PDG\'s Breakfast.</a>',
        help='This event may carry an additional charge, especially if the attendee is not staying at the <a href="/venue">Riverside Hotel</a>. Details will be provided closer to the time.',
    )

    if not lion:
        html.add_checkbox(
            f"{prefix}_partner_program",
            "Attendee would be interested in the partner's program.",
            help="The partner's program may involve an additional cost. Details will be provided closer to the time.",
        )


html = HTML()
html.add_header("First Attendee")
make_attendee_fields(html, "main")
html.add_divider()
html.add_radios(
    "partner",
    {
        "partner_none": "No partner will be coming with me",
        "partner_lion": "My Lion partner will be coming with me",
        "partner_non_lion": "My non-Lion partner in service will be coming with me",
    },
)
html.open_containing_div(cls="partner_lion")
html.add_header("Lion Partner")
make_attendee_fields(html, "partner_lion")
html.close_containing_div()
html.open_containing_div(cls="partner_non_lion")
html.add_header("Non Lion Partner")
make_attendee_fields(html, "partner_non_lion", lion=False)
html.close_containing_div()
html.add_divider()
html.add_header("Registrations")
html.add_radios(
    "reg_type",
    {
        "full_reg": "I will be making full registrations",
        "partial_reg": "I will be making one or more partial registrations",
    },
)
html.open_containing_div(cls="full_reg")
html.add_header("Full Registrations")
html.add_text(
    "full_reg",
    "Full Registrations (R1285 per person)",
    help="Full registration includes <ul><li>Lunch and teas during MD Convention</li><li>Banquet</li><li>Theme Evening</li></ul>",
    type="number",
    cls="total",
    cost=1300,
)
html.close_containing_div()
html.open_containing_div(cls="partial_reg")
html.add_header("Partial Registrations")
html.add_text(
    "partial_reg_banquet",
    '<a href="/events/banquet">Banquet Registrations</a> (R500 per person)',
    type="number",
    cls="total",
    cost=600,
)
html.add_text(
    "partial_reg_convention",
    '<a href="/events/md_convention">MD410 Convention</a> (R400 per person)',
    type="number",
    cls="total",
    cost=450,
)
html.add_text(
    "partial_reg_theme",
    '<a href="/events/theme_evening">Theme Evening Registrations</a> (R450 per person)',
    type="number",
    cls="total",
    cost=600,
)
html.close_containing_div()
html.add_divider()
html.add_header("Extra Items")
html.add_text(
    "pins", "Convention Pins (R55 per pin)", type="number", cls="total", cost=55
)
html.add_divider()
html.add_label("total_cost", "Total Cost: R0", centre=True)
html.close()

with open("../../content/registration/_index.html", "w") as fh:
    fh.write(html.render())
print(html.render())
