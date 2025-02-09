"""
Communicating with a LLM to tag scraped product information
"""

import json
import os
import requests
import sys

from typing import List, Tuple

ENDPOINT = os.getenv("TAGGING_ENDPOINT", "http://localhost:11434/api/generate")
MODEL = os.getenv("TAGGING_MODEL", "deepseek-r1:7b")
QUERY = """
Given the description below of a product (marked after TEXT) available at an online retailer, 
could you extract any relevant entities? I'd like to know the following (with data types and examples
in parenthesis). Any other descriptive information about the product that doesn't connect 
to one of the below categories should go into `tags`. If there is no information that 
would match a particular entity (e.g, `size`) please instead respond with `null` for that entity.

Please respond in JSON format.

- product_name (varchar)
- product_type (varchar)
- flavor_or_variant (varchar)
- size (varchar, e.g, in oz)
- packaging_type (varchar, e.g. bottle, box, bag)
- sale (boolean)
- sale_value (float)
- tags (array[varchar])

TEXT: """


def tag_item(text: str):
    payload = {
        "model": MODEL,
        "prompt": QUERY + text,
        "format": "json",
        "raw": False,
        "stream": False,
    }
    response = requests.post(
        url=ENDPOINT,
        data=json.dumps(payload),
    )

    if response.status_code != 200:
        raise Exception(f"Request failed with {response.status_code}")

    data = response.json()["response"]
    data = json.loads(data.strip())

    return data


if __name__ == "__main__":
    print(tag_item(sys.argv[1]))
