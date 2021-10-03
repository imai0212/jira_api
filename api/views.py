from django.shortcuts import render
from rest_framework import status, permissions, generics, viewsets
from rest_framework.response import Response
from .serializers import UserSerializer, CategorySerializer, TaskSerializer, ProfileSerializer
from .models import  Task, Category, Profile
from django.contrib.auth.models import User
from . import custom_permissions

# Endpoint作成
# 新規ユーザ作成
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    # 全ユーザーをアクセス許可設定
    permission_classes = (permissions.AllowAny,)


# リスト取得
class ListUserView(generics.ListAPIView):
    # 全てのユーザーを選択
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ログインユーザー情報取得
class LoginUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    # 更新の無効化
    def update(self, request, *args, **kwargs):
        response = {'message': 'PUT method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

# CRUD機能
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # CRUDのcreate要素を上書き
    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    def destroy(self, request, *args, **kwargs):
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'PUT method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated, custom_permissions.OwnerPermission,)

    # 新規タスク作成時にログインユーザーをowner属性にデフォルト設定
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
