"""
E2E 测试公共 fixture

本模块做两件事：
1. 覆盖 pytest-playwright 的 browser_context_args fixture，自动加载
   auth_state.json 注入 storageState，让所有 E2E 测试复用手动登录的状态。
2. 提供 feishu_base_url fixture，供测试用例拼 URL。

前置条件：
- 先跑过 `python tests/e2e/save_auth.py` 生成 auth_state.json
- 如果 auth_state.json 不存在，所有 E2E 测试会被 skip 并提示怎么生成
"""
from pathlib import Path

import pytest

AUTH_FILE = Path(__file__).parent / "auth_state.json"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    覆盖 pytest-playwright 默认的 browser context 参数，注入 storageState。

    pytest-playwright 的 page/context fixture 会调用本 fixture 的返回值来
    创建 BrowserContext。通过在返回值里加 storage_state，所有由 page fixture
    创建的浏览器实例都会自动带上登录态 cookies。
    """
    if not AUTH_FILE.exists():
        pytest.skip(
            f"未找到 {AUTH_FILE}。请先运行 "
            "`python tests/e2e/save_auth.py` 完成一次性登录。"
        )
    return {**browser_context_args, "storage_state": str(AUTH_FILE)}


@pytest.fixture(scope="session")
def feishu_base_url() -> str:
    """飞书实例的根 URL，供测试拼具体路径（如 /drive/home/）。"""
    return "https://ucnzz0zt5wpo.feishu.cn"
