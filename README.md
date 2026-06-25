# 智析销售AI - 智能销售分析平台

> 基于AI的销售对话分析平台，帮助销售团队提升效率和转化率。
> 核心能力：AI驱动的销售对话分析

## 📋 版本历史

| 版本 | 日期 | 更新内容 | 状态 |
|------|------|----------|------|
| v1.0-v1.4 | 2026-06-24~25 | 基础框架、交互优化、功能补全、数据可视化、前后端重构 | ✅ 完成 |
| v1.4.1 | 2026-06-25 | 登录优化：支持手机号/用户名登录 | ✅ 完成 |
| **v2.0** | **2026-06-25** | **AI核心能力：接入API、销售分析提示词、反馈机制** | ✅ 完成 |
| v2.1 | - | 提示词优化：行业/角色/场景定制 | ⏳ 待实施 |
| v2.2 | - | PDF导出功能 | ⏳ 待实施 |
| v2.3 | - | 响应式适配（移动端） | ⏳ 待实施 |

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                      前端 (port 5500)                     │
│         HTML + CSS + JavaScript (静态文件)                │
└─────────────────────────────────────────────────────────┘
                            ↓ API
┌─────────────────────────────────────────────────────────┐
│                    后端 (port 8000)                       │
│              Python FastAPI + SQLite                     │
│                                                          │
│  ┌─────────────────────────────────────────────────────┐│
│  │                   AI 服务                            ││
│  │  优先：本地模型（Ollama/LM Studio）免费              ││
│  │  兜底：DeepSeek API（便宜）                         ││
│  └─────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────┐│
│  │                 Whisper 转写                         ││
│  │  本地运行，零成本                                    ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

---

## 📁 项目结构

```
Smart Analysis/
│
├── frontend/                      # 前端
│   ├── index.html                 # 首页
│   ├── login.html                 # 登录（手机号+密码）
│   ├── register.html              # 注册（手机号+验证码+密码）
│   ├── dashboard.html             # 工作台
│   ├── history.html               # 分析列表
│   ├── analysis.html              # 分析详情
│   ├── team.html                  # 团队协作
│   ├── profile.html               # 个人中心
│   ├── admin.html                 # 管理员后台（仅管理员可见）
│   │
│   └── static/
│       ├── css/style.css
│       └── js/
│           ├── auth.js            # 认证
│           ├── api.js             # API（支持Mock/真实API切换）
│           ├── utils.js
│           └── pagination.js
│
├── backend/                       # 后端
│   ├── main.py                    # FastAPI入口
│   ├── config.py                  # 配置管理
│   ├── database.py                # SQLite
│   │
│   ├── services/
│   │   ├── ai_service.py          # AI服务（本地优先）
│   │   ├── whisper_service.py     # Whisper转写
│   │   └── auth_service.py        # JWT认证
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── analysis.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── analysis.py
│   │   ├── user.py
│   │   └── admin.py               # 管理员接口
│   │
│   ├── prompts/
│   │   └── sales.py               # 提示词模板
│   │
│   └── requirements.txt
│
├── .env.example                   # 环境变量示例
├── .gitignore
├── README.md
│
├── start-backend.bat              # 启动后端
├── start-frontend.bat             # 启动前端
└── init-git.bat                   # Git初始化
```

---

## 🚀 快速开始

### 方式一：使用启动脚本（推荐）

**启动后端：** 双击 `start-backend.bat`

**启动前端：** 双击 `start-frontend.bat`

### 方式二：手动启动

**终端1 - 启动后端：**
```bash
cd backend
pip install -r requirements.txt
python main.py
# 访问 http://localhost:8000
# API文档 http://localhost:8000/docs
```

**终端2 - 启动前端：**
```bash
cd frontend
python -m http.server 5500
# 访问 http://localhost:5500
```

---

## 🔐 测试账号

| 账号 | 手机号 | 密码 | 角色 |
|------|--------|------|------|
| 管理员 | admin | admin123 | admin |
| 普通用户 | 13800138000 | 任意6位+ | user |

**注册新用户：**
- 验证码：`123456`（Mock模式）
- 密码：至少6位

**管理员后台：**
- 登录管理员账号后，左侧菜单显示「管理后台」
- 包含：DAU、WAU、用户管理、分析记录

---

## 🔐 登录方式

### 支持的登录方式

| 登录方式 | 格式 | 说明 |
|----------|------|------|
| 手机号 | 13800138000 | 11位数字，1开头 |
| 用户名 | test1234 | 4-20位字母+数字 |

### 注册说明

| 字段 | 必填 | 格式 |
|------|------|------|
| 手机号 | ✅ 是 | 11位数字 |
| 验证码 | ✅ 是 | 6位数字（Mock：123456） |
| 密码 | ✅ 是 | 至少6位 |
| 用户名 | ❌ 否 | 4-20位字母+数字 |
| 邮箱 | ❌ 否 | 标准邮箱格式 |

---

## 🤖 AI配置

### 当前配置（v2.0）

```env
# AI提供商：api（兼容OpenAI）或 ollama（本地）
AI_PROVIDER=api

# 兼容OpenAI的API配置
API_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1
API_KEY=your-api-key
API_MODEL=deepseek-chat
```

### 支持的AI提供商

| 提供商 | 说明 | 成本 |
|--------|------|------|
| 兼容OpenAI API | 当前使用，兼容OpenAI格式 | 按量计费 |
| Ollama本地 | 本地运行，零成本 | 免费 |
| DeepSeek API | 官方API | 便宜 |

### 提示词架构

```
prompts/sales.py
├── BASE_PROMPT         # 基础销售分析提示词
├── INDUSTRY_PROMPTS    # 行业扩展（教育/软件/金融/电商）
└── ROLE_PROMPTS        # 角色扩展（销售员/经理/创业者）
```

---

## 📝 测试账号

**验证码：** `123456`（任意手机号）

**测试流程：**
1. 打开 http://localhost:5500
2. 点击「登录」
3. 输入手机号（如 13800138000）
4. 输入验证码 123456
5. 登录成功

---

## 🔧 开发说明

### 切换Mock/API模式

编辑 `frontend/static/js/api.js`：
```javascript
var USE_API = false; // false=Mock模式，true=连接后端
```

### 查看API文档

启动后端后访问：http://localhost:8000/docs

---

## 📄 许可证

MIT License
