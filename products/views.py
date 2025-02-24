from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from utils import mixins
from . import serializers, models, permissions


class ProductImageViewSet(ModelViewSet):
    serializer_class = serializers.ProductImageSerializer
    queryset = models.ProductImage.objects.all()


class ProductViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'retrieve': serializers.RetrieveProductSerializer,
    }
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()

    def get_permissions(self):
        if self.action in ['retrieve', 'list', ]:
            return IsAuthenticated(),

        return permissions.IsUser(),
