from django.db import models


class SystemLog(models.Model):
    """系统日志"""

    LEVEL_CHOICES = [
        ("info", "信息"),
        ("warning", "警告"),
        ("error", "错误"),
    ]

    level = models.CharField("日志级别", max_length=10, choices=LEVEL_CHOICES, default="info")
    action = models.CharField("操作", max_length=200)
    detail = models.TextField("详情", blank=True)
    ip_address = models.GenericIPAddressField("IP地址", null=True, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "系统日志"
        verbose_name_plural = verbose_name
        db_table = "system_logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.level}] {self.action}"
