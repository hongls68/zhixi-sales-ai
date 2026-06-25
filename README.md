# 智析销售AI - 智能销售分析平台

> 基于AI的销售对话分析平台，帮助销售团队提升效率和转化率。
> 本地AI优先，API兜底，零成本开发。

## 📋 版本历史

| 版本 | 日期 | 更新内容 | 状态 |
|------|------|----------|------|
| v1.0 | 2026-06-24 | 基础框架：7个页面、登录注册、Mock数据 | ✅ 完成 |
| v1.1 | 2026-06-24 | 交互优化：Toast、动画、骨架屏、表单验证 | ✅ 完成 |
| v1.2 | 2026-06-24 | 功能补全：搜索筛选、分页、分析列表页 | ✅ 完成 |
| v1.3 | 2026-06-24 | 数据可视化：Chart.js、趋势图、评分环形图 | ✅ 完成 |
| **v1.4** | 2026-06-25 | **前后端重构 + AI集成** | ✅ 完成 |
| v1.5 | - | PDF导出功能 | ⏳ 待实施 |
| v1.6 | - | 响应式适配（移动端） | ⏳ 待实施 |

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
│   ├── login.html                 # 登录
│   ├── register.html              # 注册
│   ├── dashboard.html             # 工作台
│   ├── history.html               # 分析列表
│   ├── analysis.html              # 分析详情
│   ├── team.html                  # 团队协作
│   ├── profile.html               # 个人中心
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
│   │   └── user.py
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

## 🤖 AI配置

### 本地优先策略

```env
# AI策略：local_first（本地优先）或 api_only（只用API）
AI_STRATEGY=local_first

# 本地模型（Ollama）
LOCAL_MODEL_TYPE=ollama
LOCAL_MODEL_URL=http://localhost:11434
LOCAL_MODEL_NAME=qwen2.5:14b

# API兜底（DeepSeek）
DEEPSEEK_API_KEY=your-api-key
DEEPSEEK_MODEL=deepseek-chat
```

### 模型选择建议

| 场景 | 推荐 | 成本 |
|------|------|------|
| 开发测试 | Ollama + 小模型 | 免费 |
| 本地部署 | Ollama + 大模型 | 免费 |
| 云端部署 | DeepSeek API | 便宜 |
| 混合策略 | 本地优先+API兜底 | 最优 |

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
