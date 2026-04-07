"""
部门接口测试用例
"""

import pytest
from api.department import DepartmentAPI


class TestDepartmentAPI:
    """部门 API 测试类"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.department_api = DepartmentAPI()

    @pytest.mark.skip(reason="需要有效的 user_id，请根据实际情况修改后运行")
    def test_update_user_id(self):
        """测试更新用户 ID"""
        result = self.department_api.update_user_id(
            user_id="old_user_id",
            new_user_id="new_user_id"
        )
        assert result["code"] == 0
