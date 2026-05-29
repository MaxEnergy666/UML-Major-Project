from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    """用户档案 - 基础信息"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField("姓名", max_length=50, default="")
    gender = models.CharField("性别", max_length=10, blank=True)
    birth_date = models.DateField("出生日期", null=True, blank=True)
    university = models.CharField("学校", max_length=100, blank=True)
    major = models.CharField("专业", max_length=100, blank=True)
    grade = models.CharField("年级", max_length=20, blank=True)
    gpa = models.FloatField("GPA", null=True, blank=True)
    introduction = models.TextField("自我介绍", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "用户档案"
        verbose_name_plural = verbose_name
        db_table = "user_profiles"

    def __str__(self):
        return f"{self.name} 的档案"


class Experience(models.Model):
    """经历 - 实习/项目/竞赛等"""

    TYPE_CHOICES = [
        ("internship", "实习经历"),
        ("project", "项目经历"),
        ("competition", "竞赛经历"),
        ("activity", "活动经历"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="experiences")
    type = models.CharField("类型", max_length=20, choices=TYPE_CHOICES)
    title = models.CharField("标题", max_length=200)
    organization = models.CharField("组织/公司", max_length=200, blank=True)
    start_date = models.DateField("开始日期")
    end_date = models.DateField("结束日期", null=True, blank=True)
    description = models.TextField("描述", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "经历"
        verbose_name_plural = verbose_name
        db_table = "experiences"
        ordering = ["-start_date"]

    def __str__(self):
        return self.title


class MBTIResult(models.Model):
    """MBTI 测评结果"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mbti")
    code = models.CharField("MBTI 类型", max_length=10)  # 如 INTJ-A
    ei_score = models.FloatField("外向-内向分数", default=50)
    sn_score = models.FloatField("感觉-直觉分数", default=50)
    tf_score = models.FloatField("思维-情感分数", default=50)
    jp_score = models.FloatField("判断-知觉分数", default=50)
    description = models.TextField("类型描述", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "MBTI 结果"
        verbose_name_plural = verbose_name
        db_table = "mbti_results"


class HollandResult(models.Model):
    """霍兰德测评结果"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="holland")
    code = models.CharField("霍兰德代码", max_length=10)  # 如 IAS
    r_score = models.FloatField("现实型", default=0)
    i_score = models.FloatField("研究型", default=0)
    a_score = models.FloatField("艺术型", default=0)
    s_score = models.FloatField("社会型", default=0)
    e_score = models.FloatField("企业型", default=0)
    c_score = models.FloatField("常规型", default=0)
    description = models.TextField("结果描述", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "霍兰德结果"
        verbose_name_plural = verbose_name
        db_table = "holland_results"


class CompetencyResult(models.Model):
    """胜任力测评结果"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="competency")
    learning_score = models.FloatField("学习能力", default=0)
    communication_score = models.FloatField("沟通能力", default=0)
    teamwork_score = models.FloatField("团队协作", default=0)
    problem_solving_score = models.FloatField("问题解决", default=0)
    leadership_score = models.FloatField("领导力", default=0)
    innovation_score = models.FloatField("创新能力", default=0)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "胜任力结果"
        verbose_name_plural = verbose_name
        db_table = "competency_results"
