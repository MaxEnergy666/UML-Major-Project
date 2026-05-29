from django.db import models
from django.conf import settings


class CareerPlanReport(models.Model):
    """职业规划报告"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="career_plans")
    overall_score = models.FloatField("综合评分", default=0)
    summary = models.TextField("分析摘要", blank=True)
    short_term = models.TextField("短期规划 (0-6月)", blank=True)
    mid_term = models.TextField("中期规划 (6月-2年)", blank=True)
    long_term = models.TextField("长期规划 (2-5年)", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "职业规划报告"
        verbose_name_plural = verbose_name
        db_table = "career_plan_reports"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} 的职业规划报告"


class CareerDirection(models.Model):
    """推荐就业方向"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="career_directions")
    name = models.CharField("方向名称", max_length=100)
    match_score = models.FloatField("匹配度", default=0)
    market_demand = models.CharField("市场需求", max_length=50, blank=True)
    typical_positions = models.CharField("典型岗位", max_length=500, blank=True)
    reason = models.TextField("推荐理由", blank=True)
    is_excluded = models.BooleanField("是否排除", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "就业方向"
        verbose_name_plural = verbose_name
        db_table = "career_directions"
        ordering = ["-match_score"]

    def __str__(self):
        return f"{self.name} - 匹配度 {self.match_score}%"


class JobRecommendation(models.Model):
    """推荐岗位"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_recommendations")
    job = models.ForeignKey("jobs.JobPosting", on_delete=models.CASCADE, related_name="recommendations")
    overall_match = models.FloatField("综合匹配度", default=0)
    major_match = models.FloatField("专业匹配", default=0)
    skill_match = models.FloatField("能力匹配", default=0)
    interest_match = models.FloatField("兴趣匹配", default=0)
    salary_match = models.FloatField("薪资匹配", default=0)
    city_match = models.FloatField("城市匹配", default=0)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "岗位推荐"
        verbose_name_plural = verbose_name
        db_table = "job_recommendations"
        ordering = ["-overall_match"]

    def __str__(self):
        return f"{self.job.title} - 匹配度 {self.overall_match}%"


class ImprovementSuggestion(models.Model):
    """提升建议"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="improvements")
    skill_name = models.CharField("技能名称", max_length=100)
    current_score = models.FloatField("当前分数", default=0)
    target_score = models.FloatField("目标分数", default=0)
    learning_path = models.TextField("学习路径", blank=True)
    recommended_courses = models.TextField("推荐课程", blank=True)
    recommended_books = models.TextField("推荐书籍", blank=True)
    recommended_projects = models.TextField("推荐项目", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "提升建议"
        verbose_name_plural = verbose_name
        db_table = "improvement_suggestions"
        ordering = ["-current_score"]

    def __str__(self):
        return f"{self.skill_name} 提升建议"


class MockInterviewRecord(models.Model):
    """模拟面试记录"""

    TYPE_CHOICES = [
        ("behavioral", "行为面试"),
        ("technical", "技术面试"),
        ("comprehensive", "综合面试"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interviews")
    target_job = models.CharField("目标岗位", max_length=200, blank=True)
    interview_type = models.CharField("面试类型", max_length=20, choices=TYPE_CHOICES)
    rounds = models.IntegerField("轮数", default=3)
    overall_score = models.FloatField("综合评分", default=0)
    feedback = models.TextField("评估反馈", blank=True)
    status = models.CharField("状态", max_length=20, default="pending")  # pending, in_progress, completed
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    completed_at = models.DateTimeField("完成时间", null=True, blank=True)

    class Meta:
        verbose_name = "模拟面试"
        verbose_name_plural = verbose_name
        db_table = "mock_interview_records"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} 的{self.get_interview_type_display()}"


class InterviewMessage(models.Model):
    """面试对话消息"""

    ROLE_CHOICES = [
        ("ai", "AI 面试官"),
        ("user", "用户"),
    ]

    interview = models.ForeignKey(MockInterviewRecord, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField("角色", max_length=10, choices=ROLE_CHOICES)
    content = models.TextField("内容")
    feedback = models.TextField("反馈", blank=True)  # AI 对用户回答的反馈
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "面试消息"
        verbose_name_plural = verbose_name
        db_table = "interview_messages"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.get_role_display()}: {self.content[:50]}"


class ResumeOptimizationReport(models.Model):
    """简历优化报告"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resume_reports")
    target_job = models.CharField("目标岗位", max_length=200, blank=True)
    original_resume = models.TextField("原始简历内容", blank=True)
    optimized_resume = models.TextField("优化后简历", blank=True)
    suggestions = models.TextField("优化建议", blank=True)
    overall_score = models.FloatField("综合评分", default=0)
    keyword_coverage = models.FloatField("关键词覆盖度", default=0)
    status = models.CharField("状态", max_length=20, default="pending")  # pending, processing, completed
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "简历优化报告"
        verbose_name_plural = verbose_name
        db_table = "resume_optimization_reports"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} 的简历优化报告"
