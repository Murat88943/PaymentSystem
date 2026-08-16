from yookassa import Configuration, Refund

from config.config import secret_key, account_id

Configuration.account_id = account_id
Configuration.secret_key = secret_key


def refund_payment(sum, currency, id_operations):
    print(f"пытаемся вернуть: sum={sum}, currency={currency}, payment_id={id_operations}")

    try:
        refund = Refund.create({
            "amount": {
                "value": f"{sum}",
                "currency": f"{currency}"
            },
            "payment_id": f"{id_operations}"
        })
        print(f"возврат успешен: {refund.id}")
        return refund
    except Exception as e:
        print(f"ошибка возврата: {e}")
        return None