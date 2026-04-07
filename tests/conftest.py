"""
Pytest 配置文件
定义全局 fixtures 和钩子
"""

import pytest
from utils.token_manager import token_manager


@pytest.fixture(scope="session", autouse=True)
def setup_token():
    """测试会话开始前获取 token"""
    token_manager.clear_cache()
    token = token_manager.get_token()
    print(f"\n获取 token 成功: {token[:20]}...")


@pytest.fixture(scope="session")
def api_token():
    """返回 token 供测试使用"""
    return token_manager.get_token()
