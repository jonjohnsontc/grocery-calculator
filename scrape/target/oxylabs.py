import os
import requests
from pprint import pprint

user = os.getenv("OXY_USER")
password = os.getenv("OXY_PASS")

# Structure payload.
payload = {
    "source": "universal",
    "url": "https://www.target.com/s?searchTerm=whole+bean+coffee&tref=typeahead%7Cterm%7Cwhole+bean+coffee%7C%7C%7Chistory",
    "geo_location": "United States",
    "render": "html",
    "parse": True,
}

# Get response.
response = requests.request(
    "POST",
    "https://realtime.oxylabs.io/v1/queries",
    auth=(user, password),
    json=payload,
)

# Instead of response with job status and results url, this will return the
# JSON response with the result.
pprint(response.json())
