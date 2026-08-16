import uuid
from yookassa import Configuration, Payment
from config.config import secret_key, account_id


Configuration.account_id = account_id
Configuration.secret_key = secret_key


def create_payment(currency, sum, description, return_url):
    payment = Payment.create({
        "amount": {
            "value": f"{sum}",
            "currency": f"{currency}"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"{return_url}"
        },
        "capture": True,
        "description": f"{description}"
    }, uuid.uuid4())

    payment_url = payment.confirmation.confirmation_url
    print(f"ссылка для оплаты счета: {payment_url}")

    return payment