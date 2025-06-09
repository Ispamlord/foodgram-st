from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from djoser.serializers import SetPasswordSerializer

from recipes.models import Follow
from users.models import User
from users.serializers import FollowSerializer, UserSerializer
from api.permissions import IsCurrentUserOrAdminOrReadOnly
from api.paginations import ApiPagination


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet для пользователей и подписок."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsCurrentUserOrAdminOrReadOnly,)
    pagination_class = ApiPagination

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Возвращает текущего пользователя."""
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated]()_
