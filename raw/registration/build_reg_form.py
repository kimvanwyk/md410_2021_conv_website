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
            '<form name="registration" method="POST" data-netlify="true">',
        ]
        self.level = 1

    def close(self):
        self.out.append("</form>")

    def render(self):
        return "\n".join([l.replace("~", "   ") for l in self.out])

    def open_containing_div(self, cls=None):
        if cls:
            cls = f' id="{cls}"'
        else:
            cls = ""
        self.out.append(f"{'~' * self.level}<div{cls}>")
        self.level += 1

    def close_containing_div(self):
        self.level -= 1
        self.out.append(f"{'~' * self.level}</div>")

    def open_form_item(self, tag, label):
        self.out.append(
                f'{"~" * self.level}<div class="form-group row">'
        )
        self.level += 1
        self.out.append(
            f'{"~" * self.level}<label for="{tag}" class="col-sm-4 col-form-label">'
        )
        self.level += 1
        self.out.append(
            f'{"~" * self.level}{label}: '
        )
        self.level -= 1
        self.out.extend(
            (
                f'{"~" * self.level}</label>',
                f'{"~" * self.level}<div class="col-sm-8">',
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

    def add_text(self, tag, label, help="", type="text"):
        self.open_form_item(tag, label)
        if help:
            help_attr = f' aria-describedby="{tag}_help"'
        else:
            help_attr = ""
        inner = [
            f'{"~" * self.level}<input type="{type}" class="form-control" id="{tag}" name="{tag}"{help_attr}>'
        ]
        if help:
            inner.append(
                    f'{"~" * self.level}<small id="{tag}_help" class="form-text text-muted">'
                )
            self.level += 1
            inner.append(
                    f'{"~" * self.level}{help}'
            )
            self.level -= 1
            inner.append(
                    f'{"~" * self.level}</small>',
            )
        self.out.extend(inner)
        self.close_form_item()

    def add_email(self, tag, label, help=""):
        self.add_text(tag, label, help=help, type="email")

    def add_selector(self, tag, label, items, help=""):
        self.open_form_item(tag, label)
        if help:
            help_attr = f' aria-describedby="{tag}_help"'
        else:
            help_attr = ""
        inner = [f'{"~" * self.level}<select class="form-control" id="{tag}" name="{tag}"{help_attr}>']
        self.level += 1
        inner.extend([f'{"~" * self.level}<option value="{item}">{item}</option>' for item in items])
        self.level -= 1
        inner.append(f'{"~" * self.level}</select>')
        if help:
            inner.append(
                    f'{"~" * self.level}<small id="{tag}_help" class="form-text text-muted">'
                )
            self.level += 1
            inner.append(
                    f'{"~" * self.level}{help}'
            )
            self.level -= 1
            inner.append(
                    f'{"~" * self.level}</small>',
            )
        self.out.extend(inner)
        self.close_form_item()

    def add_radios(self, name, options):
        self.out.append(f'{"~" * self.level}<div class="form-group row">')
        self.level += 1
        for (n,(k, v)) in enumerate(options.items()):
            self.out.append(
                    f'{"~" * self.level}<div class="form-check">'
                )
            self.level += 1
            self.out.append(
                f'{"~" * self.level}<input class="form-check-input" type="radio" name="{name}" id="{k}" value="{k}"{" checked" if n == 0 else ""}>'
            )
            self.out.append(
                f'{"~" * self.level}<label class="form-check-label" for="{k}">'
            )
            self.level += 1
            self.out.append(
                f'{"~" * self.level}{v}'
            )
            self.level -= 1
            self.out.append(
                f'{"~" * self.level}</label>'
            )
            self.level -= 1
            self.out.append(
                f'{"~" * self.level}</div>'
            )
        self.level -= 1
        self.out.append(f'{"~" * self.level}</div>')

html = HTML()
html.add_header("First Attendee")
html.add_text(
    "main_first_names",
    "First Names(s)",
    "Your first name or names. Please use your real name rather than a nickname - nicknames can however be used for your name badge later in this form.",
)
html.add_text("main_last_name", "Last Name")
html.add_selector("main_club", "Lions Club", CLUBS)
html.add_text(
    "main_cell",
    "Cell Phone",
    "A cellphone number you can be reached at if needed. Your number may also be used for urgent SMSes for changes of plan during the convention.",
)
html.add_email("main_email", "Email Address")
html.add_text(
    "main_dietary",
    "Dietary Requirements",
    help="Please be VERY clear with these requirements",
)
html.add_text(
    "main_disability",
    "Special Access Requirements",
    help="Please indicate any requirements for wheel chair access or the like, if applicable",
)
html.add_text(
    "main_name_badge",
    "Name Badge",
    help="The name you would like to appear on your name badge. eg Kim van Wyk; Lion Trevor Hobbs, ZC Dave Shone; PDG Lyn Botha",
)

html.add_radios("partner", {"partner_none": "No partner will be coming with me",
                            "partner_lion":"My Lion partner will be coming with me",
                            "partner_non_lion":"My non-Lion partner in service will be coming with me"})
html.open_containing_div(cls="partner_lion_div")
html.add_header("Lion Partner") 
html.close_containing_div()
html.open_containing_div(cls="partner_non_lion_div")
html.add_header("Non Lion Partner")
html.close_containing_div()
html.close()

with open("../../content/registration/_index.html", "w") as fh:
    fh.write(html.render())
print(html.render())
