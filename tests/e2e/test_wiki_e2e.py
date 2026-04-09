"""
飞书知识库 wiki E2E 测试

镜像 test_docs_e2e.py 的两个场景结构，验证 wiki 模块的浏览器端行为：
1. TestWikiHomeLoads        — 登录态在 wiki 页面有效 + wiki 相关 API 全部健康
2. TestWikiNetworkMonitoring — 捕获 wiki 首页加载时命中的专属 API 端点

已知 wiki 内部端点样本（由 test_docs_e2e.py::TestNetworkMonitoring 首次产出）：
- GET /space/api/wiki/v2/space/star/get/?size=200  # 知识空间收藏列表

前置条件同 docs：
- tests/e2e/auth_state.json 必须存在（由 save_auth.py 生成）
- conftest.py 里 browser_context_args 会自动注入 storageState
"""

WIKI_HOME_PATH = "/wiki/"


class TestWikiHomeLoads:
    """打开 wiki 首页，验证登录态有效、wiki 相关后端 API 健康。"""

    def test_wiki_home_loads_without_login_redirect(self, page, feishu_base_url):
        """
        核心 E2E 断言：用户访问 wiki 首页能正常看到自己的知识空间列表。

        三层断言：
        - URL 层：没被重定向到登录/SSO 页面
        - URL 层：最终停留在 /wiki 路径下（防止被静默跳走）
        - 网络层：feishu.cn 域下所有 /api/ 调用 HTTP status < 400
        """
        responses: list[dict] = []

        page.on(
            "response",
            lambda r: responses.append({"url": r.url, "status": r.status}),
        )

        page.goto(f"{feishu_base_url}{WIKI_HOME_PATH}")
        page.wait_for_load_state("networkidle")

        # 断言 1：没被重定向到登录/SSO 页面
        current_url = page.url.lower()
        assert "login" not in current_url and "passport" not in current_url, (
            f"被重定向到登录页：{page.url}"
            "——登录态可能已失效，请重新运行 `python tests/e2e/save_auth.py`"
        )

        # 断言 2：最终 URL 确实停留在 wiki 路径下
        assert "/wiki" in current_url, (
            f"打开 wiki 首页后 URL 不在 wiki 路径下：{page.url}"
            "——可能飞书前端路由变化，需要确认正确的 wiki 首页路径"
        )

        # 断言 3：feishu.cn 域下的 API 调用没有 4xx/5xx
        api_failures = [
            r
            for r in responses
            if "feishu.cn" in r["url"]
            and "/api/" in r["url"]
            and r["status"] >= 400
        ]
        assert not api_failures, (
            f"wiki home 加载中有 {len(api_failures)} 个 API 请求失败："
            f"{api_failures[:3]}"
        )

        print(
            f"\n[OK] wiki home 加载正常："
            f"共捕获 {len(responses)} 个响应，无失败 API"
        )


class TestWikiNetworkMonitoring:
    """观察型测试：捕获 wiki 首页加载时的请求，筛出 wiki 专属 API。"""

    def test_capture_wiki_specific_endpoints(self, page, feishu_base_url):
        """
        在 docs 版 TestNetworkMonitoring 的基础上增加 wiki 维度的过滤。

        产出两份数据：
        1. 全量请求按 resource_type 分类（对齐 docs 版，用于横向对比）
        2. wiki 专属 API 清单（URL 含 /wiki/ 且类型为 fetch/xhr）——
           后续写 wiki mock 测试时从这里挑具体 URL 模式。
        """
        captured: list[dict] = []

        page.on(
            "request",
            lambda req: captured.append(
                {
                    "method": req.method,
                    "url": req.url,
                    "resource_type": req.resource_type,
                }
            ),
        )

        page.goto(f"{feishu_base_url}{WIKI_HOME_PATH}")
        page.wait_for_load_state("networkidle")

        # 按 resource_type 分类统计
        by_type: dict[str, int] = {}
        for req in captured:
            by_type[req["resource_type"]] = by_type.get(req["resource_type"], 0) + 1

        # 筛 wiki 专属 API：URL 包含 /wiki/ 且是 fetch/xhr 类型
        wiki_api_calls = [
            r
            for r in captured
            if "/wiki/" in r["url"]
            and r["resource_type"] in ("fetch", "xhr")
        ]

        print(f"\n共捕获 {len(captured)} 个请求")
        print(f"按资源类型分布: {by_type}")
        print(f"wiki 专属 API 调用: {len(wiki_api_calls)} 个")
        if wiki_api_calls:
            print("前 5 个 wiki 端点（截断到 120 字符）：")
            for call in wiki_api_calls[:5]:
                print(f"  {call['method']} {call['url'][:120]}")

        # 宽松断言：wiki 首页至少应该产生一些请求
        assert len(captured) > 0, "加载 wiki home 应该至少产生一些请求"
