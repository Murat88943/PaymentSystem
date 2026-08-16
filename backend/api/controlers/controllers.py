import sys
import os
from typing import Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from backend.api.services.auth_service import register_user, login_user, get_user_profile
from backend.api.services.payment_subscription import (
    create_subscription_service, cancel_subscription_service,
    refund_subscription_service, get_user_subscription_service,
    check_subscription_active
)
from backend.api.services.payment_link_service import create_payment_link_service
from backend.payment.refund_funds import refund_payment
from backend.api.repositories.database import get_payment_by_subscription_id


def handle_register(data: Dict[str, Any]) -> Dict[str, Any]:
    name = data.get('name', '')
    email = data.get('email', '')
    phone = data.get('phone', '')
    password = data.get('password', '')

    return register_user(name, email, phone, password)


def handle_login(data: Dict[str, Any]) -> Dict[str, Any]:
    email = data.get('email', '')
    password = data.get('password', '')

    return login_user(email, password)


def handle_profile(user_id: str) -> Dict[str, Any]:
    user = get_user_profile(user_id)
    if user:
        return {
            'success': True,
            'user': dict(user)
        }
    return {
        'success': False,
        'message': 'пользователь не найден'
    }


def handle_create_subscription(data: Dict[str, Any]) -> Dict[str, Any]:
    user_id = data.get('user_id')
    plan_type = data.get('plan_type')
    price = data.get('price')
    duration_days = data.get('duration_days')

    return create_subscription_service(user_id, plan_type, price, duration_days)


def handle_cancel_subscription(data: Dict[str, Any]) -> Dict[str, Any]:
    subscription_id = data.get('subscription_id')
    return cancel_subscription_service(subscription_id)


def handle_refund_subscription(data: Dict[str, Any]) -> Dict[str, Any]:
    subscription_id = data.get('subscription_id')

    if not subscription_id:
        return {'success': False, 'message': 'subscription_id обязателен'}

    payment = get_payment_by_subscription_id(subscription_id)

    if payment and payment.get('subscription_id'):
        try:
            refund = refund_payment(payment['amount'], 'RUB', payment['subscription_id'])

            if refund:
                result = refund_subscription_service(subscription_id)

                if result.get('success'):
                    return {
                        'success': True,
                        'refund_id': refund.id,
                        'status': refund.status,
                        'message': 'возврат выполнен'
                    }
        except Exception as e:
            print(f'ошибка возврата через юкассу: {e}')

    result = refund_subscription_service(subscription_id)

    if result.get('success'):
        return {'success': True, 'message': 'возврат выполнен'}

    return {'success': False, 'message': 'ошибка возврата'}


def handle_get_subscription(user_id: str) -> Dict[str, Any]:
    subscription = get_user_subscription_service(user_id)
    if subscription:
        return {
            'success': True,
            'subscription': subscription
        }
    return {
        'success': False,
        'message': 'активная подписка не найдена'
    }


def handle_check_subscription(user_id: str) -> Dict[str, Any]:
    return check_subscription_active(user_id)


def handle_create_payment_link(data: Dict[str, Any]) -> Dict[str, Any]:
    user_id = data.get('user_id')
    plan_name = data.get('plan_name')
    amount = data.get('amount')
    currency = data.get('currency', 'RUB')
    return_url = data.get('return_url', 'http://localhost:5173/')
    description = data.get('description', '')

    if not user_id:
        return {'success': False, 'message': 'user_id обязателен'}

    if not plan_name:
        return {'success': False, 'message': 'plan_name обязателен'}

    if not amount or amount <= 0:
        return {'success': False, 'message': 'сумма должна быть больше 0'}

    return create_payment_link_service(
        user_id=user_id,
        plan_name=plan_name,
        amount=amount,
        currency=currency,
        return_url=return_url,
        description=description
    )


def handle_refund_subscription(data: Dict[str, Any]) -> Dict[str, Any]:
    subscription_id = data.get('subscription_id')

    if not subscription_id:
        return {'success': False, 'message': 'subscription_id обязателен'}

    payment = get_payment_by_subscription_id(subscription_id)
    print(f"subscription_id: {subscription_id}")
    print(f"payment: {payment}")

    if payment and payment.get('payment_id'):
        print(f"payment_id из бд: {payment['payment_id']}")
        try:
            refund = refund_payment(payment['amount'], 'RUB', payment['payment_id'])

            if refund:
                result = refund_subscription_service(subscription_id)

                if result.get('success'):
                    return {
                        'success': True,
                        'refund_id': refund.id,
                        'status': refund.status,
                        'message': 'возврат выполнен'
                    }
        except Exception as e:
            print(f'ошибка возврата через юкассу: {e}')

    result = refund_subscription_service(subscription_id)

    if result.get('success'):
        return {'success': True, 'message': 'возврат выполнен'}

    return {'success': False, 'message': 'ошибка возврата'}

def handle_refund_payment(data: Dict[str, Any]) -> Dict[str, Any]:
    payment_id = data.get('payment_id')
    amount = data.get('amount')
    currency = data.get('currency', 'RUB')

    if not payment_id:
        return {'success': False, 'message': 'payment_id обязателен'}

    if not amount or amount <= 0:
        return {'success': False, 'message': 'сумма должна быть больше 0'}

    refund = refund_payment(amount, currency, payment_id)

    if refund:
        return {
            'success': True,
            'refund_id': refund.id,
            'status': refund.status,
            'message': 'возврат выполнен'
        }

    return {'success': False, 'message': 'ошибка возврата средств'}