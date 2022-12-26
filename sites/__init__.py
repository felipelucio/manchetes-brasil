from dataclasses import dataclass, field
from datetime import datetime

class Scrapper:
    def __init__(self, parser):
        self._parser = parser

    @property
    def parser(self):
        return self._parser


@dataclass
class HeadlineUpdate:
    date: datetime
    old_headline: str

@dataclass
class SectionUpdate:
    date: datetime
    old_section: str


@dataclass
class Register:
    url: str
    site: str
    headline: str
    subheadline: str
    section: str
    img: str
    tag: str
    date: datetime

