"""
LLM 服务抽象层
支持 Mock 和 OpenAI 兼容 API 两种模式
"""

import json
import os
from abc import ABC, abstractmethod
from django.conf import settings


class LLMService(ABC):
    """LLM 服务抽象基类"""

    @abstractmethod
    def generate_career_plan(self, user_id: int) -> dict:
        """生成职业规划报告"""
        pass

    @abstractmethod
    def generate_career_directions(self, user_id: int) -> list:
        """生成就业方向推荐"""
        pass

    @abstractmethod
    def generate_improvement_suggestions(self, user_id: int) -> list:
        """生成提升建议"""
        pass

    @abstractmethod
    def generate_interview_question(self, job: str, interview_type: str, round_num: int) -> str:
        """生成面试题"""
        pass

    @abstractmethod
    def generate_interview_feedback(self, answer: str) -> str:
        """生成面试反馈"""
        pass

    @abstractmethod
    def generate_interview_evaluation(self, interview_id: int) -> dict:
        """生成面试评估报告"""
        pass

    @abstractmethod
    def optimize_resume(self, resume: str, target_job: str) -> dict:
        """优化简历"""
        pass


class MockLLMService(LLMService):
    """Mock LLM 服务 - 返回预置的高质量中文内容"""

    def generate_career_plan(self, user_id: int) -> dict:
        return {
            "overall_score": 85.5,
            "summary": "基于您的 MBTI（INTJ-A）、霍兰德代码（IAS）和胜任力测评结果，我们对您的职业发展进行了全面分析。您具有较强的逻辑思维能力和创新意识，适合从事需要深度思考和技术钻研的工作。建议您在夯实技术基础的同时，注重团队协作和沟通能力的提升。",
            "short_term": """【短期目标：0-6个月】

1. 技术能力夯实
   - 深入学习 Python/Java 核心技术栈，掌握数据结构与算法
   - 完成 2-3 个高质量项目，包括一个 AI 相关的实践项目
   - 参加 LeetCode 周赛，提升算法能力至 1800+ rating

2. 工程实践积累
   - 参与开源项目贡献，积累 GitHub 上的代码提交记录
   - 学习 Git 工作流、CI/CD 流程、代码审查规范
   - 掌握 Docker 容器化部署基础

3. 求职准备
   - 完善简历，突出项目经验和技术能力
   - 准备技术面试常见问题（操作系统、计算机网络、数据库）
   - 参加校招提前批，积累面试经验""",
            "mid_term": """【中期目标：6个月-2年】

1. 专业方向深耕
   - 进入互联网大厂实习（字节跳动/阿里巴巴/腾讯等）
   - 深入学习 AI/大数据方向：机器学习、深度学习、大数据处理
   - 参与公司核心项目，积累大型系统开发经验

2. 技术视野拓展
   - 关注前沿技术动态（LLM、AIGC、云原生等）
   - 参加技术社区活动，建立行业人脉
   - 考取相关技术认证（AWS/Azure 云计算认证）

3. 软技能提升
   - 提升技术文档写作能力
   - 学习项目管理基础知识
   - 培养跨团队协作能力""",
            "long_term": """【长期目标：2-5年】

1. 技术专家路线
   - 成为 AI 领域技术专家，具备独立负责大型项目的能力
   - 在技术社区建立个人影响力（技术博客、开源项目）
   - 探索技术管理方向，逐步承担团队管理职责

2. 职业发展路径
   - Year 2-3: 高级工程师 → 技术负责人
   - Year 3-4: 技术专家/架构师
   - Year 4-5: 技术总监/CTO 方向发展

3. 持续学习计划
   - 深入研究分布式系统、高并发架构
   - 学习商业思维和产品意识
   - 培养战略规划和决策能力""",
        }

    def generate_career_directions(self, user_id: int) -> list:
        return [
            {
                "name": "AI 算法工程师",
                "match_score": 92,
                "market_demand": "高需求",
                "typical_positions": "机器学习工程师、深度学习工程师、NLP工程师、CV工程师",
                "reason": "您的创新能力得分最高（88分），配合扎实的编程基础和学习能力，非常适合从事AI算法研发工作。当前大模型时代，AI人才需求旺盛，薪资待遇优厚。"
            },
            {
                "name": "数据分析师",
                "match_score": 87,
                "market_demand": "高需求",
                "typical_positions": "数据分析师、商业分析师、数据产品经理",
                "reason": "您的问题解决能力突出（82分），具备良好的逻辑思维，适合从数据中挖掘价值。数据分析是各行业都需要的核心岗位，职业发展空间广阔。"
            },
            {
                "name": "后端开发工程师",
                "match_score": 83,
                "market_demand": "稳定需求",
                "typical_positions": "Java开发工程师、Go开发工程师、Python开发工程师",
                "reason": "您的学习能力强（85分），适合快速掌握后端技术栈。后端开发是互联网行业的基础岗位，技术成熟，晋升路径清晰。"
            },
            {
                "name": "产品经理",
                "match_score": 76,
                "market_demand": "中等需求",
                "typical_positions": "产品经理、产品总监、增长产品经理",
                "reason": "您的创新能力和问题解决能力组合适合产品经理岗位。建议在提升沟通能力（当前70分）后考虑此方向。"
            },
            {
                "name": "技术架构师",
                "match_score": 71,
                "market_demand": "长期需求",
                "typical_positions": "系统架构师、解决方案架构师、云架构师",
                "reason": "作为长期发展方向，需要先积累3-5年开发经验。您的技术视野和学习能力为此奠定了良好基础。"
            },
        ]

    def generate_improvement_suggestions(self, user_id: int) -> list:
        return [
            {
                "skill_name": "沟通表达能力",
                "current_score": 70,
                "target_score": 85,
                "learning_path": "从基础沟通技巧开始，逐步提升技术演讲和跨团队协作能力",
                "recommended_courses": "《高效沟通》- 得到APP、《技术演讲实战》- 极客时间、TED 演讲技巧学习",
                "recommended_books": "《非暴力沟通》、《关键对话》、《金字塔原理》",
                "recommended_projects": "主动承担项目汇报、参与技术分享会、加入辩论社或演讲俱乐部"
            },
            {
                "skill_name": "领导力",
                "current_score": 65,
                "target_score": 80,
                "learning_path": "从项目管理入手，逐步培养团队协调和决策能力",
                "recommended_courses": "《项目管理实战》- 极客时间、《领导力21法则》- 樊登读书、MBA 核心课程",
                "recommended_books": "《高效能人士的七个习惯》、《从优秀到卓越》、《领导力》",
                "recommended_projects": "担任课程项目组长、组织技术学习小组、参与学生会或社团管理"
            },
            {
                "skill_name": "团队协作能力",
                "current_score": 78,
                "target_score": 88,
                "learning_path": "强化协作意识，学习敏捷开发和DevOps文化",
                "recommended_courses": "《Scrum敏捷实战》- 极客时间、《团队协作的艺术》- Coursera",
                "recommended_books": "《团队协作的五大障碍》、《敏捷开发》、《持续交付》",
                "recommended_projects": "参与大型开源项目协作、组织Hackathon活动、实践结对编程"
            },
        ]

    def generate_interview_question(self, job: str, interview_type: str, round_num: int) -> str:
        questions = {
            "behavioral": [
                "请介绍一下你最有成就感的一个项目经历，在这个项目中你遇到了什么挑战，是如何克服的？",
                "描述一次你在团队中遇到意见分歧的经历，你是如何处理的？",
                "请分享一个你在时间紧迫的情况下完成任务的经历，你是如何管理时间和优先级的？",
                "谈谈你在学习新技术时的方法和策略，能举一个具体的例子吗？",
                "描述一次你主动发现问题并解决的经历，这个问题的影响是什么？",
                "请分享一个你需要向非技术人员解释复杂技术概念的经历。",
                "谈谈你在面对失败或挫折时的应对方式，能举一个具体例子吗？",
                "描述一次你需要在多个任务之间切换的经历，你是如何保持效率的？",
            ],
            "technical": [
                f"请解释一下你对{job}这个岗位核心技能的理解，你目前掌握了哪些？",
                "请描述一下你对微服务架构的理解，它的优缺点是什么？",
                "解释一下 RESTful API 的设计原则，你在项目中是如何应用的？",
                "谈谈你对数据库索引的理解，什么时候应该使用索引，什么时候不应该？",
                "请解释一下 Python 中的装饰器是什么，你能举一个实际应用场景吗？",
                "描述一下你了解的设计模式，能举一个你在项目中使用过的例子吗？",
                "请解释一下什么是死锁，如何避免死锁？",
                "谈谈你对容器化技术（Docker）的理解，它解决了什么问题？",
            ],
            "comprehensive": [
                f"请简单介绍一下你自己，以及你为什么想从事{job}这个方向？",
                "你认为自己最大的优势和不足分别是什么？你打算如何改进？",
                "如果你入职后发现实际工作内容与预期不符，你会怎么处理？",
                "谈谈你对未来3-5年职业发展的规划。",
                "你如何看待加班文化？你认为工作效率和工作时长的关系是什么？",
                "如果你和上级在技术方案上有分歧，你会如何处理？",
                "你最近关注的技术趋势是什么？你认为它会如何影响行业？",
                "请描述一下你理想中的工作环境和团队文化。",
            ],
        }
        type_questions = questions.get(interview_type, questions["comprehensive"])
        index = (round_num - 1) % len(type_questions)
        return type_questions[index]

    def generate_interview_feedback(self, answer: str) -> str:
        return "您的回答整体思路清晰，能够结合具体经历来阐述。建议在回答时更加突出您的个人贡献和具体成果，使用 STAR 法则（情境-任务-行动-结果）来组织答案会更加结构化。同时可以适当加入一些量化的数据来增强说服力。"

    def generate_interview_evaluation(self, interview_id: int) -> dict:
        return {
            "overall_score": 82,
            "feedback": """## 面试综合评估

### 整体表现
您在本次面试中表现良好，展现了扎实的专业基础和清晰的逻辑思维能力。

### 优点
- 回答问题思路清晰，能够有条理地组织语言
- 具备良好的学习能力和求知欲
- 对技术有热情，能够结合实际项目经验来回答

### 待改进
- 部分回答可以更加具体，加入量化数据
- 可以更好地运用 STAR 法则来结构化回答
- 在描述团队协作经历时，可以更突出个人贡献

### 面试建议
1. 准备更多具体案例，特别是有数据支撑的成功经历
2. 练习在限定时间内精炼地表达核心观点
3. 对目标岗位的技术栈做更深入的研究""",
        }

    def optimize_resume(self, resume: str, target_job: str) -> dict:
        return {
            "optimized_resume": """# 何家齐
**求职意向：AI 算法工程师** | 软件工程专业 | 大三在读

## 教育背景
**XX大学** | 软件工程专业 | 2022.09 - 2026.06（预计）
- GPA: 3.6/4.0（专业前15%）
- 相关课程：机器学习、深度学习、数据结构与算法、操作系统、计算机网络

## 专业技能
- **编程语言**：Python（熟练）、Java（熟练）、C++（了解）
- **AI/ML框架**：PyTorch、TensorFlow、Scikit-learn、Hugging Face
- **开发工具**：Git、Docker、Linux、MySQL、Redis
- **其他**：熟悉常见的机器学习算法，了解大语言模型原理

## 项目经历

### 1. 基于 Transformer 的文本情感分析系统 | 项目负责人
**2024.03 - 2024.06**
- 使用 PyTorch 实现基于 BERT 的情感分析模型，在 Yelp 数据集上达到 92% 准确率
- 设计并实现了数据增强策略，将模型性能提升 5%
- 撰写技术文档，进行团队内部技术分享

### 2. 智能推荐系统设计与实现 | 核心开发者
**2023.09 - 2023.12**
- 参与设计基于协同过滤的推荐算法，支撑日均 10 万+ 请求
- 使用 Redis 缓存优化推荐接口响应时间，从 200ms 降至 50ms
- 负责推荐效果评估模块开发，实现 A/B 测试框架

### 3. 个人技术博客系统 | 独立开发者
**2023.06 - 2023.08**
- 使用 Vue 3 + Django 开发全栈博客系统，支持 Markdown 渲染和代码高亮
- 实现文章搜索功能（基于 Elasticsearch），支持中文分词
- 项目获得 200+ GitHub Star

## 实习经历
**字节跳动** | 后端开发实习生 | 2024.07 - 2024.09
- 参与抖音推荐系统后端开发，负责特征工程模块
- 优化数据处理管道，处理效率提升 30%
- 获得"优秀实习生"评价

## 荣誉奖项
- 2024 年全国大学生数学建模竞赛省级一等奖
- 2023 年校级程序设计大赛银奖
- 连续两年获得校级奖学金""",
            "suggestions": """## 简历优化建议

### 1. 突出 AI 相关经验
**建议**：在专业技能部分，将 AI/ML 相关内容放在更突出的位置
**原因**：目标岗位是 AI 算法工程师，需要让招聘者一眼看到相关技能

### 2. 量化项目成果
**建议**：在项目经历中加入更多量化数据
**原因**：量化成果能让招聘者更直观地评估你的贡献和能力

### 3. 强化技术深度描述
**建议**：在项目描述中加入更多技术细节
**原因**：展示你对技术的深入理解，而非只是表面使用

### 4. 优化关键词覆盖
**建议**：确保简历包含目标岗位 JD 中的关键词
**原因**：很多公司使用 ATS 系统筛选简历，关键词匹配度很重要

### 5. 调整经历顺序
**建议**：将最相关的经历放在前面
**原因**：招聘者通常只花 30 秒扫描简历，需要快速抓住注意力

### 6. 补充研究成果
**建议**：如有论文或技术博客，建议单独列出
**原因**：对于算法岗位，学术能力和技术输出是重要的加分项""",
            "overall_score": 88,
            "keyword_coverage": 85.5,
        }


class OpenAICompatibleLLMService(LLMService):
    """OpenAI 兼容 API 的 LLM 服务"""

    def __init__(self):
        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=os.getenv("LLM_API_KEY", ""),
                base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
            )
            self.model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        except ImportError:
            raise ImportError("请安装 openai 包: pip install openai")

    def _chat(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

    def generate_career_plan(self, user_id: int) -> dict:
        system_prompt = "你是一位专业的职业规划师，为大学生提供职业规划建议。请以JSON格式返回。"
        user_prompt = f"请为用户ID={user_id}生成职业规划报告，包含overall_score, summary, short_term, mid_term, long_term字段。"
        result = self._chat(system_prompt, user_prompt)
        return json.loads(result)

    def generate_career_directions(self, user_id: int) -> list:
        system_prompt = "你是一位专业的职业规划师，请推荐5个就业方向。"
        user_prompt = f"请为用户ID={user_id}推荐5个就业方向，每个包含name, match_score, market_demand, typical_positions, reason字段。返回JSON数组。"
        result = self._chat(system_prompt, user_prompt)
        return json.loads(result)

    def generate_improvement_suggestions(self, user_id: int) -> list:
        system_prompt = "你是一位专业的职业规划师，请提供能力提升建议。"
        user_prompt = f"请为用户ID={user_id}提供3个最需要提升的技能建议，每个包含skill_name, current_score, target_score, learning_path, recommended_courses, recommended_books, recommended_projects字段。返回JSON数组。"
        result = self._chat(system_prompt, user_prompt)
        return json.loads(result)

    def generate_interview_question(self, job: str, interview_type: str, round_num: int) -> str:
        system_prompt = "你是一位专业的面试官。"
        user_prompt = f"请为{job}岗位生成一道{interview_type}面试题，这是第{round_num}轮。直接返回问题文本。"
        return self._chat(system_prompt, user_prompt)

    def generate_interview_feedback(self, answer: str) -> str:
        system_prompt = "你是一位专业的面试官，请对候选人的回答给出反馈。"
        user_prompt = f"请对以下回答给出反馈和改进建议：\n{answer}"
        return self._chat(system_prompt, user_prompt)

    def generate_interview_evaluation(self, interview_id: int) -> dict:
        system_prompt = "你是一位专业的面试官，请生成面试评估报告。"
        user_prompt = f"请为面试ID={interview_id}生成评估报告，包含overall_score和feedback字段。返回JSON。"
        result = self._chat(system_prompt, user_prompt)
        return json.loads(result)

    def optimize_resume(self, resume: str, target_job: str) -> dict:
        system_prompt = "你是一位专业的简历优化顾问。"
        user_prompt = f"请优化以下简历，目标岗位是{target_job}。返回JSON格式，包含optimized_resume, suggestions, overall_score, keyword_coverage字段。\n\n原始简历：\n{resume}"
        result = self._chat(system_prompt, user_prompt)
        return json.loads(result)


def get_llm_service() -> LLMService:
    """获取 LLM 服务实例"""
    provider = os.getenv("LLM_PROVIDER", "mock")
    if provider == "openai":
        return OpenAICompatibleLLMService()
    return MockLLMService()
