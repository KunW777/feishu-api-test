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

    @pytest.mark.skip(reason="需要有效的 folder_token，请根据实际情况修改后运行")
    def test_create_doc(self):
        """测试创建文档"""
        result = self.docs_api.create_doc(
            title="测试文档",
            folder_token="your_folder_token"  # 替换为实际的 folder_token
        )
        assert result["code"] == 0
        assert "document_id" in result["data"]

    @pytest.mark.skip(reason="需要有效的 document_id，请根据实际情况修改后运行")
    def test_get_doc_info(self):
        """测试获取文档基本信息"""
        result = self.docs_api.get_doc_info(
            document_id="your_document_id"  # 替换为实际的 document_id
        )
        assert result["code"] == 0
