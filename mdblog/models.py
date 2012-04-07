from operator import attrgetter

from mdblog.query import find_entries
from mdblog.date import build_date


class EntryManager:

    def __init__(self, query):
        self.query = query

    def latest(self, limit=1):
        return self.all()[:limit]

    def all(self):
        return self.sort([Entry(**e) for e in self.query()])

    def sort(self, entries):
        return sorted(entries, key=attrgetter("date"), reverse=True)


class Entry:
    objects = EntryManager(query=find_entries)

    def __init__(self, **attrs):
        for attr in attrs:
            if attr == "date":
                attrs[attr] = build_date(attrs[attr], "%Y-%m-%d")
            setattr(self, attr, attrs[attr])
