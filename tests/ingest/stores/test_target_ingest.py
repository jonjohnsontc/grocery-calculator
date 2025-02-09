import unittest
import unittest.mock

from tests import FIXTURES_DIR
from grocery_calculator.ingest.stores.target import TargetIngest


class TestTargetIngest(unittest.TestCase):

    def test_tag_items_tags_the_items_passed_through(self):
        TEST_TAGGED_ITEM = (
            "test value",
            "Ice Cream",
            "Vanilla",
            "20oz",
            False,
            None,
            ["Ice Cream", "Frozen", "Fruit Cake"],
        )

        ti = TargetIngest()
        ti._tag_item = unittest.mock.MagicMock(return_value=TEST_TAGGED_ITEM)

        items = [
            (
                1,
                "favorite day | blueberry streusel muffins - 4ct/14oz - favorite day™ |",
            ),
            (
                2,
                "once upon a farm | save 15% in cart on select once upon a farm foods | once upon a farm strawberry banana swirl organic dairy-free kids' smoothie - 4ct/4oz pouches",
            ),
            (
                3,
                "daily harvest | daily harvest frozen banana and almond smoothie - 7.4oz |",
            ),
        ]
        tagged = []
        for chunks in ti.tag_items(items, chunk_size=3):
            tagged.extend(chunks)
        self.assertEqual(len(tagged), 3)
