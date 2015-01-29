VERSION = '0.1.0'

DEBUG_MODE_BRIEF = "brief"
DEBUG_MODE_SILENT = "silent"
DEBUG_MODE_VERBOSE = "verbose"

PAYMENT_METHOD_CARD = "card"
PAYMENT_METHOD_BANK = "bank"
PAYMENT_METHOD_PHONE = "phone"
PAYMENT_METHOD_INVOICE = "invoice"


IP_WHITELIST = [
    "192.168.100.1",
    "192.168.100.20",
    "79.136.103.5",
    "94.140.57.180",
    "94.140.57.181",
    "94.140.57.184",
]

IP_BLACKLIST = []


class PayerIPNotOnWhitelistException(Exception):
    pass

class PayerIPBlacklistedException(Exception):
    pass

class PayerURLValidationError(Exception):
    pass
