# 飞书开放平台 API 测试项目

本项目用于实操飞书开放平台服务端 API 测试，涵盖以下测试方式：

- **HTTPS 各种方法请求**
- **Playwright 端到端 (E2E) 测试**
- **Python requests 库 + pytest 实现多参数自动化接口/集成测试**
- **生成 HTML 测试报告**

> 📖 开放平台 API 文档首页：https://open.feishu.cn/document/home/index

---

## 项目结构

```
feishu-api-test/
├── config/                 # 配置文件
│   └── settings.py         # 全局配置（app_id、app_secret 等）
├── api/                    # API 封装层
│   ├── base.py             # 基础请求封装
│   ├── docs.py             # 文档 API
│   ├── wiki.py             # 知识库 API
│   └── department.py       # 部门 API
├── utils/                  # 工具模块
│   └── token_manager.py    # Token 管理（获取、缓存、刷新）
├── tests/                  # 测试用例
│   ├── conftest.py         # Pytest 配置和 fixtures
│   ├── test_docs.py        # 文档接口测试
│   ├── test_wiki.py        # 知识库接口测试
│   └── test_department.py  # 部门接口测试
├── e2e/                    # Playwright E2E 测试（预留）
├── reports/                # 测试报告输出目录
├── requirements.txt        # 项目依赖
└── README.md
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置应用凭证

修改 `config/settings.py`，填入你的 `app_id` 和 `app_secret`：

```python
APP_ID = "your_app_id"
APP_SECRET = "your_app_secret"
```

### 3. 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行指定测试文件
pytest tests/test_docs.py

# 生成 HTML 测试报告
pytest tests/ --html=reports/report.html --self-contained-html
```

---

## 涉及模块

### 一、云文档

#### 1. 文档

| 接口 | 方法 |
|------|------|
| 创建文档 | POST |
| 获取文档基本信息 | GET |

#### 2. 知识库

##### 知识空间

| 接口 | 方法 |
|------|------|
| 获取知识空间列表 | GET |
| 创建知识空间 | POST |

##### 空间成员

| 接口 | 方法 |
|------|------|
| 删除知识空间成员 | DELETE |

##### 空间设置

| 接口 | 方法 |
|------|------|
| 更新知识空间设置 | PUT |

#### 3. 部门

| 接口 | 方法 |
|------|------|
| 更新用户 ID | PATCH |

---

## 权限说明

飞书开放平台涉及两种主要权限模式：

| 模式 | Token 类型 | 使用场景 | 获取方式 |
|------|------------|----------|----------|
| 服务端 API | `tenant_access_token` | 服务端 API 调试 | Python 代码调用 API，或终端命令行工具（curl、HTTPie） |
| E2E 测试 | `user_access_token` | 端到端用户模拟测试 | 飞书开放平台 API 调试台获取 |

> ⚠️ `user_access_token` 需要用户授权（OAuth 流程），流程繁琐。为简化测试，直接在飞书开放平台 **API 调试台** 中获取。
>
> 📖 API 调试台位置：飞书开放平台 → 应用详情 → API 调试台 → 选择「user_access_token」模式
