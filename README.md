Python Payer API
================

[![Build Status](https://travis-ci.org/dessibelle/python-payer-api.svg?branch=master)](https://travis-ci.org/dessibelle/python-payer-api) [![Coverage Status](https://coveralls.io/repos/dessibelle/python-payer-api/badge.svg?branch=master)](https://coveralls.io/r/dessibelle/python-payer-api?branch=master) [![Latest Version](https://pypip.in/version/python-payer-api/badge.svg?style=flat)](https://pypi.python.org/pypi/python-payer-api/)

Python package for interacting with the [Payer](http://payer.se) payments API.

The scope of this module is basically to serialize the data into XML
ready for transmitting to Payer. Given order details, billing details
and callback URLs it will build an XML tree, encode it according to
the Payer specifications and return the encoded data along with the
required key-value pairs in a dict. Payer expects this data in a
POST request using an `application/x-www-form-urlencoded` content
type.

Generating HTML, providing any type of request handlers or views
needed for a successful payment procedure however, is outside the
scope of this module. Such implementations are encouraged to be
realized as independent modules, in relation to the frameworks, 
webshop modules etc. that you may be using. One such example is
[django-shop-payer-backend](https://github.com/dessibelle/django-shop-payer-backend) for which python-payer-api was
initially developed.

Installation
------------

	pip install python-payer-api

Basic usage
-----------

```python
from payer_api import (
    PAYMENT_METHOD_CARD,
    PAYMENT_METHOD_BANK,
    PAYMENT_METHOD_PHONE,
    PAYMENT_METHOD_INVOICE,
)
from payer_api.postapi import PayerPostAPI
from payer_api.order import (
    PayerProcessingControl,
    PayerBuyerDetails,
    PayerOrderItem,
    PayerOrder,
)

api = PayerPostAPI(
    agent_id="AGENT_ID",
    key_1="6866ef97a972ba3a2c6ff8bb2812981054770162",
    key_2="1388ac756f07b0dda2961436ba8596c7b7995e94",
    payment_methods=[
        PAYMENT_METHOD_CARD,
        PAYMENT_METHOD_BANK,
        PAYMENT_METHOD_PHONE,
        PAYMENT_METHOD_INVOICE,
    ]
)


processing_control = PayerProcessingControl(
    success_redirect_url="http://localhost/webshop/thankyou/",
    authorize_notification_url="http://localhost/webshop/auth/",
    settle_notification_url="http://localhost/webshop/settle/",
    redirect_back_to_shop_url="http://localhost/webshop/",
)

order = PayerOrder(
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

api.set_order(order)
api.set_processing_control(processing_control)

print api.get_post_data()
```

Payment Process
---------------

The main flow of the payment process is as follows:

1. Initialize a `PayerPostAPI` object using the Agent ID, Key 1 and Key 2 values supplied by Payer. Optinally set `test_mode` and `debug_mode` and add a list of `payment_methods`.
1. Create a `PayerProcessingControl` object and add it to your API object using the `set_processing_control()` method. This object holds four URL's that your site has to provide. They are:  
   
    `success_redirect_url`: A "thank you" URL, displayed after completed purchase  
    `authorize_notification_url`: A callback URL, described below, called when orders are authorized.  
    `settle_notification_url`: A callback URL, described below, called when orders are payed.   
    `redirect_back_to_shop_url`: A "cancel" or "back to shop" URL.  
       
1. Create a `PayerOrder` object (including `PayerBuyerDetails` and `PayerOrderItem` objects) and add it to your API object using the `set_order()` method.
1. You can now call `api.get_post_data()` for a dict of the query parameters Payer expects. Add them as `<input type="hidden">` elements  in a `<form>` element with method `POST` and action `api.get_post_url()` and have the user submit the form (i.e. needs to happen client-side).
1. Payer will parse your order, and once the payment has been completed Payer will perform a GET request to your callback URL's - the `authorize_notification_url` URL, and depending on payment method (direct / invoice) call the `settle_notification_url` URL. You will want to implement a view or URL handler that listens on these URL's, for which you call the `validate_callback_ip()` and `validate_callback_url()` methods on PayerPostAPI. A couple of query parameters will be appended to the callback URL's, from which you can extract the Order ID, selected payment method, payment ID etc. The complete list of query paramters are:  
   
`order_id`, `payer_callback_type`, `payer_testmode`, `payer_payment_type`, `payer_added_fee`, `payer_merchant_reference_id`, `payer_payment_id`, `payread_payment_id`.  
   
Depending on the validity of the requests, your views should return either `TRUE` or `FALSE` using a `text/plain` content type.
1. Once Payer has performed its auth and settle validation it will redirect the user the the `success_redirect_url` URL.
