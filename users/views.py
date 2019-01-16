# -*- coding: UTF-8 -*-


# Create your views here.

from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from apps.users.serializers import UserRegisterSerializer, UserDetailSerializer, RoleSerializer
from apps.users.models import Role


User = get_user_model()

class UserViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    #动态配置返回的用户信息
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegisterSerializer
        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated, )
    #重载获取权限的函数，动态配置权限，注册不需要权限
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class RoleViewSet(CreateModelMixin,mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    """
    登录成功后自定义返回
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
    "code":20000,
    "data": {
        "token": "JWT "+ token
    }
    }