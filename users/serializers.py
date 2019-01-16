# -*- coding: UTF-8 -*-
from django.contrib.auth import get_user_model
from apps.users.models import Role
from rest_framework import serializers

from rest_framework.validators import UniqueValidator

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ("role_name", "role_desc", "role_parent_id")

class UserRegisterSerializer(serializers.ModelSerializer):

    # role = serializers.CharField(source="role.role_name", read_only=True)
    role = serializers.StringRelatedField(many=True)


    # 利用drf中的validators验证username是否唯一
    username = serializers.CharField(required=True, allow_blank=False, validators=[UniqueValidator(queryset=User.objects.all(),
                                                                                        message='用户已经存在')])
    print(username)
    password = serializers.CharField(
         style={"input_type": "password"},help_text="密码", label="密码", write_only=True,
     )
    print(password, "password")

    def create(self, validated_data):
         user = super(UserRegisterSerializer, self).create(validated_data= validated_data)
         user.set_password(validated_data["password"])
         user.save()
         return user
    class Meta:
         model = User
         fields = ( "username", "password", "role", "avatar")
         depth = 1


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列表类
    """
    # role = serializers.CharField(source="role.role_name", read_only=True)
    role = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = ("id", "username", "name", "role", "avatar")