from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, EmailValidator
from mptt.models import MPTTModel, TreeForeignKey
import uuid
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django_extensions.db.fields import AutoSlugField
from transliterate import translit
# Create your models here.


# Product's Category with tree foreign keys
class Category(MPTTModel):
    name = models.CharField(max_length=200, db_index=True)
    slug = AutoSlugField(
        max_length=200, db_index=True, unique=True,
        populate_from='transliterate_slug')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

    class Meta:
        ordering = ['name']
        verbose_name = 'Category/Категория'
        verbose_name_plural = 'Categories/Категории'

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    # count of products with this or it children category
    def get_group_count(self):
        category = self.get_descendants(include_self=True)
        return Product.objects.filter(category__in=category).count()

    # category image - image from first product image thumbnail
    def image(self):
        category = self.get_descendants(include_self=True)
        first_product = Product.objects.filter(category__in=category).first()
        if first_product is not None:
            return first_product.image_thumbnail
        else:
            return None

    # return ancestor's path
    def path(self):
        return self.get_ancestors()

    # return transliterates name
    def transliterate_slug(self):
        return translit(self.name, reversed=True)


# Product model
class Product(models.Model):
    category = TreeForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='products', verbose_name="Category/Категория")
    name = models.CharField(max_length=200, db_index=True, verbose_name="Name/Имя")
    slug = AutoSlugField(
        max_length=200, db_index=True, unique=True,
        populate_from='transliterate_slug')
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True,
                              verbose_name="Product image/Изображение товара")
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(170, 113)],
                                     format='JPEG',
                                     options={'quality': 60})
    description = models.TextField(blank=True, verbose_name="Description/Описание")
    price = models.IntegerField(verbose_name="Price/Цена")
    stock = models.PositiveIntegerField(verbose_name="In stock/На складе", validators=[MinValueValidator(0)])
    available = models.BooleanField(default=True, verbose_name="Available/Доступен")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # return html code for product image to display admin panel
    def image_img(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.image.url))
        else:
            return '(No image/Нет изображения)'

    image_img.short_description = 'Pic/Картинка'
    image_img.allow_tags = True

    # return transliterates name
    def transliterate_slug(self):
        return translit(self.name, reversed=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


# Order class
class Order(models.Model):
    REJECTED = 'R'
    NOT_CONFIRMED = 'N'
    REQUIRES_ATTENTION = 'R'
    WORK_IN_PROGRESS = 'W'
    COMPLETED = 'C'
    STATUS_CHOICES = (
        (REJECTED, "Rejected"),
        (NOT_CONFIRMED, "Not confirmed"),
        (REQUIRES_ATTENTION, "Requires attention"),
        (WORK_IN_PROGRESS, "Work in progress"),
        (COMPLETED, "Completed")
    )
    user = models.ForeignKey(User, verbose_name='Заказчик', null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name='First Name/Имя', max_length=50)
    last_name = models.CharField(verbose_name='Last Name/Фамилия', max_length=50)
    email = models.EmailField(verbose_name='Email', validators=[EmailValidator])
    address = models.CharField(verbose_name='Address/Адрес', max_length=250)
    postal_code = models.CharField(verbose_name='Postal code/Почтовый код', max_length=20)
    city = models.CharField(verbose_name='City/Город', max_length=100)
    created = models.DateTimeField(verbose_name='Created/Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Updated/Обновлен', auto_now=True)
    paid = models.BooleanField(verbose_name='Paid/Оплачен', default=False)
    status = models.CharField(verbose_name='Status/Статус', choices=STATUS_CHOICES,
                              max_length=1, default=NOT_CONFIRMED)
    uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order/Заказ'
        verbose_name_plural = 'Orders/Заказы'

    def __str__(self):
        return 'Заказ: {}'.format(self.id)

    # Summ cost all products in Order
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


# Order item class
class OrderItem(models.Model):
    user = models.ForeignKey(User, verbose_name='Заказчик', null=True, blank=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='items', verbose_name='Order/Заказ', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', verbose_name='Product/Продукт',
                                on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Price/Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Quantity/Количество',
                                           validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Order item/Позиция заказа'
        verbose_name_plural = 'Orders items/Позиции заказов'

    def __str__(self):
        return '{}'.format(self.id)

    # Price of position in Order
    def get_cost(self):
        return self.price * self.quantity


# UserProfile class for user uuid
class UserProfile(models.Model):
    user = models.ForeignKey(User, verbose_name='Заказчик', null=True, blank=True, on_delete=models.CASCADE)
    uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)
