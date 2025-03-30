"""
Communicating with a LLM to tag scraped product information
"""

import json
import os
import requests
import sys

from grocery_calculator.logger import setup_logger

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

TAGGED_ATTRS = {
    "product_name": str,
    "product_type": str,
    "flavor_or_variant": str,
    "size": str,
    "packaging_type": str,
    "sale": bool,
    "sale_value": float,
    "tags": list,
}

logger = setup_logger(__name__)


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
    logger.info("response from LLM is %s", data)

    remaining_attrs = TAGGED_ATTRS.copy()
    logger.debug("expected tagged attributes are %s", remaining_attrs)

    to_delete = []
    for attr in data:
        if attr not in remaining_attrs:
            logger.warning("unknown attribute found - %s", attr)
            to_delete.append(attr)
        else:
            del remaining_attrs[attr]

    for attr in to_delete:
        del data[attr]

    for attr in remaining_attrs:
        logger.warning("could not find attribute %s. setting to null", attr)
        data[attr] = None

    return data


if __name__ == "__main__":
    print(tag_item(sys.argv[1]))
