from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q, F
from users.models import User


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    unit = models.CharField(max_length=200)

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Label(models.Model):
    GREEN = '09db4f'
    ORANGE = 'fa6a02'
    PURPLE = 'b813d1'

    COLOR_CHOICES = [
        (GREEN, 'Зеленый'),
        (ORANGE, 'Оранжевый'),
        (PURPLE, 'Фиолетовый'),
    ]

    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7, unique=True, choices=COLOR_CHOICES, default=GREEN)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Dish(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Product, through='DishProduct')
    labels = models.ManyToManyField(Label)
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    time = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='media/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        default_related_name = 'dishes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'author'], name='unique_dish')
        ]

    def __str__(self):
        return self.name


class DishProduct(models.Model):
    dish = models.ForeignKey(Dish, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Состав рецепта'
        verbose_name_plural = 'Состав рецепта'
        constraints = [
            models.UniqueConstraint(fields=['dish', 'product'], name='unique_dish_product')
        ]

    def __str__(self):
        return f'{self.product} {self.amount}'


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart_items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, related_name='in_carts', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'dish'], name='unique_cart_item')
        ]

    def __str__(self):
        return str(self.dish)


class Bookmark(models.Model):
    user = models.ForeignKey(User, related_name='bookmarks', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, related_name='favorited_by', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(fields=['user', 'dish'], name='unique_bookmark')
        ]

    def __str__(self):
        return str(self.dish)


class Subscription(models.Model):
    user = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='subscribers', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'], name='unique_subscription'),
            models.CheckConstraint(check=~Q(user=F('author')), name='no_self_subscription')
        ]

    def __str__(self):
        return f'{self.user} → {self.author}'
