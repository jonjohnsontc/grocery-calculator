import logging
import logging.handlers
import unittest
import unittest.mock

from grocery_calculator.ingest.stores.target import TargetIngest


class TestTargetIngest(unittest.TestCase):

    def test_tag_items_tags_the_items_passed_through(self):
        TEST_TAGGED_ITEM = {
            "product_name": "test value",
            "product_type": "Ice Cream",
            "flavor_or_variant": "Vanilla",
            "size": "20oz",
            "packaging_type": "blank",
            "sale": False,
            "sale_value": None,
            "tags": ["Ice Cream", "Frozen", "Fruit Cake"],
        }

        ti = TargetIngest()
        ti._tag_item = unittest.mock.MagicMock(return_value=TEST_TAGGED_ITEM)
        logger = logging.getLogger()
        logger.addHandler(logging.NullHandler())
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
        tagged = ti.tag_items(items)
        self.assertEqual(len(tagged), 3)
        logger.removeHandler(logger.handlers[0])
