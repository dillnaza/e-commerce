from typing import Protocol, OrderedDict

from rest_framework.generics import get_object_or_404

from . import models


class UserReposInterface(Protocol):
    def create_user(self, data: OrderedDict) -> models.User:         ...

    def get_user(self, data: OrderedDict) -> models.User:    ...


class UserRepositoriesV1:
    model = models.User

    def create_user(self, data: OrderedDict) -> models.User:
        return self.model.objects.create_user(**data)

    def get_user(self, data: OrderedDict) -> models.User:
        return get_object_or_404(self.model, **data)
