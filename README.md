Python package for interacting with the [Payer](http://payer.se) API.


Installation
============

	pip install payer-api

Basic usage
===========

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
