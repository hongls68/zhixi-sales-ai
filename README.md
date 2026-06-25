# 智析销售AI - 智能销售分析平台

> 基于AI的销售对话分析平台，帮助销售团队提升效率和转化率。

## 📋 版本历史

| 版本 | 日期 | 更新内容 | 状态 |
|------|------|----------|------|
| v1.0 | 2026-06-24 | 基础框架：7个页面、登录注册、Mock数据 | ✅ 完成 |
| v1.1 | 2026-06-24 | 交互优化：Toast、动画、骨架屏、表单验证 | ✅ 完成 |
| v1.2 | 2026-06-24 | 功能补全：搜索筛选、分页、分析列表页 | ✅ 完成 |
| v1.3 | 2026-06-24 | 数据可视化：Chart.js、趋势图、评分环形图、关键词柱状图 | ✅ 完成 |
| v1.4 | - | PDF导出：html2pdf.js、章节选择 | ⏳ 待实施 |
| v1.5 | - | 响应式完善：移动端适配、底部导航 | ⏳ 待实施 |
| v1.6 | - | 后端对接准备：Mock规范化、API文档 | ⏳ 待实施 |

---

## 🎯 项目简介

智析销售AI是一个基于人工智能的销售对话分析平台，帮助销售团队：
- 📞 分析销售通话，提取关键信息
- 🎯 评估客户购买意向
- 📊 生成可视化分析报告
- 👥 团队协作共享洞察
- 📄 导出PDF报告

---

## 🛠️ 技术栈

**前端：**
- HTML5 + CSS3 + JavaScript (ES6+)
- 响应式设计
- CSS变量主题系统

**后端：**
- Python FastAPI
- SQLite数据库
- JWT认证

---

## 📁 项目结构

```
Smart Analysis/
├── index.html              # 首页（产品介绍）✓
├── login.html              # 登录页 ✓
├── register.html           # 注册页 ✓
├── dashboard.html          # 工作台 ✓
├── history.html            # 分析列表（搜索+分页）✓
├── analysis.html           # 分析详情 ✓
├── team.html               # 团队协作 ✓
├── profile.html            # 个人中心 ✓
│
├── static/
│   ├── css/
│   │   └── style.css       # 全局样式
│   ├── js/
│   │   ├── auth.js         # 认证工具
│   │   ├── api.js          # API封装
│   │   ├── utils.js        # 工具函数
│   │   └── pagination.js   # 分页组件
│   └── images/
│       └── logo.svg        # Logo
│
├── backend/                # 后端服务（FastAPI）
│
├── .gitignore              # Git忽略规则
├── init-git.bat            # Git初始化脚本
├── ISSUES.md               # 跳过功能记录
└── README.md               # 本文件
```

---

## 🚀 快速开始

### 启动后端

```bash
cd backend
pip install -r requirements.txt
python main.py
```

后端服务：http://localhost:8080

### 访问前端

直接在浏览器打开 HTML 文件，或使用 Live Server：

```bash
# 使用 Python
cd D:\vs_code\Smart Analysis
python -m http.server 5500

# 访问 http://localhost:5500
```

---

## 📝 开发路线图

### v1.0 - 基础框架 ✅
- [x] 全局CSS样式系统
- [x] 认证状态管理
- [x] API调用封装
- [x] 工具函数库
- [x] 7个页面完整实现
- [x] 登录/注册流程
- [x] Mock数据展示

### v1.1 - 交互优化 ✅
- [x] Toast提示优化（堆叠、动画、点击关闭）
- [x] 页面过渡动画（fadeIn、fadeInUp）
- [x] 按钮Loading状态
- [x] 空状态引导
- [x] 骨架屏加载
- [x] 表单验证优化（实时验证、颜色提示）

### v1.2 - 功能补全 ✅
- [x] 搜索筛选组件（防抖300ms + 回车搜索）
- [x] 分页组件（每页20条）
- [x] 分析列表页（history.html）
- [x] 删除确认弹窗
- [x] 数据刷新功能

### v1.3 - 数据可视化 ✅
- [x] Chart.js集成（CDN）
- [x] 工作台趋势折线图
- [x] 统计数字滚动动画
- [x] 分析详情评分环形图
- [x] 关键词柱状图

### v1.4 - PDF导出 ⏳
- [ ] html2pdf.js集成
- [ ] 导出范围选择
- [ ] PDF模板设计

### v1.5 - 响应式完善 ⏳
- [ ] 移动端底部导航
- [ ] 响应式断点
- [ ] 各页面移动端适配

### v1.6 - 后端对接准备 ⏳
- [ ] Mock数据规范化
- [ ] API接口文档
- [ ] Token刷新机制
- [ ] 错误处理统一

### v0.6 - 历史记录
- [ ] 分析列表
---

## 🎨 设计规范

### 色彩系统
- 主色：`#3B82F6` (科技蓝)
- 成功：`#10B981` (绿色)
- 警告：`#F59E0B` (橙色)
- 错误：`#EF4444` (红色)

### 技术选型
- 图表库：Chart.js v4.x
- PDF库：html2pdf.js v0.10.1
- 动画风格：简洁淡入

---

## 🔗 相关链接

- **GitHub仓库**：https://github.com/hongls68/zhixi-sales-ai
- **后端API文档**：http://localhost:8080/docs（启动后端后访问）

---

## 📄 许可证

Copyright © 2026 智析销售AI. All rights reserved.
