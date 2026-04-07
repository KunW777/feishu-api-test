"""
用户接口测试用例
"""

import pytest
from api.user import UserAPI


class TestUserAPI:
    """用户 API 测试类"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.user_api = UserAPI()

    def test_update_user_id(self):
        """测试更新用户 ID"""
        result = self.user_api.update_user_id(
            user_id="test_user_id_123456789",
            new_user_id="new_test_user_id"
        )
        # 验证 API 能连通
        assert "code" in result
