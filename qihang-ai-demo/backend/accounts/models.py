from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户模型"""

    ROLE_CHOICES = [
        ("student", "普通用户"),
        ("admin", "系统管理员"),
    ]

    phone = models.CharField("手机号", max_length=11, blank=True)
    role = models.CharField("角色", max_length=10, choices=ROLE_CHOICES, default="student")
    is_verified = models.BooleanField("是否已认证", default=False)
    name = models.CharField("姓名", max_length=50, blank=True, default="")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        db_table = "users"

    def __str__(self):
        return self.username
