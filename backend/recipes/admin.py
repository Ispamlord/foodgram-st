from django.conf import settings
from django.contrib import admin

from recipes.models import (Bookmark, Product, Dish,
                            DishProduct, Cart, Label)


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name', 'color', 'slug')
    empty_value_display = settings.EMPTY_VALUE


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = settings.EMPTY_VALUE


class DishProductInline(admin.TabularInline):
    model = DishProduct


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'bookmarks_count')
    search_fields = ('name', 'author__username')
    list_filter = ('name', 'author', 'labels')
    empty_value_display = settings.EMPTY_VALUE
    inlines = [
        DishProductInline,
    ]

    def bookmarks_count(self, obj):
        return obj.favorited_by.count()
    bookmarks_count.short_description = 'В избранном'


@admin.register(DishProduct)
class DishProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'dish', 'product', 'amount')
    empty_value_display = settings.EMPTY_VALUE


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'dish')
    search_fields = ('user__username', 'dish__name')
    empty_value_display = settings.EMPTY_VALUE


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'dish')
    search_fields = ('user__username', 'dish__name')
    empty_value_display = settings.EMPTY_VALUE
