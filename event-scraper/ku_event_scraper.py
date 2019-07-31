import requests
from bs4 import BeautifulSoup
import re
import datetime
import hashlib


def parse_location(location_string):
    matches = re.search(r'Ort: (.*)$', location_string.strip())

    if matches:
        return matches[1]
    else:
        return ""


def parse_date(date_string):
    matches = re.search(r'([0-9]{2})\.([0-9]{2})\.(2[0-9]{3})', date_string)
    year = int(matches[3])
    month = int(matches[2])
    day = int(matches[1])
    return datetime.datetime(year, month, day)


def ku_get_latest_events():
    response = requests.get("http://www.kufstein.at/de/events.html")
    soup = BeautifulSoup(response.content, 'html.parser')

    events = []
    items = soup.select('article')
    for item in items:
        title_tag = item.select_one('.title')
        date_tag = item.select_one('.date')
        link_tag = item.select_one('a.title')
        short_tag = item.select_one('.text')
        location_tag = item.select_one('.addition')

        if short_tag != None:
            short_tag = short_tag.get_text()
        else:
            short_tag = ''

        name = title_tag.get_text()
        date = parse_date(date_tag['data-date'].strip())
        location = location_tag.get_text()

        hash = hashlib.sha256()
        hash.update(bytes(name, 'utf-8'))
        hash.update(bytes(location, 'utf-8'))
        hash.update(bytes(str(date.time()), 'utf-8'))

        events.append({
            "name": name,
            "date": date,
            "location": location,
            "link": "https://www.kufstein.at" + link_tag['href'].strip(),
            "short": short_tag,
            "source": "Stadt Kufstein Homepage",
            "identifier": hash.hexdigest()
        })

    return events
