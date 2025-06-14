from rest_framework import serializers

from recipes.models import Follow, Recipe
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class RecipeMiniSerializer(serializers.ModelSerializer):
    """Lightweight serializer for Recipe used in FollowSerializer."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(UserSerializer):
    """Serializer for user subscriptions."""
    recipes = RecipeMiniSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )

    def get_recipes_count(self, obj):
        return obj.recipe.count()
