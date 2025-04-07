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

    def to_tuple(self):
        return (self.name, self.address, self.zip_code)

    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "zip_code": self.zip_code,
        }


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
        self.items = []

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

    @staticmethod
    def from_lp_solution(
        x, y, problem, purchase_candidates: List[PurchaseCandidate]
    ) -> "SolvedProblem":
        """Create a SolvedProblem from the LP solution"""
        result = SolvedProblem()
        result.total_cost = problem.objective.value()
        result.num_stores = sum(y[store].value() for store in y)

        result.trips = []
        # TODO: Figure out how to create without iterating over all purhase candidates
        # for each store
        for store in y:
            if y[store].value() == 1:
                trip = GroceryTrip(store[0], store[1])
                for item in purchase_candidates:
                    if (
                        x[(item.item.name, item.store.name)].value() == 1
                        and item.store.name == store[0]
                    ):
                        trip.add_item(item)
                result.trips.append(trip)
        return result

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
    y = LpVariable.dicts("y", [s.to_tuple() for s in stores], cat="Binary")

    problem += lpSum(item.price * x[(item.item.name, item.store.name)] for item in pc)

    for category, items in items_by_cat.items():
        problem += lpSum(x[category, item.store.name] for item in items) == 1

    problem += lpSum(y[store.to_tuple()] for store in stores) <= max_stores

    for item in pc:
        problem += x[(item.item.name, item.store.name)] <= y[item.store.to_tuple()]

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

    results = SolvedProblem.from_lp_solution(x, y, problem, purchase_candidates)
    return results


def parse_grocery_list(text_list: str) -> Optional[List[GroceryItem]]:
    pass


def get_items(parsed_items: List[GroceryItem]) -> Optional[List[PurchaseCandidate]]:
    pass


if __name__ == "__main__":
    main()
