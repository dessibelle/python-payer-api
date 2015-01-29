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
django-shop-payer-backend for which python-payer-api was
initially developed.

Installation
============

	pip install python-payer-api

Basic usage
===========

```python
from payer_api.order import (
    PayerProcessingControl,
    PayerBuyerDetails,
    PayerOrderItem,
    PayerOrder,
)

processing_control = PayerProcessingControl(
    success_redirect_url="http://localhost/webshop/success/",
    authorize_notification_url="http://localhost/webshop/auth/",
    settle_notification_url="http://localhost/webshop/settle/",
    redirect_back_to_shop_url="http://localhost/webshop/shop/",
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

api = PayerPostAPI(
    agent_id="AGENT_ID",
    key_1="6866ef97a972ba3a2c6ff8bb2812981054770162",
    key_2="1388ac756f07b0dda2961436ba8596c7b7995e94",
    processing_control=processing_control,
)

api.set_order(order)

print api.get_post_data()
```
