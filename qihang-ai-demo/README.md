# 启航AI - 大学生职业生涯规划系统

> 基于 Vue 3 + Django + 大模型的大学生职业生涯规划全栈应用，UML 大作业项目。

## 项目简介

「启航AI」是一套面向在校大学生的智能职业生涯规划系统。系统依托大语言模型（LLM），通过多维度测评（MBTI 性格测试、霍兰德职业兴趣测试、胜任力评估）生成精准的用户画像，并结合行业数据为用户提供个性化的职业规划方案。

温馨提示：本项目为大学课程作业，重设计轻代码，数据和功能均为演示性质，不涉及真实用户信息或商业用途。

### 核心亮点

- **AI 驱动**：基于大模型生成个性化职业规划、模拟面试、简历优化等内容
- **多维画像**：集成 MBTI、霍兰德、胜任力三大测评体系，雷达图可视化
- **完整闭环**：从用户画像 → 职业方向 → 岗位推荐 → 技能提升 → 模拟面试 → 简历优化，覆盖求职全链路
- **双模 LLM**：内置 Mock 模式可离线演示，也支持接入任意 OpenAI 兼容 API

### 功能模块

| 模块 | 说明 |
|------|------|
| 登录认证 | 用户名密码登录，Token 认证机制 |
| 用户信息 | 基础信息（学校/专业/GPA）+ 实习/项目/竞赛经历 CRUD |
| 用户画像 | MBTI / 霍兰德 / 胜任力三项测评 + 雷达图展示 |
| 招聘信息 | 20 条预置大厂岗位数据，支持筛选与收藏 |
| 职业规划 | **核心模块**：短/中/长期职业规划时间轴、5 大就业方向推荐、岗位多维匹配推荐、技能提升建议、模拟面试（AI 对话）、简历优化 |
| 系统管理 | 用户管理、数据统计看板、系统日志 |

### 演示账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 普通用户 | `demo_student` | `demo1234` |
| 管理员 | `admin` | `admin1234` |

---

## 技术栈

### 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue 3 | 3.5 | 前端框架（Composition API + `<script setup>`） |
| Vite | 8 | 构建工具 |
| TypeScript | 6 | 类型安全 |
| Pinia | 3 | 状态管理 |
| Vue Router | 4.6 | 路由（含导航守卫） |
| Element Plus | 2.14 | UI 组件库（自动导入） |
| ECharts | 6.1 | 图表（雷达图等） |
| Axios | 1.16 | HTTP 客户端 |
| html2pdf.js | 0.14 | PDF 导出 |

### 后端

| 技术 | 版本 | 用途 |
|------|------|------|
| Django | 4.x | Web 框架 |
| Django REST Framework | 3.14 | RESTful API |
| SQLite | - | 数据库（零配置，开箱即用） |
| django-cors-headers | 4.3 | 跨域支持 |
| python-dotenv | 1.0 | 环境变量管理 |
| openai | - | LLM API 客户端（可选） |

---

## 快速启动

### 环境要求

- **Python** 3.10+
- **Node.js** 18+（推荐 20 LTS）
- **npm** 9+

### 1. 克隆项目

```bash
git clone https://github.com/MaxEnergy666/UML-Major-Project.git
cd UML-Major-Project/qihang-ai-demo
```

### 2. 启动后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
# Windows 激活虚拟环境
venv\Scripts\activate
# macOS/Linux 激活虚拟环境
# source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化演示数据（首次运行必须执行，可重复执行）
python seed.py

# 启动 Django 开发服务器
python manage.py runserver
```

后端将运行在 http://localhost:8000

### 3. 启动前端

打开**新的终端窗口**：

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将运行在 http://localhost:3000

### 4. 访问系统

打开浏览器访问 http://localhost:3000，使用演示账号登录即可。

---

## LLM 配置（可选）

系统默认使用 **Mock 模式**，内置了丰富的模拟回复内容，无需任何外部 API 即可完整体验所有功能。

如需接入真实大模型，可通过环境变量配置（在 `backend/` 目录下创建 `.env` 文件）：

```env
LLM_PROVIDER=openai
LLM_API_KEY=your-api-key-here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-3.5-turbo
```

支持所有 OpenAI 兼容的 API 服务（如 DeepSeek、通义千问、文心一言等）。

---

## 项目结构

```
qihang-ai-demo/
├── README.md                           # 项目文档
├── backend/                            # 后端（Django）
│   ├── manage.py                       # Django 入口
│   ├── db.sqlite3                      # SQLite 数据库（预置数据）
│   ├── requirements.txt                # Python 依赖
│   ├── seed.py                         # 演示数据初始化脚本
│   ├── qihang/                         # Django 工程配置
│   │   ├── settings.py                 # 数据库/DRF/CORS/时区等配置
│   │   └── urls.py                     # 根路由
│   ├── accounts/                       # 登录认证 & 用户模型
│   ├── profiles/                       # 用户画像 & 测评结果
│   ├── jobs/                           # 招聘岗位 & 收藏
│   ├── career/                         # 职业规划（核心模块）
│   ├── admin_panel/                    # 系统管理
│   └── services/
│       └── llm_service.py              # LLM 抽象层（Mock + OpenAI 双实现）
└── frontend/                           # 前端（Vue 3）
    ├── package.json                    # 依赖配置
    ├── vite.config.ts                  # Vite 配置（端口/代理/别名）
    └── src/
        ├── main.ts                     # 应用入口
        ├── App.vue                     # 根组件
        ├── api/                        # Axios 实例 & 请求拦截
        ├── router/                     # 路由配置 & 导航守卫
        ├── stores/                     # Pinia 状态管理
        ├── layouts/                    # 布局组件（侧边栏/顶栏）
        ├── components/                 # 公共组件
        ├── views/                      # 页面视图
        │   ├── auth/                   #   登录页
        │   ├── profile/                #   用户信息 & 画像
        │   ├── jobs/                   #   招聘信息
        │   ├── career/                 #   职业规划（6 个子页面）
        │   └── admin/                  #   系统管理
        └── styles/                     # 全局样式
```

---

## API 接口

所有接口统一前缀 `/api/`，采用 Token 认证（`Authorization: Token <token>`）。

| 模块 | 路径前缀 | 主要接口 |
|------|----------|----------|
| 认证 | `/api/auth/` | `POST /login/`、`GET /me/` |
| 画像 | `/api/profiles/` | 用户资料、经历、测评结果 CRUD |
| 岗位 | `/api/jobs/` | 岗位列表（筛选/收藏） |
| 规划 | `/api/career/` | 职业规划、方向推荐、岗位推荐、提升建议、模拟面试、简历优化 |
| 管理 | `/api/admin/` | 用户管理、统计数据、系统日志 |

---

## 数据模型

系统包含 5 个 Django App，共 14 个数据模型：

- **accounts**: `User`（扩展 AbstractUser，增加 phone/role/is_verified）
- **profiles**: `UserProfile`、`Experience`、`MBTIResult`、`HollandResult`、`CompetencyResult`
- **jobs**: `JobPosting`、`JobFavorite`
- **career**: `CareerPlanReport`、`CareerDirection`、`JobRecommendation`、`ImprovementSuggestion`、`MockInterviewRecord`、`InterviewMessage`、`ResumeOptimizationReport`
- **admin_panel**: `SystemLog`

---

## 常见问题

### Q: 后端启动报错 `No module named 'django'`
A: 确保已激活虚拟环境并执行 `pip install -r requirements.txt`。

### Q: 前端页面空白或接口报错
A: 确保后端服务已启动（默认 http://localhost:8000），前端 Vite 会自动代理 `/api` 请求到后端。

### Q: 如何重新初始化数据？
A: 直接重新运行 `python seed.py`，脚本使用 `get_or_create`，可安全重复执行。

### Q: 如何切换到真实大模型？
A: 在 `backend/` 目录创建 `.env` 文件，配置 `LLM_PROVIDER=openai` 及对应的 API Key、Base URL、Model。详见上方「LLM 配置」章节。

### Q: `db.sqlite3` 文件是否需要提交到 Git？
A: 对于演示项目可以包含，便于克隆后直接使用。生产环境建议加入 `.gitignore`。

---

## 截图清单

> 以下为功能截图占位，运行项目后替换为实际截图。

1. **登录页** → 太空主题动画登录界面
2. **Dashboard** → 雷达图概览 + 统计卡片
3. **用户信息页** → 基础信息 + 经历列表
4. **用户画像页** → MBTI / 霍兰德 / 胜任力测评 + 雷达图
5. **招聘信息页** → 岗位列表 + 筛选 + 收藏
6. **职业规划页** → 短/中/长期时间轴
7. **就业方向推荐页** → 5 张方向卡片 + 匹配度
8. **岗位推荐页** → 列表 + 多维匹配度
9. **提升建议页** → 雷达对比图 + Top-3 待提升技能
10. **模拟面试页** → 配置 → AI 对话 → 评估报告
11. **简历优化页** → 上传 → 三栏对比 → 评分
12. **系统管理页** → 用户列表 / 数据统计 / 系统日志

---

## License

本项目为大学课程作业，仅供学习交流使用。
