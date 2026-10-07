"""Verify the requested label at the existing public dashboard seam."""

from html.parser import HTMLParser

from relayboard.testing import request
from relayboard.web import create_seeded_app


class JobsHeadings(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_jobs = False
        self.in_heading = False
        self.headings = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_jobs = dict(attrs).get("id") == "jobs"
        if tag == "th" and self.in_jobs:
            self.in_heading = True

    def handle_endtag(self, tag):
        if tag == "th":
            self.in_heading = False
        if tag == "table":
            self.in_jobs = False

    def handle_data(self, data):
        if self.in_heading:
            self.headings.append(data)


code, body = request(create_seeded_app(), "GET", "/dashboard")
assert code == 200, code
parser = JobsHeadings()
parser.feed(body)
print("Observed Jobs headings:", parser.headings)
assert parser.headings == ["Job", "Enabled", "Latest result"], parser.headings
print("PASS: Jobs table shows Latest result")
