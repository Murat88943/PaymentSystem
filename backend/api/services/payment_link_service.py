import uuid
import sys
import os
from typing import Dict, Any
from yookassa import Configuration, Payment

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from config.config import secret_key, account_id
from backend.api.repositories.database import create_payment, get_user_by_id, create_subscription, \
    update_payment_subscription


Configuration.account_id = account_id
Configuration.secret_key = secret_key


def create_payment_link_service(
        user_id: str,
        plan_name: str,
        amount: float,
        currency: str = "RUB",
        return_url: str = "http://localhost:5173/",
        description: str = ""
) -> Dict[str, Any]:
    try:
        user = get_user_by_id(user_id)
        if not user:
            return {'success': False, 'message': 'пользователь не найден'}

        idempotence_key = str(uuid.uuid4())

        payment = Payment.create({
            "amount": {
                "value": f"{amount:.2f}",
                "currency": currency
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url
            },
            "capture": True,
            "description": description or f"оплата тарифа {plan_name}",
            "metadata": {
                "user_id": user_id,
                "plan_name": plan_name
            }
        }, idempotence_key)

        payment_url = payment.confirmation.confirmation_url
        payment_id = payment.id

        subscription = create_subscription(user_id, plan_name, amount, 30)

        payment_record = create_payment(
            user_id=user_id,
            subscription_id=subscription['id'] if subscription else None,
            amount=amount,
            payment_method='yookassa'
        )

        if payment_record:
            update_payment_subscription(payment_record['id'], payment_id)

        return {
            'success': True,
            'payment_id': payment_id,
            'payment_url': payment_url,
            'subscription': subscription,
            'message': 'ссылка для оплаты создана'
        }

    except Exception as e:
        return {'success': False, 'message': f'ошибка создания платежа: {str(e)}'}


def check_payment_status(payment_id: str) -> Dict[str, Any]:
    try:
        payment = Payment.find_one(payment_id)

        return {
            'success': True,
            'payment_id': payment.id,
            'status': payment.status,
            'paid': payment.paid,
            'amount': {
                'value': payment.amount.value,
                'currency': payment.amount.currency
            },
            'created_at': payment.created_at,
            'metadata': payment.metadata if hasattr(payment, 'metadata') else None
        }
    except Exception as e:
        return {'success': False, 'message': f'ошибка проверки платежа: {str(e)}'}


def capture_payment(payment_id: str) -> Dict[str, Any]:
    try:
        payment = Payment.find_one(payment_id)
        if payment.status == 'waiting_for_capture':
            payment = Payment.capture(payment_id)

        return {
            'success': True,
            'payment_id': payment.id,
            'status': payment.status,
            'paid': payment.paid
        }
    except Exception as e:
        return {'success': False, 'message': f'ошибка подтверждения платежа: {str(e)}'}


def cancel_payment(payment_id: str) -> Dict[str, Any]:
    try:
        payment = Payment.cancel(payment_id)

        return {
            'success': True,
            'payment_id': payment.id,
            'status': payment.status
        }
    except Exception as e:
        return {'success': False, 'message': f'ошибка отмены платежа: {str(e)}'}