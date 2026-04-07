"""
文档接口测试用例
"""

import pytest
from api.docs import DocsAPI


class TestDocsAPI:
    """文档 API 测试类"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.docs_api = DocsAPI()
        self.document_id = None

    def test_get_token(self, api_token):
        """测试获取 token"""
        assert api_token is not None
        assert len(api_token) > 0

    def test_01_create_doc(self):
        """测试创建文档"""
        result = self.docs_api.create_doc(title="API测试文档")
        assert result["code"] == 0
        # 保存 document_id 供后续测试使用
        self.__class__.document_id = result["data"]["document"]["document_id"]
        print(f"\n创建文档成功，document_id: {self.__class__.document_id}")

    def test_02_get_doc_info(self):
        """测试获取文档基本信息"""
        # 如果创建失败，跳过此测试
        if not hasattr(self.__class__, 'document_id') or not self.__class__.document_id:
            pytest.skip("没有有效的 document_id")
        
        result = self.docs_api.get_doc_info(document_id=self.__class__.document_id)
        assert result["code"] == 0
        print(f"\n获取文档信息成功: {result['data']['document']['title']}")
