import sys
import os
from typing import Dict, Any, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.api.repositories.database import (
    create_user,
    get_user_by_email,
    get_user_by_token,
    update_user_token,
    get_user_by_id,
    validate_email,
    verify_password,
    init_database
)


def register_user(name: str, email: str, phone: str, password: str) -> Dict[str, Any]:
    init_database()

    if not name or len(name.strip()) < 2:
        return {
            'success': False,
            'message': 'имя должно содержать минимум 2 символа'
        }

    if not validate_email(email):
        return {
            'success': False,
            'message': 'неверный формат email'
        }

    if len(password) < 6:
        return {
            'success': False,
            'message': 'пароль должен содержать минимум 6 символов'
        }

    existing_user = get_user_by_email(email)
    if existing_user:
        return {
            'success': False,
            'message': 'пользователь с таким email уже существует'
        }

    user = create_user(name, email, phone, password)

    if user:
        return {
            'success': True,
            'message': 'регистрация успешна',
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'phone': user['phone'],
                'token': user['token'],
                'created_at': user['created_at']
            }
        }
    else:
        return {
            'success': False,
            'message': 'ошибка сохранения пользователя'
        }


def login_user(email: str, password: str) -> Dict[str, Any]:
    init_database()

    if not email or not password:
        return {
            'success': False,
            'message': 'email и пароль обязательны'
        }

    user = get_user_by_email(email)
    if not user:
        return {
            'success': False,
            'message': 'пользователь не найден'
        }

    if not verify_password(password, user['password']):
        return {
            'success': False,
            'message': 'неверный пароль'
        }

    new_token = update_user_token(user['id'])

    if new_token:
        return {
            'success': True,
            'message': 'вход выполнен',
            'token': new_token,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'phone': user['phone']
            }
        }
    else:
        return {
            'success': False,
            'message': 'ошибка обновления токена'
        }


def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    init_database()
    return get_user_by_id(user_id)


def get_user_by_token_service(token: str) -> Optional[Dict[str, Any]]:
    init_database()
    return get_user_by_token(token)