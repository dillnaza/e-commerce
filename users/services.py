import logging
import random
import uuid
from typing import Protocol, OrderedDict
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt import tokens
from . import repos, models

logger = logging.getLogger(__name__)


class UserServicesInterface(Protocol):

    def create_user(self, data: OrderedDict) -> dict: ...

    def verify_user(self, data: OrderedDict) -> models.User | None: ...

    def create_token(self, data: OrderedDict) -> dict: ...

    def verify_token(self, data: OrderedDict) -> dict: ...


class UserServicesV1:
    user_repos: repos.UserReposInterface = repos.UserRepositoriesV1()

    def create_user(self, data: OrderedDict) -> dict:
        session_id = self._verify_phone_number(data=data)
        return {
            'session_id': session_id,
        }

    def verify_user(self, data: OrderedDict) -> models.User | None:
        user_data = cache.get(data['session_id'])
        if not user_data:
            raise ValidationError
        if data['code'] != user_data['code']:
            raise ValidationError
        user = self.user_repos.create_user(data={
            'email': user_data['email'],
            'phone_number': user_data['phone_number'],
        })
        return user

    def create_token(self, data: OrderedDict) -> dict:
        session_id = self._verify_phone_number(data=data, is_exist=True)
        return {
            'session_id': session_id,
        }

    def verify_token(self, data: OrderedDict) -> dict:
        session = cache.get(data['session_id'])
        if not session:
            raise ValidationError
        if session['code'] != data['code']:
            raise ValidationError
        user = self.user_repos.get_user(data={'phone_number': session['phone_number']})
        access = tokens.AccessToken.for_user(user=user)
        refresh = tokens.RefreshToken.for_user(user=user)
        return {
            'access': str(access),
            'refresh': str(refresh),
        }

    def _verify_phone_number(self, data: OrderedDict, is_exist: bool = False) -> str:
        phone_number = data['phone_number']
        if is_exist:
            user = self.user_repos.get_user(data)
            phone_number = str(user.phone_number)
        code = self._generate_code()
        session_id = self._generate_session_id()
        cache.set(session_id, {'phone_number': phone_number, 'code': code, **data}, timeout=300)
        self._send_sms_to_phone_number(phone_number=data['phone_number'], code=code)
        return session_id

    @staticmethod
    def _send_sms_to_phone_number(phone_number: str, code: str) -> None:
        print(f'send sms code {code} to {phone_number}')


    @staticmethod
    def _generate_code(length: int = 4) -> str:
        numbers = [str(i) for i in range(10)]
        return ''.join(random.choices(numbers, k=length))

    @staticmethod
    def _generate_session_id() -> str:
        return str(uuid.uuid4())
