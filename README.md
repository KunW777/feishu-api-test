# 飞书开放平台 API 测试项目

本项目用于实操飞书开放平台服务端 API 测试，涵盖以下测试方式：

- **HTTPS 各种方法请求**
- **Playwright 端到端 (E2E) 测试**（预留）
- **Python requests 库 + pytest 实现多参数自动化接口/集成测试**
- **生成 HTML 测试报告**

> 📖 开放平台 API 文档首页：https://open.feishu.cn/document/home/index

---

## 项目结构

```
feishu-api-test/
├── .gitignore               # Git 忽略规则
├── LICENSE                  # 开源协议
├── README.md
├── requirements.txt         # 项目依赖
│
├── config/                  # 配置文件
│   ├── settings.py          # 全局配置（app_id、app_secret）❌ 不上传
│   └── settings.py.template # 配置模板
│
├── api/                     # API 封装层
│   ├── base.py              # 基础请求封装
│   ├── docs.py              # 文档 API
│   └── wiki.py              # 知识库 API
│
├── utils/                   # 工具模块
│   └── token_manager.py     # Token 管理（获取、缓存、刷新）
│
├── tests/                   # API 测试用例
│   ├── conftest.py          # Pytest 配置和 fixtures
│   ├── test_docs.py         # 文档接口测试
│   └── test_wiki.py         # 知识库接口测试
│
├── e2e/                     # Playwright E2E 测试（预留）
│
└── reports/                 # 测试报告输出目录 ❌ 不上传
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt

# 安装 Playwright 浏览器（E2E 测试需要）
playwright install
```

### 2. 配置应用凭证

复制配置模板并填入你的 `app_id` 和 `app_secret`：

```bash
cp config/settings.py.template config/settings.py
```

修改 `config/settings.py`：

```python
APP_ID = "your_app_id"
APP_SECRET = "your_app_secret"
```

### 3. 运行测试

```bash
# 运行基础测试（使用 tenant_access_token）
pytest --html=reports/report.html --self-contained-html

# 运行完整测试（需要 user_access_token）
pytest --user-token=你的user_access_token --html=reports/report.html --self-contained-html
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

---

## 测试结果

### 基础测试（tenant_access_token）

| 模块 | 接口 | 状态 |
|------|------|------|
| 文档 | 创建文档 | ✅ 通过 |
| 文档 | 获取文档基本信息 | ✅ 通过 |
| 知识库 | 获取知识空间列表 | ✅ 通过 |

### 完整测试（需要 --user-token）

| 模块 | 接口 | 状态 |
|------|------|------|
| 知识库 | 创建知识空间 | ✅ 通过 |
| 知识库 | 更新知识空间设置 | ✅ 通过 |
| 知识库 | 删除知识空间成员 | ✅ 通过 |

---

## Token 说明

| 接口 | Token 类型 |
|------|------------|
| 创建文档 | `tenant_access_token` |
| 获取文档信息 | `tenant_access_token` |
| 获取知识空间列表 | `tenant_access_token` |
| **创建知识空间** | `user_access_token` ⚠️ |
| 更新知识空间设置 | `tenant_access_token` |
| 删除知识空间成员 | `tenant_access_token` |

### 获取 user_access_token

1. 打开飞书开放平台 → 应用详情 → API 调试台
2. 选择「user_access_token」模式
3. 复制 token 用于测试

```bash
pytest --user-token=复制的token
```

---

## 权限说明

| 模式 | Token 类型 | 使用场景 | 获取方式 |
|------|------------|----------|----------|
| 服务端 API | `tenant_access_token` | 服务端 API 调试 | Python 代码 / curl / HTTPie |
| 用户权限 API | `user_access_token` | 需要用户权限的接口 | 飞书开放平台 API 调试台 |
