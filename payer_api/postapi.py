# -*- coding: utf-8 -*-
from . import VERSION
import base64
import hashlib
from xml import PayerXMLDocument


class PayerPostAPIError(Exception):

    ERROR_MISSING_AGENT_ID = 100
    ERROR_MISSING_KEY_1 = 101
    ERROR_MISSING_KEY_2 = 102
    ERROR_MISSING_ORDER = 200
    ERROR_MISSING_PROCESSING_CONTROL = 300
    ERROR_XML_ERROR = 400

    ERROR_MESSAGES = {
        ERROR_MISSING_AGENT_ID: "Agent ID not set.",
        ERROR_MISSING_KEY_1: "Key 1 not set.",
        ERROR_MISSING_KEY_2: "Key 2 not set.",
        ERROR_MISSING_ORDER: "Order not set.",
        ERROR_MISSING_PROCESSING_CONTROL: "Processing control not set.",
        ERROR_XML_ERROR: "There was an error while generating XML data.",
    }

    def __init__(self, code):
            self.code = code

    def __str__(self):
        return repr("Error %s: %s" % (self.code, self.ERROR_MESSAGES.get(self.code, "Unknown Error")))


class PayerPostAPI(object):

    PAYER_POST_URL = "https://secure.payer.se/PostAPI_V1/InitPayFlow"
    API_VERSION = "Python_Payer_API_%s" % PYTHON_PAYER_API_VERSION

    def __init__(self, agent_id, key_1, key_2, processing_control, *args, **kwargs):

        self.agent_id = agent_id
        self.key_1 = key_1
        self.key_2 = key_2

        self.payment_methods = []
        self.encoding = kwargs.get('encoding', "utf-8")
        self.currency = kwargs.get('currency', "SEK")

        self.xml_document = None

        self.set_order(kwargs.get('order', None))
        self.set_processing_control(processing_control)


    def set_order(self, order):
        self.order = order

        self._generate_xml()

    def set_processing_control(self, processing_control):
        self.processing_control = processing_control

        self._generate_xml()

    def get_post_url(self):
        return self.PAYER_POST_URL

    def get_agent_id(self):
        return self.agent_id

    def get_api_version(self):
        return self.API_VERSION

    def get_encoding(self):
        return self.encoding

    def get_checksum(self, b64_encoded_xml=None):
        if not b64_encoded_xml:
            b64_encoded_xml = get_base64_data()

        if not self.key_1:
            raise PayerPostAPIError(PayerPostAPIError.ERROR_MISSING_KEY_1)

        if not self.key_2:
            raise PayerPostAPIError(PayerPostAPIError.ERROR_MISSING_KEY_2)

        return hashlib.md5(self.key_1 + b64_encoded_xml + self.key_2).hexdigest()

    def _generate_xml(self):

        if self.order and self.processing_control:

            if not self.agent_id:
                raise PayerPostAPIError(PayerPostAPIError.ERROR_MISSING_AGENT_ID)

            self.xml_document = PayerXMLDocument(
                agent_id=self.get_agent_id(),
                order=self.order,
                processing_control=self.processing_control,
                debug_mode=PayerXMLDocument.DEBUG_MODE_VERBOSE,
                test_mode=True,
            )

    def get_xml_data(self, *args, **kwargs):

        if not self.xml_document:
            self._generate_xml()

        if not self.order:
            raise PayerPostAPIError(PayerPostAPIError.ERROR_MISSING_ORDER)

        if not self.processing_control:
            raise PayerPostAPIError(PayerPostAPIError.ERROR_MISSING_PROCESSING_CONTROL)

        if not self.xml_document:
            raise PayerPostAPIError(PayerPostAPIError.ERROR_XML_ERROR)

        return self.xml_document.tostring(*args, **kwargs)

    def get_base64_data(self, xml_data=None, *args, **kwargs):
        if not xml_data:
            xml_data = self.get_xml_data(*args, **kwargs)

        return base64.b64encode(xml_data)

    def get_post_data(self):
        base64_data = self.get_base64_data()

        return {
            'payer_agentid': self.get_agent_id(),
            'payer_xml_writer': self.get_api_version(),
            'payer_data': base64_data,
            'payer_checksum': self.get_checksum(base64_data),
            'payer_charset': self.get_encoding(),
        }
