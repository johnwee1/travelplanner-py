import requests, io, re, logging
import pandas as pd
from parsedates import DateParser

# CHANGE YOUR CONSTANTS HERE
"""NOTE: This script fails if no "name" and "availabilities" columns exist."""
#


def _test():
    # add your own unit test here
    pass


def process_sheets_url(url):
    _test()
    # Extract the first gid
    gid_match = re.search(r"gid=(\d+)", url)
    # Remove 'edit?resourcekey=' and everything after it
    url = re.sub(r"edit\?resourcekey=.*", "", url)
    if gid_match:
        gid = gid_match.group(1)

        # Construct the new URL
        processed_url = f"{url}export?format=csv&gid={gid}"

        return processed_url
    else:
        raise ValueError(
            "No gid found in URL. This is a breaking error! Google probably messed with the URL structure cuz this used to work."
        )


def retrieve_db(url) -> dict[str, DateParser]:
    raw_csv = requests.get(process_sheets_url(url)).content.decode("utf-8")
    df = pd.read_csv(io.StringIO(raw_csv))
    # df = pd.read_csv("form.csv")

    db = {}

    for entry in df.itertuples():
        db[entry.name] = DateParser.update_availability(
            db.get(entry.name, []), str(entry.availabilities)
        )

    return db
