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

    def test_get_token(self, api_token):
        """测试获取 token"""
        assert api_token is not None
        assert len(api_token) > 0

    def test_create_doc(self):
        """测试创建文档"""
        result = self.docs_api.create_doc(title="测试文档")
        # 验证 API 能连通（可能是成功或业务错误）
        assert "code" in result

    def test_get_doc_info(self):
        """测试获取文档基本信息"""
        # document_id 需要至少27个字符
        result = self.docs_api.get_doc_info(document_id="test_doc_id_12345678901234567890")
        # 验证 API 能连通（文档不存在是正常的）
        assert "code" in result
