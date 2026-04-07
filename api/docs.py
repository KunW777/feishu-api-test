"""
文档相关 API
"""

from api.base import BaseAPI


class DocsAPI(BaseAPI):
    """文档 API 封装"""

    def create_doc(self, title: str, folder_token: str = None) -> dict:
        """
        创建文档

        :param title: 文档标题
        :param folder_token: 文件夹 token（可选）
        :return: API 响应
        """
        endpoint = "/docx/v1/documents"
        data = {"title": title}
        if folder_token:
            data["folder_token"] = folder_token
        return self.post(endpoint, data=data)

    def get_doc_info(self, document_id: str) -> dict:
        """
        获取文档基本信息

        :param document_id: 文档 ID
        :return: API 响应
        """
        endpoint = f"/docx/v1/documents/{document_id}"
        return self.get(endpoint)
