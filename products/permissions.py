from rest_framework.permissions import DjangoObjectPermissions
from . import models

class IsUser(DjangoObjectPermissions):
    def has_object_permission(self, request, view, obj:models.Product):
        return obj.user==request.user