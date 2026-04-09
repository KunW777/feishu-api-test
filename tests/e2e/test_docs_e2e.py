"""
飞书云文档 E2E 测试

两个场景：
1. TestDriveHomeLoads    — 登录态有效性 + 后端 API 健康检查
2. TestNetworkMonitoring — 网络请求监听与分类统计

所有测试依赖 tests/e2e/auth_state.json（由 save_auth.py 生成），
conftest.py 会自动把登录态注入到 page fixture 创建的浏览器 context 里。
"""


class TestDriveHomeLoads:
    """打开 drive home，验证登录态有效、后端 API 全部响应正常。"""

    def test_drive_home_loads_without_login_redirect(self, page, feishu_base_url):
        """
        核心 E2E 断言：用户访问云文档首页能正常看到自己的内容。

        包含两层断言：
        - URL 层：没有被重定向到登录/SSO 页面
        - 网络层：feishu.cn 域名下的所有 /api/ 调用 HTTP status < 400
        """
        responses: list[dict] = []

        # 注册响应监听器，捕获所有响应的 url 和 status
        page.on(
            "response",
            lambda r: responses.append({"url": r.url, "status": r.status}),
        )

        page.goto(f"{feishu_base_url}/drive/home/")
        page.wait_for_load_state("networkidle")

        # 断言 1：没被重定向到登录/SSO 页面
        current_url = page.url.lower()
        assert "login" not in current_url and "passport" not in current_url, (
            f"被重定向到登录页：{page.url}"
            "——登录态可能已失效，请重新运行 `python tests/e2e/save_auth.py`"
        )

        # 断言 2：feishu.cn 域名下的 API 调用没有失败
        api_failures = [
            r
            for r in responses
            if "feishu.cn" in r["url"]
            and "/api/" in r["url"]
            and r["status"] >= 400
        ]
        assert not api_failures, (
            f"drive home 加载中有 {len(api_failures)} 个 API 请求失败："
            f"{api_failures[:3]}"
        )

        print(
            f"\n[OK] drive home 加载正常："
            f"共捕获 {len(responses)} 个响应，无失败 API"
        )


class TestNetworkMonitoring:
    """观察型测试：打开页面时捕获所有请求并按资源类型分类统计。"""

    def test_capture_and_classify_requests(self, page, feishu_base_url):
        """
        监听浏览器发出的所有请求，做分类统计并打印。

        不做严格业务断言——本测试的价值是产出"飞书 drive home 加载时
        实际调了哪些端点"的分析报告，后续写 mock 测试时可以从这里挑
        具体 URL 模式。
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

        page.goto(f"{feishu_base_url}/drive/home/")
        page.wait_for_load_state("networkidle")

        # 按 resource_type 分类（document/script/image/xhr/fetch 等）
        by_type: dict[str, int] = {}
        for req in captured:
            by_type[req["resource_type"]] = by_type.get(req["resource_type"], 0) + 1

        # 粗略筛出疑似 API 调用
        api_calls = [
            r for r in captured if "/api/" in r["url"] or "/suite/" in r["url"]
        ]

        print(f"\n共捕获 {len(captured)} 个请求")
        print(f"按资源类型分布: {by_type}")
        print(f"疑似 API 调用: {len(api_calls)} 个")
        if api_calls:
            print("前 5 个 API 端点（截断到 100 字符）：")
            for call in api_calls[:5]:
                print(f"  {call['method']} {call['url'][:100]}")

        # 宽松断言：加载 drive home 至少应该产生 HTML + 若干静态资源
        assert len(captured) > 0, "加载 drive home 应该至少产生一些请求"
