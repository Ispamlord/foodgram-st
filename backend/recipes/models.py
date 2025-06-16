from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Label(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        unique=True
    )
    slug = models.SlugField(
        'Слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
    )
    unit = models.CharField(
        'Единица измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Dish(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dishes',
        verbose_name='Автор',
    )
    name = models.CharField(
        'Название',
        max_length=200,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='media/',
        blank=True,
    )
    description = models.TextField(
        'Описание',
    )
    ingredients = models.ManyToManyField(
        Product,
        through='DishProduct',
        verbose_name='Ингредиенты',
    )
    labels = models.ManyToManyField(
        Label,
        verbose_name='Теги',
    )
    time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                1, 'Время приготовления не должно быть меньше 1 минуты'
            )
        ]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class DishProduct(models.Model):
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='dishproducts',
        verbose_name='Рецепт'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='dishproducts',
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                1, 'Количество ингредиентов не может быть меньше 1'
            )
        ]
    )

    class Meta:
        verbose_name = 'Состав рецепта'
        verbose_name_plural = 'Состав рецепта'


class Bookmark(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name='Пользователь',
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'dish'],
                name='unique_user_dish_bookmark'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user.username} добавил {self.dish.name} в избранное'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Пользователь'
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='in_carts',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'dish'],
                name='unique_user_dish_cart'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user.username} добавил {self.dish.name} в список покупок'
