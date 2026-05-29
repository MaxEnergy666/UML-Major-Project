from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import (
    CareerPlanReport,
    CareerDirection,
    JobRecommendation,
    ImprovementSuggestion,
    MockInterviewRecord,
    InterviewMessage,
    ResumeOptimizationReport,
)
from .serializers import (
    CareerPlanReportSerializer,
    CareerDirectionSerializer,
    JobRecommendationSerializer,
    ImprovementSuggestionSerializer,
    MockInterviewRecordSerializer,
    InterviewMessageSerializer,
    ResumeOptimizationReportSerializer,
    InterviewConfigSerializer,
)
from services.llm_service import get_llm_service


class CareerPlanViewSet(viewsets.ModelViewSet):
    """职业规划报告视图集"""

    serializer_class = CareerPlanReportSerializer

    def get_queryset(self):
        return CareerPlanReport.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def generate(self, request):
        """生成职业规划报告"""
        llm = get_llm_service()
        report_data = llm.generate_career_plan(request.user.id)

        report = CareerPlanReport.objects.create(
            user=request.user,
            overall_score=report_data["overall_score"],
            summary=report_data["summary"],
            short_term=report_data["short_term"],
            mid_term=report_data["mid_term"],
            long_term=report_data["long_term"],
        )
        return Response(CareerPlanReportSerializer(report).data, status=status.HTTP_201_CREATED)


class CareerDirectionViewSet(viewsets.ModelViewSet):
    """就业方向视图集"""

    serializer_class = CareerDirectionSerializer

    def get_queryset(self):
        return CareerDirection.objects.filter(user=request.user, is_excluded=False)

    @action(detail=True, methods=["post"])
    def exclude(self, request, pk=None):
        """排除该方向"""
        direction = self.get_object()
        direction.is_excluded = True
        direction.save()
        return Response({"status": "excluded"})

    @action(detail=False, methods=["post"])
    def generate(self, request):
        """生成就业方向推荐"""
        llm = get_llm_service()
        directions_data = llm.generate_career_directions(request.user.id)

        directions = []
        for data in directions_data:
            direction = CareerDirection.objects.create(
                user=request.user,
                name=data["name"],
                match_score=data["match_score"],
                market_demand=data["market_demand"],
                typical_positions=data["typical_positions"],
                reason=data["reason"],
            )
            directions.append(direction)
        return Response(CareerDirectionSerializer(directions, many=True).data, status=status.HTTP_201_CREATED)


class JobRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """岗位推荐视图集"""

    serializer_class = JobRecommendationSerializer

    def get_queryset(self):
        queryset = JobRecommendation.objects.filter(user=self.request.user)

        # 二次筛选
        city = self.request.query_params.get("city")
        salary_min = self.request.query_params.get("salary_min")
        salary_max = self.request.query_params.get("salary_max")
        job_type = self.request.query_params.get("job_type")

        if city:
            queryset = queryset.filter(job__city=city)
        if salary_min:
            queryset = queryset.filter(job__salary_max__gte=int(salary_min))
        if salary_max:
            queryset = queryset.filter(job__salary_min__lte=int(salary_max))
        if job_type:
            queryset = queryset.filter(job__job_type=job_type)

        return queryset


class ImprovementSuggestionViewSet(viewsets.ModelViewSet):
    """提升建议视图集"""

    serializer_class = ImprovementSuggestionSerializer

    def get_queryset(self):
        return ImprovementSuggestion.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def generate(self, request):
        """生成提升建议"""
        llm = get_llm_service()
        suggestions_data = llm.generate_improvement_suggestions(request.user.id)

        suggestions = []
        for data in suggestions_data:
            suggestion = ImprovementSuggestion.objects.create(
                user=request.user,
                skill_name=data["skill_name"],
                current_score=data["current_score"],
                target_score=data["target_score"],
                learning_path=data["learning_path"],
                recommended_courses=data["recommended_courses"],
                recommended_books=data["recommended_books"],
                recommended_projects=data["recommended_projects"],
            )
            suggestions.append(suggestion)
        return Response(ImprovementSuggestionSerializer(suggestions, many=True).data, status=status.HTTP_201_CREATED)


class MockInterviewViewSet(viewsets.ModelViewSet):
    """模拟面试视图集"""

    serializer_class = MockInterviewRecordSerializer

    def get_queryset(self):
        return MockInterviewRecord.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def start(self, request):
        """开始模拟面试"""
        serializer = InterviewConfigSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        interview = MockInterviewRecord.objects.create(
            user=request.user,
            target_job=serializer.validated_data["target_job"],
            interview_type=serializer.validated_data["interview_type"],
            rounds=serializer.validated_data["rounds"],
            status="in_progress",
        )

        # 生成第一道题
        llm = get_llm_service()
        first_question = llm.generate_interview_question(
            interview.target_job,
            interview.interview_type,
            1,
        )

        InterviewMessage.objects.create(
            interview=interview,
            role="ai",
            content=first_question,
        )

        return Response(MockInterviewRecordSerializer(interview).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def answer(self, request, pk=None):
        """用户回答问题"""
        interview = self.get_object()
        answer_text = request.data.get("answer", "")

        # 保存用户回答
        InterviewMessage.objects.create(
            interview=interview,
            role="user",
            content=answer_text,
        )

        # 生成 AI 反馈和下一题
        llm = get_llm_service()
        current_round = interview.messages.filter(role="ai").count()

        if current_round >= interview.rounds:
            # 面试结束，生成评估报告
            feedback = llm.generate_interview_evaluation(interview.id)
            interview.overall_score = feedback["overall_score"]
            interview.feedback = feedback["feedback"]
            interview.status = "completed"
            interview.completed_at = timezone.now()
            interview.save()

            return Response({
                "status": "completed",
                "evaluation": feedback,
            })

        # 生成下一题
        feedback_text = llm.generate_interview_feedback(answer_text)
        next_question = llm.generate_interview_question(
            interview.target_job,
            interview.interview_type,
            current_round + 1,
        )

        InterviewMessage.objects.create(
            interview=interview,
            role="ai",
            content=next_question,
            feedback=feedback_text,
        )

        return Response({
            "status": "in_progress",
            "feedback": feedback_text,
            "next_question": next_question,
        })


class ResumeOptimizationViewSet(viewsets.ModelViewSet):
    """简历优化视图集"""

    serializer_class = ResumeOptimizationReportSerializer

    def get_queryset(self):
        return ResumeOptimizationReport.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def optimize(self, request):
        """提交简历优化请求"""
        original_resume = request.data.get("resume", "")
        target_job = request.data.get("target_job", "")

        report = ResumeOptimizationReport.objects.create(
            user=request.user,
            target_job=target_job,
            original_resume=original_resume,
            status="processing",
        )

        # 调用 LLM 生成优化建议
        llm = get_llm_service()
        result = llm.optimize_resume(original_resume, target_job)

        report.optimized_resume = result["optimized_resume"]
        report.suggestions = result["suggestions"]
        report.overall_score = result["overall_score"]
        report.keyword_coverage = result["keyword_coverage"]
        report.status = "completed"
        report.save()

        return Response(ResumeOptimizationReportSerializer(report).data, status=status.HTTP_201_CREATED)
