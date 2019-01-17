from rest_framework_elasticsearch.es_serializer import ElasticModelSerializer
from .models import Product, Category, Order
from .documents import ProductIndex
from rest_framework import serializers


class ProductIndexSerializer(ElasticModelSerializer):
    image_thumbnail = serializers.ImageField('image_thumbnail')

    class Meta:
        model = Product
        es_model = ProductIndex
        fields = ('pk', 'name', 'slug', 'image', 'image_thumbnail', 'description', 'price',
                  'stock', 'available', 'created', 'updated')


# class RecursiveField(serializers.Serializer):
#
#     def to_native(self, value):
#         return CategorySerializer(value, context={"parent": self.parent.object, "parent_serializer": self.parent})


# class ProductListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ('id', 'name', 'slug', 'image', 'price')


class CategoryWithCountSerializer(serializers.ModelSerializer):
    group_count = serializers.ReadOnlyField(source='get_group_count')

    class Meta:
        model = Category
        fields = ('name', 'slug', 'group_count')


class CategoryWithImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField('image')

    class Meta:
        model = Category
        fields = ('name', 'slug', 'image')


class CategoryOverviewSerializer(serializers.ModelSerializer):
    children = CategoryWithCountSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'children')


class CategoryMinimum(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class SubCategorySerializer(serializers.ModelSerializer):
    children = CategoryWithImageSerializer(many=True, required=False)
    path = CategoryMinimum(many=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'children', 'path')


class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class ProductListSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ImageField('image_thumbnail')

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'image_thumbnail', 'price', 'description')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'image', 'description', 'price', 'available')


class ProductCartSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ImageField('image_thumbnail')

    class Meta:
        model = Product
        fields = ('id', 'name', 'image_thumbnail', 'price', 'available')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city', 'paid', 'items', 'get_total_cost')


class LastAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'first_name', 'last_name', 'email', 'city', 'address',
                  'postal_code')
