from mdblog.template import render_entry, parse_entry


def find_entries():
    "Find entries, compile them and add them to db"
    entries = []
    path = "%s/*.md" % templates_path
    for entry_path in glob.glob(path):
        with open(entry_path) as raw_entry:
            headers, body = parse_entry(raw_entry)
        entry_dict = {"body": render_entry(body)}
        entry_dict.update(headers)
        entries.append(entry_dict)

    return entries

