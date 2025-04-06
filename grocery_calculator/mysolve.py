# I think the general format of this is going to be:
#   parse_grocery_list()
#   get_items()
#   solve()
import argparse
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, PULP_CBC_CMD


@dataclass
class GroceryItem:
    """Container class for parsed grocery list items. WIP"""

    name: str
    qty: int


@dataclass
class Store:
    """Container class for store to purchase from. WIP"""

    def __init__(self, id: int, name: str, address: str, zip_code: str):
        self.id = id
        self.name = name
        self.address = address
        if len(zip_code) != 5 or not all([d.isdigit() for d in zip_code]):
            raise ValueError("Not valid zip code, you passed %s", zip_code)
        self.zip_code = zip_code


@dataclass
class PurchaseCandidate:
    """Container class for item that can be bought. WIP"""

    id: int
    store: Store
    name: str
    price: int
    item: GroceryItem

    def __repr__(self):
        return f"Item(id={self.id}, name={self.name}, price={self.price})"

    def to_dict(self):
        return {
            "id": self.id,
            "store": self.store.name,
            "name": self.name,
            "price": self.price,
            "item": {"name": self.item.name, "qty": self.item.qty},
        }


class GroceryTrip:
    """Container for individual grocery trip from solver. WIP"""

    store: str
    location: str
    total: float
    items: List[PurchaseCandidate]

    def __init__(self, store, location):
        self.store = store
        self.location = location
        self.total = 0
        self.items = None

    def add_item(self, item: PurchaseCandidate):
        """Add item to items array and add cost to total"""
        self.items.append(item)
        self.total += item.price

    def to_dict(self):
        return {
            "store": self.store,
            "location": self.location,
            "total": self.total,
            "items": [item.to_dict() for item in self.items],
        }


class SolvedProblem:
    """Container for attributes we want in a solution. WIP"""

    num_stores: int
    total_cost: float
    trips: List[GroceryTrip]

    def __init__(self):
        self.num_stores = None
        self.total_cost = None
        self.trips = None

    def to_dict(self):
        return {
            "num_stores": self.num_stores,
            "total_cost": self.total_cost,
            "trips": [trip.to_dict() for trip in self.trips],
        }


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


def lp_solve(
    stores: List[Store],
    pc: List[PurchaseCandidate],
    max_stores: int = 2,
) -> Tuple[dict, dict, LpProblem]:

    items_by_cat = defaultdict(list)
    for item in pc:
        items_by_cat[item.item.name].append(item)

    problem = LpProblem()
    problem = LpProblem("GroceryOptimization", LpMinimize)
    x = LpVariable.dicts(
        "x",
        [(item.item.name, item.store.name) for item in pc],
        cat="Binary",
    )
    y = LpVariable.dicts("y", [s.name for s in stores], cat="Binary")

    problem += lpSum(item.price * x[(item.item.name, item.store.name)] for item in pc)

    for category, items in items_by_cat.items():
        problem += lpSum(x[category, item.store.name] for item in items) == 1

    problem += lpSum(y[store.name] for store in stores) <= max_stores

    for item in pc:
        problem += x[(item.item.name, item.store.name)] <= y[item.store.name]

    problem.solve(PULP_CBC_CMD(msg=False))  # we don't want to see the solver output
    return (x, y, problem)


def solve(
    valid_stores: List[Store],
    purchase_candidates: List[PurchaseCandidate],
    constraints=None,
) -> SolvedProblem:
    results = SolvedProblem()

    (x, y, problem) = lp_solve(valid_stores, purchase_candidates)
    if problem.status != 1:
        raise RuntimeError("Solver failed to find a solution")
    results.total_cost = problem.objective.value()

    stores_to_purchase_from: Set[str] = set()
    items_to_purchase: Dict[str, List[PurchaseCandidate]] = {}
    for item in purchase_candidates:
        if x[(item.item.name, item.store.name)].value() == 1:
            stores_to_purchase_from.add(item.store.name)
            if item.store.name not in items_to_purchase:
                items_to_purchase[item.store.name] = []
            items_to_purchase[item.store.name].append(item)

    results.num_stores = len(stores_to_purchase_from)
    results.trips = []
    for store in stores_to_purchase_from:
        try:
            store_obj = next(filter(lambda s: s == store, valid_stores))
        except StopIteration:
            raise RuntimeError("No store found in store obj, something's wrong")

        trip = GroceryTrip(store_obj.name, store_obj.address)
        for item in items_to_purchase[store]:
            trip.add_item(item)

        results.trips.append(trip)

    return results


def parse_grocery_list(text_list: str) -> Optional[List[GroceryItem]]:
    pass


def get_items(parsed_items: List[GroceryItem]) -> Optional[List[PurchaseCandidate]]:
    pass


if __name__ == "__main__":
    main()
