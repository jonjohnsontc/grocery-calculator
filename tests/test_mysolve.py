import unittest

from grocery_calculator.mysolve import (
    solve,
    lp_solve,
    find_candidates,
    get_items,
    parse_grocery_list,
    parse_qty,
    GroceryItem,
    PurchaseCandidate,
    Store,
)


class TestMySolve(unittest.TestCase):

    INPUT_1 = """
    Bagels
    2lbs Pasta
    Extra Creamy oatmilk
    Coca-Cola 2 liter
    Potato Bread
    80/20 ground beef 1lb
    """

    INPUT_1_EXPECTED_PARSED_RESULT = [
        GroceryItem("Bagels", 1),
        GroceryItem("2lbs Pasta", 1),
        GroceryItem("Extra Creamy oatmilk", 1),
        GroceryItem("Coca-Cola 2 liter", 1),
        GroceryItem("Potato Bread", 1),
        GroceryItem("80/20 ground beef 1lb", 1),
    ]

    INPUT_2_PARSED_RESULT = [
        GroceryItem("milk", 1),
        GroceryItem("bread", 1),
        GroceryItem("eggs", 1),
    ]

    # TODO: Update
    STORES_1 = [
        Store(0, "store1", "123 Main St", "90290"),
        Store(1, "store2", "456 Oak St", "91212"),
        Store(2, "store3", "789 Pine St", "90290"),
    ]

    STORES_2 = [
        Store(0, "store1", "123 Main St", "90290"),
        Store(1, "store2", "456 Oak St", "91212"),
        Store(2, "store3", "789 Pine St", "90290"),
    ]

    # TODO: Update
    INPUT_1_PURCHASE_CANDIDATES = [
        PurchaseCandidate(
            0, STORES_2[0], "Brand A Milk", 200, INPUT_2_PARSED_RESULT[0]
        ),
        PurchaseCandidate(
            1, STORES_2[1], "Brand B Milk", 250, INPUT_2_PARSED_RESULT[0]
        ),
        PurchaseCandidate(
            2, STORES_2[2], "Brand C Milk", 210, INPUT_2_PARSED_RESULT[0]
        ),
        PurchaseCandidate(
            3, STORES_2[0], "Whole Wheat Bread", 100, INPUT_2_PARSED_RESULT[1]
        ),
        PurchaseCandidate(4, STORES_2[1], "White Bread", 120, INPUT_2_PARSED_RESULT[1]),
        PurchaseCandidate(
            5, STORES_2[2], "Mulitgrain Bread", 110, INPUT_2_PARSED_RESULT[1]
        ),
        PurchaseCandidate(
            6, STORES_2[0], "Organic Eggs", 300, INPUT_2_PARSED_RESULT[2]
        ),
        PurchaseCandidate(
            7, STORES_2[1], "Free-range Eggs", 280, INPUT_2_PARSED_RESULT[2]
        ),
    ]

    INPUT_2_PURCHASE_CANDIDATES = [
        PurchaseCandidate(
            0, STORES_2[0], "Brand A Milk", 200, INPUT_2_PARSED_RESULT[0]
        ),
        PurchaseCandidate(
            1, STORES_2[1], "Brand B Milk", 250, INPUT_2_PARSED_RESULT[0]
        ),
        PurchaseCandidate(
            2, STORES_2[2], "Brand C Milk", 210, INPUT_2_PARSED_RESULT[0]
        ),
        PurchaseCandidate(
            3, STORES_2[0], "Whole Wheat Bread", 100, INPUT_2_PARSED_RESULT[1]
        ),
        PurchaseCandidate(4, STORES_2[1], "White Bread", 120, INPUT_2_PARSED_RESULT[1]),
        PurchaseCandidate(
            5, STORES_2[2], "Mulitgrain Bread", 110, INPUT_2_PARSED_RESULT[1]
        ),
        PurchaseCandidate(
            6, STORES_2[0], "Organic Eggs", 300, INPUT_2_PARSED_RESULT[2]
        ),
        PurchaseCandidate(
            7, STORES_2[1], "Free-range Eggs", 280, INPUT_2_PARSED_RESULT[2]
        ),
    ]

    def test_lp_solve_returns_correct_program(self):

        (actual_x, actual_y, actual) = lp_solve(
            self.STORES_2, self.INPUT_2_PURCHASE_CANDIDATES
        )

        expected_optimal_cost = 580

        assert actual.objective.value() == expected_optimal_cost
        assert actual_x[("milk", "store1")] == 1
        assert actual_x[("bread", "store1")] == 1
        assert actual_x[("eggs", "store2")] == 1

    def test_solved_problem_from_lp_solution(self):
        solved_problem = solve(self.STORES_2, self.INPUT_2_PURCHASE_CANDIDATES)

        assert solved_problem.num_stores == 2
        assert solved_problem.total_cost == 580

        assert len(solved_problem.trips) == 2

        trip1 = solved_problem.trips[0]
        trip2 = solved_problem.trips[1]

        assert trip1.store == "store1", trip1.store
        assert trip1.location == "123 Main St", trip1.location
        assert trip1.total == 300, trip1.total
        assert len(trip1.items) == 2, len(trip1.items)

        assert trip2.store == "store2", trip2.store
        assert trip2.location == "456 Oak St", trip2.location
        assert trip2.total == 280, trip2.total
        assert len(trip2.items) == 1, len(trip2.items)

    def test_parse_grocery_list_returns_correct_items(self):
        grocery_list = self.INPUT_1
        expected_items = self.INPUT_1_EXPECTED_PARSED_RESULT

        parsed_items = parse_grocery_list(grocery_list)

        assert len(parsed_items) == len(expected_items)
        for i in range(len(parsed_items)):
            assert (
                parsed_items[i].name == expected_items[i].name
            ), f"parsed: {parsed_items[i].name}, expected: {expected_items[i].name}"
            assert (
                parsed_items[i].qty == expected_items[i].qty
            ), f"parsed: {parsed_items[i].qty}, expected: {expected_items[i].qty}"

    def test_parse_qty_string_returns_correct_qty(self):
        self.assertEqual(parse_qty("2lbs Pasta"), (1, "2lbs Pasta"))
        self.assertEqual(parse_qty("1.5kg Apples"), (1, "1.5kg Apples"))
        self.assertEqual(parse_qty("3 cans of beans"), (3, "cans of beans"))
        self.assertEqual(parse_qty("2 bags of chips"), (2, "bags of chips"))
        self.assertEqual(parse_qty("1 dozen eggs"), (1, "dozen eggs"))
        self.assertEqual(parse_qty("4.5 liters of milk"), (1, "4.5 liters of milk"))

    # def test_get_items_returns_correct_candidates(self):
    #     expected_candidates = self.INPUT_2_PURCHASE_CANDIDATES
    #     actual_candidates = get_items(self.INPUT_2_PARSED_RESULT)

    #     self.assertEqual(len(actual_candidates), len(expected_candidates))
    #     for i in range(len(actual_candidates)):
    #         self.assertEqual(
    #             actual_candidates[i].item.qty,
    #             expected_candidates[i].item.qty,
    #             f"parsed: {actual_candidates[i].item.qty}, expected: {expected_candidates[i].item.qty}",
    #         )
    #         self.assertEqual(
    #             actual_candidates[i].store.name,
    #             expected_candidates[i].store.name,
    #             f"parsed: {actual_candidates[i].store.name}, expected: {expected_candidates[i].store.name}",
    #         )

    # def test_find_candidates_returns_correct_candidates(self):
    #     expected_candidates = self.INPUT_2_PURCHASE_CANDIDATES
    #     actual_candidates = find_candidates(self.INPUT_2_PARSED_RESULT[0])

    #     self.assertEqual(len(actual_candidates), len(expected_candidates))
    #     for i in range(len(actual_candidates)):
    #         self.assertEqual(
    #             actual_candidates[i].item.qty,
    #             expected_candidates[i].item.qty,
    #             f"parsed: {actual_candidates[i].item.qty}, expected: {expected_candidates[i].item.qty}",
    #         )
    #         self.assertEqual(
    #             actual_candidates[i].store.name,
    #             expected_candidates[i].store.name,
    #             f"parsed: {actual_candidates[i].store.name}, expected: {expected_candidates[i].store.name}",
    #         )
