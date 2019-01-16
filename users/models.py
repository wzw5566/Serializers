from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.

class Role(models.Model):
    """
    角色表
    """
    role_name = models.CharField(max_length=30, unique=True, verbose_name="角色名")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    role_desc = models.TextField(max_length=100, verbose_name="角色描述")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="更新时间")

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.role_name


class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female", verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    role = models.ManyToManyField(Role, verbose_name="角色", related_name='roles')

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username