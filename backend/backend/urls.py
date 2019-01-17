"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from shop.views import ProductSearchView, CategoryListView, SubCategoryView,\
    MenuCategoryListView, ProductListView, ProductView, CartView, CreateOrderView, check_token,\
    NewUserSet, GetLastAddress, verify_user, verify_order

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/obtain_token/', obtain_jwt_token),
    path('auth/refresh_token/', refresh_jwt_token),
    path('auth/token-verify/', verify_jwt_token),
    path('api/check-token/', check_token),
    path('api/add-user/', NewUserSet.as_view()),
    path('api/verify-user', verify_user),
    path('api/verify-order', verify_order),
    path('api/get-menu/', MenuCategoryListView.as_view()),
    path('api/cart/', CartView.as_view()),
    path('api/create-order/', CreateOrderView.as_view()),
    path('api/get-last-addr/', GetLastAddress.as_view()),
    path('api/category/', CategoryListView.as_view()),
    re_path(r'^api/category/', SubCategoryView.as_view()),
    re_path(r'^api/product/', ProductListView.as_view()),
    re_path(r'^api/p/(?P<slug>\S+)/$', ProductView.as_view()),
    url(
        regex=r'^api/list$',
        view=ProductSearchView.as_view(),
        name='product-list'
    ),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
