import unittest
import urlparse
from payer_api.tests import TestCase
from payer_api.xml import PayerXMLDocument
from payer_api.order import (
    PayerProcessingControl,
    PayerOrder,
    PayerBuyerDetails,
    PayerOrderItem,
)
from payer_api import (
    DEBUG_MODE_BRIEF,
    DEBUG_MODE_SILENT,
    DEBUG_MODE_VERBOSE,
    PAYMENT_METHOD_CARD,
    PAYMENT_METHOD_BANK,
    PAYMENT_METHOD_PHONE,
    PAYMENT_METHOD_INVOICE,
)
from lxml import etree


class XMLTestCase(TestCase):

    def setUp(self):

        self.order = self.getOrder()
        self.processing_control = self.getProcessingControl()

        kwargs = {
            'agent_id': 'AGENT_ID',
            'order': self.order,
            'processing_control': self.processing_control,
        }
        self.xml_document = PayerXMLDocument(**kwargs)

    def getOrder(self):
        return PayerOrder(
            order_id="123456",
            buyer_details=PayerBuyerDetails(
                first_name="John",
                last_name="Doe",
                address_line_1="1234 Main Street",
                postal_code="12345",
                city="Anywhere",
                phone_mobile="012345678",
                email="john.doe@host.com",
            ),
            order_items=[
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
            ],
            info_lines=[
                "Shipping with 5 work days",
                "Additional line of order info",
            ]
        )

    def getProcessingControl(self):
        return PayerProcessingControl(
            success_redirect_url="http://localhost/webshop/thankyou/",
            authorize_notification_url="http://localhost/webshop/auth/",
            settle_notification_url="http://localhost/webshop/settle/",
            redirect_back_to_shop_url="http://localhost/webshop/",
        )

    def test_settings(self):

        # Default settings
        self.assertEqual(self.xml_document.agent_id, "AGENT_ID")
        self.assertEqual(self.xml_document.debug_mode, "silent")
        self.assertEqual(self.xml_document.test_mode, False)
        self.assertEqual(self.xml_document.message, None)
        self.assertEqual(self.xml_document.hide_details, False)
        self.assertEqual(self.xml_document.language, "sv")
        self.assertEqual(self.xml_document.currency, "SEK")
        self.assertEqual(self.xml_document.payment_methods, [
            PAYMENT_METHOD_CARD,
            PAYMENT_METHOD_BANK,
            PAYMENT_METHOD_PHONE,
            PAYMENT_METHOD_INVOICE,
        ])
        self.assertEqual(self.xml_document.order, self.order)

        self.assertEqual(
            self.xml_document.success_redirect_url,
            self.processing_control.success_redirect_url)
        self.assertEqual(
            self.xml_document.authorize_notification_url,
            self.processing_control.authorize_notification_url)
        self.assertEqual(
            self.xml_document.settle_notification_url,
            self.processing_control.settle_notification_url)
        self.assertEqual(
            self.xml_document.redirect_back_to_shop_url,
            self.processing_control.redirect_back_to_shop_url)

        # Modified settings
        self.xml_document.debug_mode = DEBUG_MODE_BRIEF
        self.assertEqual(self.xml_document.debug_mode, "brief")

        self.xml_document.debug_mode = DEBUG_MODE_SILENT
        self.assertEqual(self.xml_document.debug_mode, "silent")

        self.xml_document.debug_mode = DEBUG_MODE_VERBOSE
        self.assertEqual(self.xml_document.debug_mode, "verbose")

        self.xml_document.currency = "NOK"
        self.assertEqual(self.xml_document.currency, "NOK")

        self.xml_document.language = "no"
        self.assertEqual(self.xml_document.language, "no")

    def test_urls(self):
        self.assertEqual(
            self.xml_document.get_success_redirect_url(),
            self.processing_control.success_redirect_url)
        self.assertEqual(
            self.xml_document.get_authorize_notification_url(
                self.order.order_id),
            self.processing_control.authorize_notification_url +
            "?order_id=123456")
        self.assertEqual(
            self.xml_document.get_settle_notification_url(
                self.order.order_id),
            self.processing_control.settle_notification_url +
            "?order_id=123456")
        self.assertEqual(
            self.xml_document.get_redirect_back_to_shop_url(),
            self.processing_control.redirect_back_to_shop_url)

        self.assertEqual(
            self.xml_document.get_authorize_notification_url(),
            self.processing_control.authorize_notification_url +
            "?order_id=")
        self.assertEqual(
            self.xml_document.get_settle_notification_url(),
            self.processing_control.settle_notification_url +
            "?order_id=")

        self.assertEqual(
            self.xml_document._add_params_to_url(
                self.processing_control.settle_notification_url, {}),
            self.processing_control.settle_notification_url)

        url = self.xml_document._add_params_to_url(
            self.processing_control.settle_notification_url, {
                'order_id': '123',
                'data': 'true',
                'empty': '',
            })

        url_parts = list(urlparse.urlparse(url))
        params = dict(urlparse.parse_qsl(url_parts[4], keep_blank_values=True))

        self.assertEqual(
            set(params.keys()),
            set(['order_id', 'data', 'empty']))

        url = self.xml_document._add_params_to_url(
            "https://www.host.com/path/handler.php?foo=bar", {
                'order_id': '123',
                'data': 'true',
                'empty': '',
            })

        url_parts = list(urlparse.urlparse(url))
        params = dict(urlparse.parse_qsl(url_parts[4], keep_blank_values=True))

        self.assertEqual(
            set(params.keys()),
            set(['foo', 'order_id', 'data', 'empty']))

        self.xml_document.ORDER_ID_URL_PARAMETER_NAME = "oid"

        self.assertEqual(
            self.xml_document.get_settle_notification_url(
                self.order.order_id),
            self.processing_control.settle_notification_url +
            "?oid=123456")

    def test_xml(self):
        xml = self.xml_document.tostring()
        self.assertEqual(xml, str(self.xml_document))

        try:
            parser = etree.XMLParser(dtd_validation=False)
            root = etree.fromstring(xml, parser)
            if root is None:
                raise Exception("No XML data")
        except Exception as e:
            raise e

        def missing_dtd():
            parser = etree.XMLParser(dtd_validation=True)
            root = etree.fromstring(xml, parser)
            assert root

        def malformed_xml():
            parser = etree.XMLParser(dtd_validation=False)
            root = etree.fromstring(xml + "malformed xml", parser)
            assert root

        self.assertRaises(etree.XMLSyntaxError, missing_dtd)
        self.assertRaises(etree.XMLSyntaxError, malformed_xml)

        xml = self.xml_document.tostring()
        root = etree.fromstring(xml)

        currency = root.xpath("/payread_post_api_0_2/purchase/currency/text()")
        self.assertEqual(currency[0], 'SEK')

        message = root.xpath("/payread_post_api_0_2/purchase/message")
        self.assertEqual(message, [])

        self.xml_document.message = "Foo bar"
        xml = self.xml_document.tostring(rebuild_tree=True)
        root = etree.fromstring(xml)

        message = root.xpath("/payread_post_api_0_2/purchase/message/text()")
        self.assertEqual(message[0], "Foo bar")

        payment_methods = root.xpath(
            "/payread_post_api_0_2/database_overrides" +
            "/accepted_payment_methods/payment_method/text()")
        self.assertEqual(
            set(payment_methods),
            set(self.xml_document.payment_methods))

        self.xml_document.payment_methods = []
        xml = self.xml_document.tostring(rebuild_tree=True)
        root = etree.fromstring(xml)
        payment_methods = root.xpath(
            "/payread_post_api_0_2/database_overrides" +
            "/accepted_payment_methods")
        self.assertEqual(payment_methods, [])

if __name__ == '__main__':
    unittest.main()
