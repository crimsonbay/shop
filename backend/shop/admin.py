from django.contrib import admin
from .models import Category, Product, Order, OrderItem, UserProfile
from mptt.admin import MPTTModelAdmin

# Register your models here.


class CategoryAdmin(MPTTModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'image_img', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    readonly_fields = ['image_img', ]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_field = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',
                    'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(UserProfile)