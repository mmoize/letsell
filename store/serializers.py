from rest_framework import serializers

from store.models import (
    Category,
    Product,
    PaymentMethod,
    PurchaseOrder,
    PurchaseItem
)


class CategorySerializer(serializers.ModelSerializer):
    """ Serializer for the Category model """

    class Meta:
        """ CategorySerializer's Meta class """

        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """ Serializer for the Product model """

    class Meta:
        """ ProductSerializer's Meta class """

        model = Product
        exclude = ('slug', )


class PaymentMethodSerializer(serializers.ModelSerializer):
    """ Serializer for the PaymentMethod model """

    class Meta:
        """ PaymentMethodSerializer's Meta class """

        model = PaymentMethod
        fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """ Serializer for the PurchaseOrder model """

    class Meta:
        """ PurchaseOrderSerializer's Meta class """

        model = PurchaseOrder
        fields = '__all__'


class PurchaseItemSerializer(serializers.ModelSerializer):
    """ Serializer for the PurchaseItem model """

    class Meta:
        """ PurchaseItemSerializer's Meta class """

        model = PurchaseItem
        fields = '__all__'