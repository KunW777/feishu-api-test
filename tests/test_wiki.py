"""
知识库接口测试用例
"""

import pytest
from api.wiki import WikiAPI


class TestWikiAPI:
    """知识库 API 测试类"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.wiki_api = WikiAPI()

    def test_get_space_list(self):
        """测试获取知识空间列表"""
        result = self.wiki_api.get_space_list(page_size=10)
        assert result["code"] == 0
        assert "items" in result["data"]

    @pytest.mark.skip(reason="需要根据实际情况修改后运行")
    def test_create_space(self):
        """测试创建知识空间"""
        result = self.wiki_api.create_space(
            name="测试知识空间",
            description="这是一个测试知识空间"
        )
        assert result["code"] == 0

    @pytest.mark.skip(reason="需要有效的 space_id 和 member_id，请根据实际情况修改后运行")
    def test_delete_member(self):
        """测试删除知识空间成员"""
        result = self.wiki_api.delete_member(
            space_id="your_space_id",
            member_id="your_member_id"
        )
        assert result["code"] == 0

    @pytest.mark.skip(reason="需要有效的 space_id，请根据实际情况修改后运行")
    def test_update_space_settings(self):
        """测试更新知识空间设置"""
        result = self.wiki_api.update_space_settings(
            space_id="your_space_id",
            visible_type="public"
        )
        assert result["code"] == 0
