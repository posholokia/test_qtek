"""
Сюда импортируем declarative base и orm модели, чтобы их видел alembic.
Base нужно импортировать отсюда в env.py
"""
from src.apps.account.models import UserModel

from .db import Base
