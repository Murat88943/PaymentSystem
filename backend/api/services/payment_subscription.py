import sys
import os
from typing import Dict, Any, Optional
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from backend.api.repositories.database import (
    create_subscription,
    get_user_subscription,
    cancel_subscription,
    refund_subscription
)


def create_subscription_service(user_id: str, plan_type: str, price: float, duration_days: int) -> Dict[str, Any]:
    if not user_id:
        return {'success': False, 'message': 'user_id обязателен'}

    if not plan_type:
        return {'success': False, 'message': 'plan_type обязателен'}

    if price <= 0:
        return {'success': False, 'message': 'цена должна быть больше 0'}

    if duration_days <= 0:
        return {'success': False, 'message': 'длительность должна быть больше 0'}

    subscription = create_subscription(user_id, plan_type, price, duration_days)

    if subscription:
        return {
            'success': True,
            'message': 'подписка создана',
            'subscription': subscription
        }

    return {'success': False, 'message': 'ошибка создания подписки'}


def cancel_subscription_service(subscription_id: str) -> Dict[str, Any]:
    if not subscription_id:
        return {'success': False, 'message': 'subscription_id обязателен'}

    result = cancel_subscription(subscription_id)

    if result:
        return {'success': True, 'message': 'подписка отменена'}

    return {'success': False, 'message': 'ошибка отмены подписки'}


def refund_subscription_service(subscription_id: str) -> Dict[str, Any]:
    if not subscription_id:
        return {'success': False, 'message': 'subscription_id обязателен'}

    result = refund_subscription(subscription_id)

    if result:
        return {'success': True, 'message': 'возврат выполнен'}

    return {'success': False, 'message': 'ошибка возврата'}


def get_user_subscription_service(user_id: str) -> Optional[Dict[str, Any]]:
    if not user_id:
        return None

    return get_user_subscription(user_id)


def check_subscription_active(user_id: str) -> Dict[str, Any]:
    if not user_id:
        return {'success': False, 'active': False, 'message': 'user_id обязателен'}

    subscription = get_user_subscription(user_id)

    if not subscription:
        return {'success': True, 'active': False, 'message': 'подписка не найдена'}

    end_date = subscription.get('end_date')
    if end_date:
        end_datetime = datetime.fromisoformat(end_date)
        if end_datetime > datetime.now():
            return {
                'success': True,
                'active': True,
                'subscription': subscription
            }

    return {'success': True, 'active': False, 'message': 'подписка истекла'}