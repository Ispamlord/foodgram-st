from django.contrib import admin
from .models import (
    Bookmark,
    Subscription,
    Product,
    DishProduct,
    Dish,
    Cart,
    Label
)


class ProductInline(admin.TabularInline):
    model = DishProduct
    extra = 3


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('author',)
    search_fields = ('user',)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish')
    list_filter = ('user',)
    search_fields = ('user',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish')
    list_filter = ('user',)
    search_fields = ('user',)


@admin.register(DishProduct)
class DishProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'dish', 'product', 'amount')
    list_filter = ('dish', 'product')
    search_fields = ('product__name',)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'created_at', 'favorite_count')
    search_fields = ('name',)
    list_filter = ('created_at', 'author', 'name', 'labels')
    filter_horizontal = ('ingredients',)
    empty_value_display = '-пусто-'
    inlines = [ProductInline]

    def favorite_count(self, obj):
        return obj.favorited_by.count()

    favorite_count.short_description = 'В избранном'


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    list_filter = ('name',)
    search_fields = ('name',)
