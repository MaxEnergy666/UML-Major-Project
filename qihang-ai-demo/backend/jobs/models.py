from django.db import models
from django.conf import settings


class JobPosting(models.Model):
    """岗位信息"""

    title = models.CharField("岗位名称", max_length=200)
    company = models.CharField("公司名称", max_length=200)
    city = models.CharField("城市", max_length=50)
    salary_min = models.IntegerField("最低薪资(K)")
    salary_max = models.IntegerField("最高薪资(K)")
    job_type = models.CharField("岗位类型", max_length=50)  # 如：技术、产品、运营、设计
    experience = models.CharField("经验要求", max_length=50, blank=True)
    education = models.CharField("学历要求", max_length=50, blank=True)
    description = models.TextField("岗位描述", blank=True)
    requirements = models.TextField("任职要求", blank=True)
    tags = models.CharField("标签", max_length=500, blank=True)  # 逗号分隔
    is_active = models.BooleanField("是否在招", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "岗位信息"
        verbose_name_plural = verbose_name
        db_table = "job_postings"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.company}"

    @property
    def salary_range(self):
        return f"{self.salary_min}K-{self.salary_max}K"


class JobFavorite(models.Model):
    """岗位收藏"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField("收藏时间", auto_now_add=True)

    class Meta:
        verbose_name = "岗位收藏"
        verbose_name_plural = verbose_name
        db_table = "job_favorites"
        unique_together = ["user", "job"]

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.job.title}"
