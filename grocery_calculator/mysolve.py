# I think the general format of this is going to be:
#   parse_grocery_list()
#   get_items()
#   solve()
import argparse
from decimal import Decimal
from typing import List, Optional

from pulp import LpProblem, LpMinimize, LpVariable, lpSum


class GroceryItem:
    """Container class for parsed grocery list items. WIP"""

    def __init__(self, name: str, qty: int):
        self.name = name
        self.qty = qty

    def __repr__(self):
        return f"GroceryItem(name={self.name}, qty={self.qty})"


class Store:
    """Container class for store to purchase from. WIP"""

    def __init__(self, id: int, name: str, lat: Decimal, long: Decimal):
        self.id = id
        self.name = name
        self.lat = lat
        self.long = long

    def __repr__(self):
        return f"Store(name={self.name} at {self.lat}/{self.long})"


class PurchaseCandidate:
    """Container class for item that can be bought. WIP"""

    def __init__(self, id: int, store: Store, name: str, price: int, gi: GroceryItem):
        self.id = id
        self.store = store
        self.name = name
        self.price = price
        self.item = gi

    def __repr__(self):
        return f"Item(id={self.id}, name={self.name}, price={self.price})"


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=__name__, description=__doc__)
    parser.add_argument("input_file", required=True)
    parser.add_argument("-n", "--num-stores", required=False)
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    grocery_list = parse_grocery_list(args.input_file)
    candidates = get_items(grocery_list)
    solve(grocery_list, candidates)


def solve(
    items: List[GroceryItem],
    purchase_candidates: List[PurchaseCandidate],
    constraints=None,
):
    solver = LpProblem("GroceryOptimization", LpMinimize)

    # solver needs to:
    # create variables for items and stores

    pass


def parse_grocery_list(text_list: str) -> Optional[List[GroceryItem]]:
    pass


def get_items(parsed_items: List[GroceryItem]) -> Optional[List[PurchaseCandidate]]:
    pass


if __name__ == "__main__":
    main()
