from elasticsearch import Elasticsearch, RequestsHttpConnection
from rest_framework_elasticsearch import es_views, es_filters, es_pagination
from .documents import ProductIndex
from rest_framework import generics
from .serializers import CategoryOverviewSerializer, SubCategorySerializer,\
    MenuCategorySerializer, ProductListSerializer, ProductSerializer,\
    ProductCartSerializer, OrderSerializer, LastAddressSerializer
from .models import Product, Category, Order, OrderItem, UserProfile
from rest_framework import status
from rest_framework.response import Response
import json
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
import uuid
from rest_framework.permissions import AllowAny, IsAuthenticated


# 'api/check-token/' Return User's first_name, if user authenticated
# if this is superuser( his firt_name may be empty), return first_name 'Admin'
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def check_token(request):
    if request.user.is_superuser and len(request.user.first_name) < 1:
        return JsonResponse({'firstName': 'Admin'})
    else:
        return JsonResponse({'firstName': request.user.first_name})


# 'api/verify-user?uuid=' verifies user by uuid if found and return HTTP_200_OK
# user becomes active, uuid changes too
# else return error in data and HTTP_400_BAD_REQUEST
@api_view(['GET'])
@permission_classes((AllowAny, ))
def verify_user(request):
    request_uuid = request.query_params.get('uuid', None)
    response_data = {}
    try:
        user_profile = UserProfile.objects.get(uuid=request_uuid)
        user_profile.uuid = uuid.uuid4()
        user_profile.user.is_active = True
        user_profile.user.save()
        user_profile.save()
        response_status = status.HTTP_200_OK
    except Exception as e:
        response_status = status.HTTP_400_BAD_REQUEST
        response_data['error'] = str(e)
    return Response(response_data, status=response_status)


# 'api/verify-order' verifies order by uuid if found and return HTTP_200_OK,
# order changes status on 'REQUIRES_ATTENTION', uuid changes too,
# else return error in data and HTTP_400_BAD_REQUEST
@api_view(['GET'])
@permission_classes((AllowAny, ))
def verify_order(request):
    request_uuid = request.query_params.get('uuid', None)
    response_data = {}
    try:
        order = Order.objects.get(uuid=request_uuid)
        order.uuid = uuid.uuid4()
        order.status = Order.REQUIRES_ATTENTION
        order.save()
        response_status = status.HTTP_200_OK
    except Exception as e:
        response_status = status.HTTP_400_BAD_REQUEST
        response_data['error'] = str(e)
    return Response(response_data, status=response_status)


# create a new user at 'api/add-user' by first_name, username and password
# (создать нового пользователя по адресу api/add-user по first_name, username и password)
class NewUserSet(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = json.loads(self.request.body)
        response_data = {}
        try:
            user = User.objects.create_user(
                username=data['username'],
                first_name=data['first_name'],
                password=data['password'],
                is_active=False)
            response_status = status.HTTP_200_OK
        except Exception as e:
            response_data['error'] = str(e)
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(response_data, status=response_status)


# /r'^api/list$' Elasticsearch, it looks like
# http://example.com/blogs/api/list?search=elasticsearch
# http://example.com/blogs/api/list?tag=opensource
# http://example.com/blogs/api/list?tag=opensource,aws
# http://example.com/blogs/api/list?to_created_at=2020-10-01&from_created_at=2017-09-01
# we use ?search= in our FRONTEND
class ProductSearchView(es_views.ListElasticAPIView):
    permission_classes = (AllowAny,)

    es_client = Elasticsearch(
        hosts=['localhost:9200'],
        connection_class=RequestsHttpConnection
    )
    es_pagination_class = es_pagination.ElasticLimitOffsetPagination
    es_model = ProductIndex
    es_filter_backends = (
        es_filters.ElasticFieldsFilter,
        es_filters.ElasticSearchFilter
    )
    es_filter_fields = (
        es_filters.ESFieldFilter('description', 'name'),
    )
    es_search_fields = (
        'description',
        'name',
    )


# 'api/category/' returns all categories without parent, the base categories
# witch main children with count of products in children and sub-children
class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryOverviewSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Category.objects.filter(parent__isnull=True).order_by('id')
        return queryset


# r'^api/category/' returns category with children with little image for them
# and with path field - ancestors(name+slug)
class SubCategoryView(generics.ListAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            path = self.request.path.replace('/api/category/', '')
            category_slug = path.split('/')[-1]
            queryset = Category.objects.get(slug=category_slug)  # .get_family()
            data = SubCategorySerializer(queryset).data
            response_status = status.HTTP_200_OK
        except Exception as e:
            data['error'] = str(e)
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(data=data, status=response_status)


# api/get-menu/ return base categories( name, slug) without parent,
# for frontend left menu
class MenuCategoryListView(generics.ListAPIView):
    serializer_class = MenuCategorySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Category.objects.filter(parent__isnull=True).order_by('id')
        return queryset


# r'^api/product/' returns all products that has the same category
# or it's subcategory, category takes like the simbols after last slash in path
# optional parameter sort can sort by price or reverse price
class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        path = self.request.path.replace('/api/product/', '')
        category_slug = path.split('/')[-1]
        queryset = []
        if category_slug:
            product_categories = Category.objects.filter(slug=category_slug).get_descendants(include_self=True)
            sort = self.request.query_params.get('sort', '')
            if sort == '':
                queryset = Product.objects.filter(category__in=product_categories, stock__gt=0)
            elif sort == 'price':
                queryset = Product.objects.filter(category__in=product_categories, stock__gt=0).order_by('price')
            elif sort == 'reverse_price':
                queryset = Product.objects.filter(category__in=product_categories, stock__gt=0).order_by('-price')
        else:
            pass
            # queryset = Category.objects.filter(parent__isnull=True).order_by('name')
        return queryset


# r'^api/p/(?P<slug>\S+)/$' returns the produect by slug in path
class ProductView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, slug, *args, **kwargs):
        data = {}
        try:
            product = Product.objects.get(slug=slug)
            data = ProductSerializer(product).data
            response_status = status.HTTP_200_OK
        except Exception as e:
            data['error'] = str(e)
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(data=data, status=response_status)


# api/cart/ returns products from cart in body
class CartView(generics.ListAPIView):
    serializer_class = ProductCartSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # self.request.body - json body like {"1":"12","2":"7"}
        # here 1,2 - products ids
        # 12, 7 - products count
        data = json.loads(self.request.body)
        product_ids = list(map(int, data))
        queryset = Product.objects.filter(id__in=product_ids)
        data = ProductCartSerializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)


# api/create-order/ creates order, if user is not authenticated, then
# order.user would be None
# if there is not enough products on stock, it would be in data['error']
# by each product
class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    def make_order(self, data, user):
        cart = data['cart']
        errors = {}
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=user,
                    first_name=data['firstName'],
                    last_name=data['lastName'],
                    email=data['email'],
                    address=data['address'],
                    postal_code=data['postal_code'],
                    city=data['city'],
                    paid=False)
                for key, value in cart.items():
                    try:
                        product = Product.objects.get(id=int(key))
                        quantity = int(value)
                        product.stock -= quantity
                        product.full_clean()
                        product.save()
                        order_item = OrderItem.objects.create(user=user, order=order, product=product,
                                                              price=product.price, quantity=quantity)
                        order_item.full_clean()
                    except Exception as e:
                        errors[key] = e.message_dict
                if len(errors) > 0:
                    raise Exception(errors)

        except IntegrityError as e:
            return {}, e
        except Exception as e:
            return {}, errors
        return order, {}

    def create(self, request, *args, **kwargs):
        data_in = json.loads(request.body)
        if request.user.is_authenticated:
            order, order_exception = self.make_order(data_in, request.user)
        else:
            order, order_exception = self.make_order(data_in, None)
        if order_exception == {}:
            data = OrderSerializer(order).data
            response_status = status.HTTP_200_OK
        else:
            data = order_exception
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=response_status)


# api/get-last-addr/ only for authenticated users, looking for last order,
# if find return it's address name and other delivery info
class GetLastAddress(generics.ListAPIView):
    serializer_class = LastAddressSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = dict()
        if not request.user.is_authenticated:
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        try:
            last_order = Order.objects.filter(user=request.user).first()
            data = LastAddressSerializer(last_order).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data['error'] - str(e)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)