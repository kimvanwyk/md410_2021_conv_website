CLUBS = []
with open("clubs.txt", "r") as fh:
    CLUBS = [l.strip() for l in fh] + ["Other Club"]

DISTRICTS = ["410E", "410W", "Other District"]


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
        self.out.append(
            f'{"~" * self.level}The details of your registration will be sent to you, including a unique registration number.'
        )

    def close(self):
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

    def add_label(self, tag, text, centre=False, font=None):
        self.out.append(f'{"~" * self.level}<div class="form-group row">')
        self.level += 1
        if centre:
            self.out.append(f'{"~" * self.level}<center>')
            self.level += 1
        self.out.append(
            f'{"~" * self.level}<label id={tag}>{"<h3>" if font=="b" else ""}{text}{"</h3>" if font=="b" else ""}</label>'
        )
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
        m = ""
        if type == "number":
            m = 'min="0" value="0"'
        inner = [
            f'{"~" * self.level}<input type="{type}" {m} class="{class_attr}" id="{tag}" name="{tag}"{help_attr}{cost_attr}{" disabled" if disabled else ""}>'
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
        "Attendee's first name or names.",
    )
    html.add_text(f"{prefix}_last_name", "Last Name")

    if lion:
        html.add_selector(f"{prefix}_club", "Lions Club", CLUBS)
        html.add_selector(f"{prefix}_district", "District", DISTRICTS)
        html.add_checkbox(
            f"{prefix}_voter",
            "Are you a voting delegate for your club?",
        )
        html.add_checkbox(
            f"{prefix}_attending_district_convention",
            "Will you be attending your District's online convention on 24 April?",
        )
        html.add_checkbox(
            f"{prefix}_attending_md_convention",
            "Will you be attending the Multiple District online convention on 1 May?",
        )
    html.add_text(
        f"{prefix}_cell",
        "Cell Phone",
        "A cellphone number the attendee can be reached at if needed. This number may also be used for urgent SMSes for changes of plan during the convention.",
    )
    html.add_email(f"{prefix}_email", "Email Address")
    html.add_checkbox(
        f"{prefix}_first_mdc",
        "Will this be your first Multiple District Convention?",
    )


html = HTML()
html.add_header("Attendee Details")
make_attendee_fields(html, "main")
html.close()

with open("../../content/registration/_index.html", "w") as fh:
    fh.write(html.render())
print(html.render())
