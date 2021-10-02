from django.db import models


class ImagesProduct(models.Model):
    """"""
    product = models.ForeignKey('Product')
    image = models.FileField()


class Product(models.Model):
    """ Модель товара """
    category = models.ForeignKey('Category')
    title = models.CharField(verbose_name='Name', max_length=150, db_index=True, blank=True)
    description = models.TextField(verbose_name='Description', max_length=1000)
    characteristics = models.TextField()
    count_in_shop = models.IntegerField(verbose_name='Count', blank=False)
    count_sold = models.IntegerField(verbose_name='Sold', blank=True)
    price = models.FloatField(verbose_name='Price', max_length=10, blank=False)
    recommended_products = models.ManyToManyField('self', )

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'{self.id}. {self.name} {self.description} {self.price} {self.count_in_shop}'


class Category(models.Model):
    """"""
    name = models.CharField()
    slug = models.SlugField()
    image = models.ImageField()


class Shop(models.Model):
    """ Модель магазина """
    name = models.CharField(verbose_name='Name', max_length=150, db_index=True, blank=True)
    description = models.CharField(verbose_name='Description', max_length=1000)
    product = models.ManyToManyField(Product, default=None, blank=True, related_name='product_in_shops',
                                     verbose_name='Product')

    class Meta:
        verbose_name = 'shop'
        verbose_name_plural = 'shops'

    def __str__(self):
        return f'{self.id} {self.name} {self.description} {self.product}'


class Basket(models.Model):
    """Модель корзины"""
    owner =
    products =


class BasketProduct(models.Model):
    """Модель товаров в Корзине"""
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE, blank=True,
                             related_name='user_order', verbose_name='User')
    product = models.ForeignKey(Product, default=None, blank=True, related_name='product_in_order',
                                on_delete=models.CASCADE, verbose_name='Product')
    basket = models.ForeignKey('Basket', default=None, on_delete=models.CASCADE, blank=True,
                              related_name='order', verbose_name='Product')
    quantity = models.PositiveIntegerField(verbose_name='Quantity', blank=True, null=False, default=1)

    class Meta:
        verbose_name = 'order_item'
        verbose_name_plural = 'order_items'

    def __str__(self):
        return f'{self.id} {self.product} {self.order} {self.quantity}'


class Order(models.Model):
    """Модель заказа"""
    STATUS_CHOICES = [
        ('new', 'new'),
        ('paid', 'paid'),
        ('completed', 'completed'),
        ('canceled', 'canceled'),
    ]
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE, blank=True,
                             related_name='user_order', verbose_name='User')
    status = models.CharField(verbose_name='Status', max_length=100, default='new', choices=STATUS_CHOICES, blank=True)
    date_time = models.DateTimeField(verbose_name='time', null=True, auto_now_add=True, blank=False)
    address = models.CharField()
    type_order = models.CharField()

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'{self.id} {self.user} {self.status} {self.date_time}'



