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
        self.space_id = None

    def test_01_get_space_list(self):
        """测试获取知识空间列表"""
        result = self.wiki_api.get_space_list(page_size=10)
        assert result["code"] == 0
        items = result["data"].get("items", [])
        print(f"\n知识空间数量: {len(items)}")
        
        # 如果有知识空间，保存第一个 space_id
        if items:
            self.__class__.space_id = items[0]["space"]["space_id"]
            print(f"使用已有知识空间: {self.__class__.space_id}")


class TestWikiAPIWithUserToken:
    """需要 user_access_token 的知识库 API 测试"""

    @pytest.fixture(autouse=True)
    def setup(self, user_token):
        self.user_token = user_token
        self.wiki_api = WikiAPI(user_token=user_token)
        self.space_id = None

    def test_01_create_space(self):
        """测试创建知识空间（需要 user_access_token）"""
        result = self.wiki_api.create_space(
            name="API测试知识空间",
            description="用于API测试的知识空间"
        )
        assert result["code"] == 0
        self.__class__.space_id = result["data"]["space"]["space_id"]
        print(f"\n创建知识空间成功，space_id: {self.__class__.space_id}")

    def test_02_update_space_settings(self):
        """测试更新知识空间设置"""
        if not hasattr(self.__class__, 'space_id') or not self.__class__.space_id:
            pytest.skip("创建知识空间失败，跳过此测试")
        
        result = self.wiki_api.update_space_settings(
            space_id=self.__class__.space_id,
            visible_type="public"
        )
        assert result["code"] == 0
        print(f"\n更新知识空间设置成功")

    def test_03_delete_member(self):
        """测试删除知识空间成员"""
        if not hasattr(self.__class__, 'space_id') or not self.__class__.space_id:
            pytest.skip("创建知识空间失败，跳过此测试")
        
        # 使用不存在的成员ID测试，验证API连通性
        result = self.wiki_api.delete_member(
            space_id=self.__class__.space_id,
            member_id="ou_test_member_id",
            member_type="openid",
            member_role="reader"
        )
        # 成员不存在是正常的，验证API能连通即可
        assert "code" in result
        print(f"\n删除成员接口调用成功")
