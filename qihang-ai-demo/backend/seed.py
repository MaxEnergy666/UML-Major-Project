"""
种子数据脚本 - 一键灌入演示数据
运行方式: python seed.py
"""

import os
import sys
import django

# 设置 Django 环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qihang.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from accounts.models import User
from profiles.models import UserProfile, Experience, MBTIResult, HollandResult, CompetencyResult
from jobs.models import JobPosting, JobFavorite
from career.models import CareerPlanReport, CareerDirection, JobRecommendation, ImprovementSuggestion, MockInterviewRecord, InterviewMessage, ResumeOptimizationReport
from admin_panel.models import SystemLog
from services.llm_service import MockLLMService


def seed():
    print("开始灌入演示数据...")

    # 1. 创建演示用户
    demo_user, created = User.objects.get_or_create(
        username="demo_student",
        defaults={
            "phone": "13800138000",
            "role": "student",
            "is_verified": True,
            "name": "何家齐",
        }
    )
    if created:
        demo_user.set_password("demo1234")
        demo_user.save()
        print("[OK] 创建演示用户: demo_student / demo1234")
    else:
        print("[OK] 演示用户已存在")

    # 2. 创建管理员用户
    admin_user, created = User.objects.get_or_create(
        username="admin",
        defaults={
            "phone": "13800138001",
            "role": "admin",
            "is_verified": True,
            "name": "系统管理员",
        }
    )
    if created:
        admin_user.set_password("admin1234")
        admin_user.save()
        print("[OK] 创建管理员用户: admin / admin1234")
    else:
        print("[OK] 管理员用户已存在")

    # 3. 创建用户档案
    profile, _ = UserProfile.objects.get_or_create(
        user=demo_user,
        defaults={
            "name": "何家齐",
            "gender": "男",
            "birth_date": "2003-06-15",
            "university": "华南理工大学",
            "major": "软件工程",
            "grade": "大三",
            "gpa": 3.6,
            "introduction": "热爱技术，对AI和大数据方向有浓厚兴趣。具备扎实的编程基础和良好的学习能力，善于团队协作，追求技术卓越。",
        }
    )
    print("[OK] 创建用户档案")

    # 4. 创建经历
    experiences_data = [
        {
            "type": "internship",
            "title": "后端开发实习生",
            "organization": "字节跳动",
            "start_date": "2024-07-01",
            "end_date": "2024-09-30",
            "description": "参与抖音推荐系统后端开发，负责特征工程模块。优化数据处理管道，处理效率提升30%。获得优秀实习生评价。",
        },
        {
            "type": "project",
            "title": "基于Transformer的文本情感分析系统",
            "organization": "课程项目",
            "start_date": "2024-03-01",
            "end_date": "2024-06-30",
            "description": "使用PyTorch实现基于BERT的情感分析模型，在Yelp数据集上达到92%准确率。设计并实现了数据增强策略，将模型性能提升5%。",
        },
        {
            "type": "project",
            "title": "智能推荐系统设计与实现",
            "organization": "课程项目",
            "start_date": "2023-09-01",
            "end_date": "2023-12-31",
            "description": "参与设计基于协同过滤的推荐算法，支撑日均10万+请求。使用Redis缓存优化推荐接口响应时间，从200ms降至50ms。",
        },
        {
            "type": "competition",
            "title": "全国大学生数学建模竞赛",
            "organization": "教育部",
            "start_date": "2024-09-01",
            "end_date": "2024-09-03",
            "description": "获得省级一等奖，负责模型构建和算法实现部分。",
        },
    ]

    for exp_data in experiences_data:
        Experience.objects.get_or_create(
            user=demo_user,
            title=exp_data["title"],
            defaults=exp_data,
        )
    print("[OK] 创建用户经历")

    # 5. 创建 MBTI 结果
    MBTIResult.objects.get_or_create(
        user=demo_user,
        defaults={
            "code": "INTJ-A",
            "ei_score": 25,  # 内向
            "sn_score": 75,  # 直觉
            "tf_score": 65,  # 思维
            "jp_score": 70,  # 判断
            "description": "INTJ-A（建筑师型人格）：独立、有远见、战略性思维。擅长制定长期计划并系统性地解决问题，追求效率和卓越。",
        }
    )
    print("[OK] 创建 MBTI 结果")

    # 6. 创建霍兰德结果
    HollandResult.objects.get_or_create(
        user=demo_user,
        defaults={
            "code": "IAS",
            "r_score": 35,
            "i_score": 85,
            "a_score": 65,
            "s_score": 55,
            "e_score": 45,
            "c_score": 40,
            "description": "IAS（研究型/艺术型/社会型）：喜欢探索和研究新事物，具有创造力和想象力，善于分析问题并提出创新解决方案。",
        }
    )
    print("[OK] 创建霍兰德结果")

    # 7. 创建胜任力结果
    CompetencyResult.objects.get_or_create(
        user=demo_user,
        defaults={
            "learning_score": 85,
            "communication_score": 70,
            "teamwork_score": 78,
            "problem_solving_score": 82,
            "leadership_score": 65,
            "innovation_score": 88,
        }
    )
    print("[OK] 创建胜任力结果")

    # 8. 创建岗位数据
    jobs_data = [
        {"title": "AI 算法工程师", "company": "字节跳动", "city": "北京", "salary_min": 25, "salary_max": 45, "job_type": "技术", "experience": "1-3年", "education": "硕士及以上", "description": "负责推荐系统算法研发，包括召回、排序等核心模块。", "requirements": "熟悉深度学习框架，有推荐系统或NLP项目经验优先。", "tags": "AI,深度学习,推荐系统,NLP"},
        {"title": "数据分析师", "company": "阿里巴巴", "city": "杭州", "salary_min": 20, "salary_max": 35, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责业务数据分析，提供数据驱动的决策支持。", "requirements": "熟练使用SQL、Python，具备数据可视化能力。", "tags": "数据分析,SQL,Python,数据可视化"},
        {"title": "后端开发工程师", "company": "腾讯", "city": "深圳", "salary_min": 22, "salary_max": 40, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责微信支付后端系统开发和维护。", "requirements": "熟悉Java/Go，了解分布式系统设计。", "tags": "Java,Go,微服务,分布式"},
        {"title": "前端开发工程师", "company": "美团", "city": "北京", "salary_min": 20, "salary_max": 35, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责美团App前端页面开发和性能优化。", "requirements": "熟悉Vue/React，了解前端工程化。", "tags": "Vue,React,前端工程化"},
        {"title": "产品经理", "company": "京东", "city": "北京", "salary_min": 18, "salary_max": 30, "job_type": "产品", "experience": "1-3年", "education": "本科及以上", "description": "负责电商产品规划和需求分析。", "requirements": "具备良好的沟通能力和逻辑思维，有电商经验优先。", "tags": "产品规划,需求分析,用户体验"},
        {"title": "运营专员", "company": "网易", "city": "杭州", "salary_min": 12, "salary_max": 20, "job_type": "运营", "experience": "应届生", "education": "本科及以上", "description": "负责游戏社区运营和用户增长。", "requirements": "热爱游戏，具备良好的文案能力。", "tags": "社区运营,用户增长,内容运营"},
        {"title": "UI 设计师", "company": "小红书", "city": "上海", "salary_min": 15, "salary_max": 25, "job_type": "设计", "experience": "1-3年", "education": "本科及以上", "description": "负责App界面设计和交互设计。", "requirements": "熟练使用Figma/Sketch，有移动端设计经验。", "tags": "UI设计,交互设计,Figma"},
        {"title": "测试工程师", "company": "华为", "city": "深圳", "salary_min": 18, "salary_max": 30, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责软件测试和质量保障。", "requirements": "熟悉自动化测试框架，有性能测试经验优先。", "tags": "自动化测试,性能测试,质量保障"},
        {"title": "大数据开发工程师", "company": "百度", "city": "北京", "salary_min": 22, "salary_max": 38, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责大数据平台开发和数据处理。", "requirements": "熟悉Hadoop/Spark生态，有海量数据处理经验。", "tags": "大数据,Hadoop,Spark,数据处理"},
        {"title": "DevOps 工程师", "company": "滴滴", "city": "北京", "salary_min": 20, "salary_max": 35, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责CI/CD流水线建设和运维自动化。", "requirements": "熟悉Docker/K8s，有云原生经验优先。", "tags": "DevOps,Docker,K8s,CI/CD"},
        {"title": "安全工程师", "company": "蚂蚁集团", "city": "杭州", "salary_min": 25, "salary_max": 40, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责系统安全评估和漏洞修复。", "requirements": "了解常见安全漏洞和攻防技术。", "tags": "网络安全,渗透测试,安全评估"},
        {"title": "iOS 开发工程师", "company": "苹果中国", "city": "上海", "salary_min": 22, "salary_max": 38, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责iOS应用开发和维护。", "requirements": "熟悉Swift/Objective-C，有App Store上架经验。", "tags": "iOS,Swift,Objective-C"},
        {"title": "Android 开发工程师", "company": "小米", "city": "北京", "salary_min": 18, "salary_max": 30, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责MIUI系统应用开发。", "requirements": "熟悉Kotlin/Java，了解Android Jetpack。", "tags": "Android,Kotlin,Jetpack"},
        {"title": "算法工程师", "company": "商汤科技", "city": "深圳", "salary_min": 28, "salary_max": 50, "job_type": "技术", "experience": "1-3年", "education": "硕士及以上", "description": "负责计算机视觉算法研发。", "requirements": "熟悉CV算法，有顶会论文优先。", "tags": "计算机视觉,深度学习,算法"},
        {"title": "数据工程师", "company": "快手", "city": "北京", "salary_min": 20, "salary_max": 35, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责数据仓库建设和ETL开发。", "requirements": "熟悉SQL和数据建模，有数仓经验优先。", "tags": "数据仓库,ETL,SQL"},
        {"title": "游戏开发工程师", "company": "米哈游", "city": "上海", "salary_min": 22, "salary_max": 40, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责游戏客户端开发。", "requirements": "熟悉Unity/Unreal引擎，有游戏项目经验。", "tags": "游戏开发,Unity,Unreal"},
        {"title": "嵌入式开发工程师", "company": "大疆", "city": "深圳", "salary_min": 20, "salary_max": 35, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责无人机嵌入式系统开发。", "requirements": "熟悉C/C++，了解RTOS。", "tags": "嵌入式,C/C++,RTOS"},
        {"title": "区块链开发工程师", "company": "蚂蚁链", "city": "杭州", "salary_min": 25, "salary_max": 45, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责区块链平台开发。", "requirements": "了解区块链原理，熟悉Solidity/Rust。", "tags": "区块链,智能合约,Solidity"},
        {"title": "数据库工程师", "company": "PingCAP", "city": "北京", "salary_min": 22, "salary_max": 38, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责分布式数据库开发。", "requirements": "熟悉数据库内核，有Go/Rust经验优先。", "tags": "数据库,分布式,Go"},
        {"title": "云原生工程师", "company": "阿里云", "city": "杭州", "salary_min": 25, "salary_max": 42, "job_type": "技术", "experience": "1-3年", "education": "本科及以上", "description": "负责云原生产品研发。", "requirements": "熟悉K8s、Service Mesh等云原生技术。", "tags": "云原生,K8s,Service Mesh"},
    ]

    for job_data in jobs_data:
        JobPosting.objects.get_or_create(
            title=job_data["title"],
            company=job_data["company"],
            defaults=job_data,
        )
    print("[OK] 创建岗位数据 (20条)")

    # 9. 创建职业规划报告
    CareerPlanReport.objects.get_or_create(
        user=demo_user,
        defaults={
            "overall_score": 85.5,
            "summary": "基于您的MBTI（INTJ-A）、霍兰德代码（IAS）和胜任力测评结果，我们对您的职业发展进行了全面分析。您具有较强的逻辑思维能力和创新意识，适合从事需要深度思考和技术钻研的工作。",
            "short_term": "【短期目标：0-6个月】\n\n1. 技术能力夯实\n- 深入学习Python/Java核心技术栈，掌握数据结构与算法\n- 完成2-3个高质量项目，包括一个AI相关的实践项目\n- 参加LeetCode周赛，提升算法能力\n\n2. 工程实践积累\n- 参与开源项目贡献，积累GitHub上的代码提交记录\n- 学习Git工作流、CI/CD流程、代码审查规范\n\n3. 求职准备\n- 完善简历，突出项目经验和技术能力\n- 准备技术面试常见问题\n- 参加校招提前批，积累面试经验",
            "mid_term": "【中期目标：6个月-2年】\n\n1. 专业方向深耕\n- 进入互联网大厂实习（字节跳动/阿里巴巴/腾讯等）\n- 深入学习AI/大数据方向：机器学习、深度学习、大数据处理\n- 参与公司核心项目，积累大型系统开发经验\n\n2. 技术视野拓展\n- 关注前沿技术动态（LLM、AIGC、云原生等）\n- 参加技术社区活动，建立行业人脉\n- 考取相关技术认证\n\n3. 软技能提升\n- 提升技术文档写作能力\n- 学习项目管理基础知识\n- 培养跨团队协作能力",
            "long_term": "【长期目标：2-5年】\n\n1. 技术专家路线\n- 成为AI领域技术专家，具备独立负责大型项目的能力\n- 在技术社区建立个人影响力（技术博客、开源项目）\n- 探索技术管理方向，逐步承担团队管理职责\n\n2. 职业发展路径\n- Year 2-3: 高级工程师 → 技术负责人\n- Year 3-4: 技术专家/架构师\n- Year 4-5: 技术总监/CTO方向发展\n\n3. 持续学习计划\n- 深入研究分布式系统、高并发架构\n- 学习商业思维和产品意识\n- 培养战略规划和决策能力",
        }
    )
    print("[OK] 创建职业规划报告")

    # 10. 创建就业方向
    directions_data = [
        {"name": "AI 算法工程师", "match_score": 92, "market_demand": "高需求", "typical_positions": "机器学习工程师、深度学习工程师、NLP工程师、CV工程师", "reason": "您的创新能力得分最高（88分），配合扎实的编程基础和学习能力，非常适合从事AI算法研发工作。"},
        {"name": "数据分析师", "match_score": 87, "market_demand": "高需求", "typical_positions": "数据分析师、商业分析师、数据产品经理", "reason": "您的问题解决能力突出（82分），具备良好的逻辑思维，适合从数据中挖掘价值。"},
        {"name": "后端开发工程师", "match_score": 83, "market_demand": "稳定需求", "typical_positions": "Java开发工程师、Go开发工程师、Python开发工程师", "reason": "您的学习能力强（85分），适合快速掌握后端技术栈。"},
        {"name": "产品经理", "match_score": 76, "market_demand": "中等需求", "typical_positions": "产品经理、产品总监、增长产品经理", "reason": "您的创新能力和问题解决能力组合适合产品经理岗位。"},
        {"name": "技术架构师", "match_score": 71, "market_demand": "长期需求", "typical_positions": "系统架构师、解决方案架构师、云架构师", "reason": "作为长期发展方向，需要先积累3-5年开发经验。"},
    ]

    for dir_data in directions_data:
        CareerDirection.objects.get_or_create(
            user=demo_user,
            name=dir_data["name"],
            defaults=dir_data,
        )
    print("[OK] 创建就业方向")

    # 11. 创建岗位推荐
    jobs = JobPosting.objects.all()[:12]
    for i, job in enumerate(jobs):
        JobRecommendation.objects.get_or_create(
            user=demo_user,
            job=job,
            defaults={
                "overall_match": 92 - i * 3,
                "major_match": 90 - i * 2,
                "skill_match": 88 - i * 3,
                "interest_match": 85 - i * 4,
                "salary_match": 80 - i * 2,
                "city_match": 75 - i * 3,
            }
        )
    print("[OK] 创建岗位推荐")

    # 12. 创建提升建议
    suggestions_data = [
        {"skill_name": "沟通表达能力", "current_score": 70, "target_score": 85, "learning_path": "从基础沟通技巧开始，逐步提升技术演讲和跨团队协作能力", "recommended_courses": "《高效沟通》- 得到APP、《技术演讲实战》- 极客时间", "recommended_books": "《非暴力沟通》、《关键对话》、《金字塔原理》", "recommended_projects": "主动承担项目汇报、参与技术分享会"},
        {"skill_name": "领导力", "current_score": 65, "target_score": 80, "learning_path": "从项目管理入手，逐步培养团队协调和决策能力", "recommended_courses": "《项目管理实战》- 极客时间、《领导力21法则》- 樊登读书", "recommended_books": "《高效能人士的七个习惯》、《从优秀到卓越》", "recommended_projects": "担任课程项目组长、组织技术学习小组"},
        {"skill_name": "团队协作能力", "current_score": 78, "target_score": 88, "learning_path": "强化协作意识，学习敏捷开发和DevOps文化", "recommended_courses": "《Scrum敏捷实战》- 极客时间", "recommended_books": "《团队协作的五大障碍》、《敏捷开发》", "recommended_projects": "参与大型开源项目协作、组织Hackathon活动"},
    ]

    for sug_data in suggestions_data:
        ImprovementSuggestion.objects.get_or_create(
            user=demo_user,
            skill_name=sug_data["skill_name"],
            defaults=sug_data,
        )
    print("[OK] 创建提升建议")

    # 13. 创建模拟面试记录
    interview, _ = MockInterviewRecord.objects.get_or_create(
        user=demo_user,
        target_job="AI 算法工程师",
        defaults={
            "interview_type": "comprehensive",
            "rounds": 3,
            "overall_score": 82,
            "status": "completed",
            "feedback": "## 面试综合评估\n\n### 整体表现\n您在本次面试中表现良好，展现了扎实的专业基础和清晰的逻辑思维能力。\n\n### 优点\n- 回答问题思路清晰，能够有条理地组织语言\n- 具备良好的学习能力和求知欲\n\n### 待改进\n- 部分回答可以更加具体，加入量化数据\n- 可以更好地运用STAR法则来结构化回答",
        }
    )

    # 创建面试消息
    messages_data = [
        {"role": "ai", "content": "请简单介绍一下你自己，以及你为什么想从事AI算法工程师这个方向？"},
        {"role": "user", "content": "我是华南理工大学软件工程专业的大三学生，对AI和大数据方向有浓厚兴趣。我在校期间参与了多个AI相关项目，包括基于Transformer的情感分析系统和智能推荐系统。我选择AI算法工程师方向是因为我认为AI技术能够真正解决实际问题，创造价值。"},
        {"role": "ai", "content": "很好。请描述一个你在项目中遇到的技术挑战，以及你是如何解决的？", "feedback": "您的自我介绍清晰明了，建议可以加入一些具体的数据或成果来增强说服力。"},
        {"role": "user", "content": "在情感分析项目中，我们遇到了数据不平衡的问题。我通过实现数据增强策略，包括同义词替换和回译等方法，成功将模型性能提升了5%。"},
        {"role": "ai", "content": "你认为AI算法工程师最重要的技能是什么？你在这方面有什么优势？", "feedback": "这个回答很好地展示了您解决问题的能力，建议可以进一步描述您在团队中的角色和贡献。"},
        {"role": "user", "content": "我认为最重要的技能是算法理解和工程实现能力的结合。我在这方面的优势是既有扎实的理论基础，又有实际的项目经验。"},
    ]

    for msg_data in messages_data:
        InterviewMessage.objects.get_or_create(
            interview=interview,
            role=msg_data["role"],
            content=msg_data["content"],
            defaults={"feedback": msg_data.get("feedback", "")},
        )
    print("[OK] 创建模拟面试记录")

    # 14. 创建简历优化报告
    ResumeOptimizationReport.objects.get_or_create(
        user=demo_user,
        target_job="AI 算法工程师",
        defaults={
            "original_resume": "何家齐\n软件工程专业 | 大三在读\n\n教育背景\nXX大学 | 软件工程 | 2022-2026\nGPA: 3.6/4.0\n\n技能\nPython, Java, PyTorch, TensorFlow\n\n项目经历\n1. 情感分析系统\n2. 推荐系统\n\n实习\n字节跳动后端开发实习生",
            "optimized_resume": "# 何家齐\n**求职意向：AI 算法工程师** | 软件工程专业 | 大三在读\n\n## 教育背景\n**XX大学** | 软件工程专业 | 2022.09 - 2026.06（预计）\n- GPA: 3.6/4.0（专业前15%）\n- 相关课程：机器学习、深度学习、数据结构与算法\n\n## 专业技能\n- **编程语言**：Python（熟练）、Java（熟练）\n- **AI/ML框架**：PyTorch、TensorFlow、Scikit-learn\n- **开发工具**：Git、Docker、Linux、MySQL\n\n## 项目经历\n### 1. 基于Transformer的文本情感分析系统 | 项目负责人\n- 使用PyTorch实现基于BERT的情感分析模型，准确率92%\n- 设计数据增强策略，模型性能提升5%\n\n### 2. 智能推荐系统 | 核心开发者\n- 设计协同过滤算法，支撑日均10万+请求\n- Redis缓存优化，响应时间从200ms降至50ms\n\n## 实习经历\n**字节跳动** | 后端开发实习生 | 2024.07-2024.09\n- 参与抖音推荐系统后端开发\n- 优化数据处理管道，效率提升30%",
            "suggestions": "1. 突出AI相关经验：将AI/ML技能放在更突出位置\n2. 量化项目成果：加入更多量化数据\n3. 强化技术深度：描述更多技术细节\n4. 优化关键词覆盖：包含JD中的关键词\n5. 调整经历顺序：最相关的经历放前面\n6. 补充研究成果：如有论文或技术博客单独列出",
            "overall_score": 88,
            "keyword_coverage": 85.5,
            "status": "completed",
        }
    )
    print("[OK] 创建简历优化报告")

    # 15. 创建系统日志
    logs_data = [
        {"level": "info", "action": "用户登录", "detail": "用户 demo_student 登录系统"},
        {"level": "info", "action": "生成用户画像", "detail": "用户 demo_student 生成了MBTI测评结果"},
        {"level": "info", "action": "生成职业规划", "detail": "用户 demo_student 生成了职业规划报告"},
        {"level": "info", "action": "模拟面试", "detail": "用户 demo_student 完成了一次模拟面试"},
        {"level": "info", "action": "简历优化", "detail": "用户 demo_student 提交了简历优化请求"},
    ]

    for log_data in logs_data:
        SystemLog.objects.create(**log_data)
    print("[OK] 创建系统日志")

    print("\n演示数据灌入完成！")
    print(f"演示账号: demo_student / demo1234")
    print(f"管理员账号: admin / admin1234")


if __name__ == "__main__":
    seed()
