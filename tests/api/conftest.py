"""
API 测试层的 pytest 配置

只放 API 测试专用的 fixture：tenant_access_token 获取、api_token / user_token。
--user-token 命令行参数已上移到项目根 conftest.py（pytest_addoption 必须
在 pytest 解析命令行前被加载，放在子目录 conftest 里会导致 argparse 识别不了）。
"""

import pytest
from utils.token_manager import token_manager


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
