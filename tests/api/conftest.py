"""
Pytest 配置文件
定义全局 fixtures 和钩子
"""

import pytest
from utils.token_manager import token_manager


def pytest_addoption(parser):
    """添加命令行参数"""
    parser.addoption(
        "--user-token",
        action="store",
        default=None,
        help="user_access_token，用于需要用户权限的接口测试"
    )


@pytest.fixture(scope="session", autouse=True)
def setup_token():
    """测试会话开始前获取 tenant_access_token"""
    token_manager.clear_cache()
    token = token_manager.get_token()
    print(f"\n获取 tenant_access_token 成功: {token[:20]}...")


@pytest.fixture(scope="session")
def api_token():
    """返回 tenant_access_token 供测试使用"""
    return token_manager.get_token()


@pytest.fixture(scope="session")
def user_token(request):
    """返回 user_access_token，未提供则跳过相关测试"""
    token = request.config.getoption("--user-token")
    if not token:
        pytest.skip("需要 user_access_token，请使用 --user-token 参数运行")
    return token
