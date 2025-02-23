# I think the general format of this is going to be:
#   parse_grocery_list()
#   get_items()
#   solve()
import argparse
from typing import List, Optional


class GroceryItem:
    """Container class for parsed grocery list items. WIP"""

    def __init__(self, name: str, qty: int):
        self.name = name
        self.qty = qty

    def __repr__(self):
        return f"GroceryItem(name={self.name}, qty={self.qty})"


class PurchaseCandidate:
    """Container class for item that can be bought. WIP"""

    def __init__(self, id: int, name: str, price: int):
        self.id = id
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Item(id={self.id}, name={self.name}, price={self.price})"


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=__name__, description=__doc__)
    parser.add_argument("input_file", required=True)
    parser.add_argument("-n", "--no_items", required=False)
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    grocery_list = parse_grocery_list(args.input_file)
    candidates = get_items(grocery_list)
    solve(candidates)


def solve(purchase_candidates: List[PurchaseCandidate], constraints=None):
    pass


def parse_grocery_list(text_list: str) -> Optional[List[GroceryItem]]:
    pass


def get_items(parsed_items: List[GroceryItem]) -> Optional[List[PurchaseCandidate]]:
    pass


if __name__ == "__main__":
    main()
