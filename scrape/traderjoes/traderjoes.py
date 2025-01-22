import json
import logging
import os
import requests
import time

from datetime import datetime
from pathlib import Path

URL = "https://www.traderjoes.com/api/graphql"
QUERY = "query.graphql"
VERSION = "v0"
RAW_DATA_LOC = (
    Path(__file__)
    .parents[2]
    .joinpath("data", "raw_input", "trader_joes", VERSION)
    .as_posix()
)


def write_json(data, part, directory):
    with open(f"{directory}/part_{part}.json", "w+") as f:
        json.dump(data, f, indent=4)


def get_trader_joes():
    with open(QUERY, "r") as f:
        query = f.read()

    variables = {"storeCode": 217, "published": "1", "currentPage": 0, "pageSize": 100}
    response = requests.post(
        URL,
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Query failed with status code {response.status_code}")
        print(response.text)
        raise Exception("Failed")

    ts = datetime.now().isoformat()
    directory = f"{RAW_DATA_LOC}/{ts}"
    os.mkdir(directory)
    items = data["data"]["products"]["items"]
    write_json(items, variables["currentPage"], directory)

    total_pages = data["data"]["products"]["page_info"]["total_pages"]
    total_products = data["data"]["products"]["total_count"]
    logging.info("%d total products found", total_products)

    while variables["currentPage"] < total_pages:
        time.sleep(0.5)
        variables["currentPage"] += 1

        response = requests.post(
            URL,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"},
        )
        if response.status_code != 200:
            raise Exception(
                f"Part {variables['currentPage']} - failed with {response.status_code}"
            )
        data = response.json()
        items = data["data"]["products"]["items"]
        write_json(items, variables["currentPage"], directory)
        logging.info(f"part {variables['currentPage']} of {total_products} finished")

    return


if __name__ == "__main__":
    get_trader_joes()
