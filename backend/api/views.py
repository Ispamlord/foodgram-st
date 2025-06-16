from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from recipes.models import Recipe, Tag, Ingredient, Favorite, ShoppingCart
from users.models import User
from api.serializers import (
    RecipeListSerializer, TagSerializer, IngredientSerializer,
    FavoriteSerializer, ShoppingCartSerializer, RecipeWriteSerializer
)
from api.services import download_shopping_cart
from api.permissions import PrivilegeAdmin
from api.filters import IngredientSearchFilter, RecipeFilter
from api.paginations import ApiPagination


class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (PrivilegeAdmin,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = ApiPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeListSerializer
        return RecipeWriteSerializer

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        if request.method == 'POST':
            if Favorite.objects.filter(author=user, recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже добавлен!'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = FavoriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(author=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not Favorite.objects.filter(author=user, recipe=recipe).exists():
            return Response({'errors': 'Объект не найден'}, status=status.HTTP_404_NOT_FOUND)
        Favorite.objects.filter(author=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        if request.method == 'POST':
            if ShoppingCart.objects.filter(author=user, recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже добавлен!'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ShoppingCartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(author=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not ShoppingCart.objects.filter(author=user, recipe=recipe).exists():
            return Response({'errors': 'Объект не найден'}, status=status.HTTP_404_NOT_FOUND)
        ShoppingCart.objects.filter(author=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        if user.shopping_cart.exists():
            return download_shopping_cart(request, user)
        return Response({'errors': 'Список покупок пуст.'}, status=status.HTTP_404_NOT_FOUND)
