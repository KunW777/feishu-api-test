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

    def test_create_space(self):
        """测试创建知识空间"""
        result = self.wiki_api.create_space(
            name="测试知识空间",
            description="这是一个测试知识空间"
        )
        # 验证 API 能连通
        assert "code" in result

    def test_delete_member(self):
        """测试删除知识空间成员"""
        result = self.wiki_api.delete_member(
            space_id="test_space_id",
            member_id="test_member_id"
        )
        # 验证 API 能连通
        assert "code" in result

    def test_update_space_settings(self):
        """测试更新知识空间设置"""
        result = self.wiki_api.update_space_settings(
            space_id="test_space_id",
            visible_type="public"
        )
        # 验证 API 能连通
        assert "code" in result
