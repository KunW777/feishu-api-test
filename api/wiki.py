"""
知识库相关 API
"""

from api.base import BaseAPI


class WikiAPI(BaseAPI):
    """知识库 API 封装"""

    # ========== 知识空间 ==========

    def get_space_list(self, page_size: int = 20, page_token: str = None) -> dict:
        """
        获取知识空间列表

        :param page_size: 分页大小
        :param page_token: 分页标记
        :return: API 响应
        """
        endpoint = "/wiki/v2/spaces"
        params = {"page_size": page_size}
        if page_token:
            params["page_token"] = page_token
        return self.get(endpoint, params=params)

    def create_space(self, name: str, description: str = None) -> dict:
        """
        创建知识空间

        :param name: 空间名称
        :param description: 空间描述（可选）
        :return: API 响应
        """
        endpoint = "/wiki/v2/spaces"
        data = {"name": name}
        if description:
            data["description"] = description
        return self.post(endpoint, data=data)

    # ========== 空间成员 ==========

    def delete_member(self, space_id: str, member_id: str, member_type: str = "userid") -> dict:
        """
        删除知识空间成员

        :param space_id: 知识空间 ID
        :param member_id: 成员 ID
        :param member_type: 成员类型（userid/openid/unionid）
        :return: API 响应
        """
        endpoint = f"/wiki/v2/spaces/{space_id}/members/{member_id}"
        params = {"member_type": member_type}
        return self.delete(endpoint, params=params)

    # ========== 空间设置 ==========

    def update_space_settings(self, space_id: str, visible_type: str = None) -> dict:
        """
        更新知识空间设置

        :param space_id: 知识空间 ID
        :param visible_type: 可见性类型
        :return: API 响应
        """
        endpoint = f"/wiki/v2/spaces/{space_id}/settings"
        data = {}
        if visible_type:
            data["visible_type"] = visible_type
        return self.put(endpoint, data=data)
