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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsCurrentUserOrAdminOrReadOnly,)
    pagination_class = ApiPagination

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def set_password(self, request):
        serializer = SetPasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({'message': 'Пароль успешно изменён'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, id=pk)
        user = request.user

        if request.method == 'POST':
            serializer = FollowSerializer(data=request.data, context={'request': request, 'author': author})
            serializer.is_valid(raise_exception=True)
            serializer.save(author=author, user=user)
            return Response({'message': 'Подписка успешно создана', 'data': serializer.data}, status=status.HTTP_201_CREATED)

        follow = Follow.objects.filter(author=author, user=user).first()
        if follow:
            follow.delete()
            return Response({'message': 'Успешная отписка'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Подписка не найдена'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        follows = Follow.objects.filter(user=request.user)
        pages = self.paginate_queryset(follows)
        serializer = FollowSerializer(pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
