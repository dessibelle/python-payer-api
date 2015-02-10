import unittest
from payer_api.tests import TestCase
from payer_api.order import (
    PayerOrder,
    PayerBuyerDetails,
    PayerOrderItem,
)


class TestOrder(TestCase):

    def setUp(self):
        self.order = PayerOrder(order_id="123456")

        self.buyer_details = PayerBuyerDetails(
            first_name="John",
            last_name="Doe",
            address_line_1="1234 Main Street",
            postal_code="12345",
            city="Anywhere",
            phone_mobile="012345678",
            email="john.doe@host.com",
        )

        self.order_items = [
            PayerOrderItem(
                description='A product',
                price_including_vat=123.50,
                vat_percentage=25,
                quantity=4,
            ),
            PayerOrderItem(
                description='Another product',
                price_including_vat=123.0,
                vat_percentage=12.5,
                quantity=2,
            ),
        ]

        self.info_lines = [
            "Shipping with 5 work days",
            "Additional line of order info",
        ]

    def test_add_order_item(self):
        for order_item in self.order_items:
            self.order.add_order_item(order_item)
            self.assertTrue(order_item in self.order.order_items)

        self.assertEqual(self.order.order_items, self.order_items)

    def test_add_info_line(self):
        for info_line in self.info_lines:
            self.order.add_info_line(info_line)
            self.assertTrue(info_line in self.order.info_lines)

        self.assertEqual(self.order.info_lines, self.info_lines)

    def test_set_buyer_details(self):
        self.order.set_buyer_details(self.buyer_details)
        self.assertEqual(self.order.buyer_details, self.buyer_details)

if __name__ == '__main__':
    unittest.main()
