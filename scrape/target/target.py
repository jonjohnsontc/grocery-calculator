import requests

URL = "https://redsky.target.com/redsky_aggregations/v1/web/product_summary_with_fulfillment_v1"


def get_target():
    response = requests.get(
        URL,
        params={
            "page": "s/yogurt",
            "store_id": 2479,
            "required_store_id": 2479,
            # "key": "9f36aeafbe60771e321a7cc95a78140772ab3e96",
            # "tcins": "13016477,13016490,13043725,13308678,13376152,14859438,14953055,14953056,14990487,15242876,15247366,23937892,24013290,24013291,26399564,46774662,46774664,46778312,51393466,53918346,54514895,54514903,54609545,78362089,79543730,81426165,87237310,87237313,90555456,90555467",
        },
        headers={"Content-Type": "application/json"},
    )
    return response


if __name__ == "__main__":
    r = get_target()
