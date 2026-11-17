# Ezpz 部署记录

- 独立 GitHub 仓库：https://github.com/meiliyitian2020-cyber/ezpz-website-preview
- 分支：`main`
- 托管：GitHub Pages，公开访问，无 ChatGPT 登录依赖。
- 在线评审：https://meiliyitian2020-cyber.github.io/ezpz-website-preview/?lang=zh
- 当前状态：已部署，并以无 Cookie、无登录的全新浏览器上下文验证 HTTP 200。
- 实际部署源码提交：`34395ab7825b688dfc41596a495047ca8821ca06`。
- 部署流水线：https://github.com/meiliyitian2020-cyber/ezpz-website-preview/actions/runs/44047175611 ，结果 success。
- 线上 `index.html` 与本地 `dist/index.html` 逐字节一致，SHA-256：`ea39a5b717fce2e46d8d62882ed51f57f5d1c41a9dea4e7da5ca3e7de49a30e8`。
- 本地目录：`G:\26.11.13-ezpz\ezpz-website-preview\`
- 母版：Ola v19，提交 `f8026d91802eb907a54d9f84c349aa306ef098cd`。
- 最新内容口径：2026-11-17 用户确认所有展示文案和标题复用 Ola，仅改产品身份和品牌视觉。
- 本地验证：96 组矩形比对（2 种尺寸 × 4 语言 × 12 路由），布局偏移 0、文本溢出 0、脚本错误 0；下载、弹层、语言、FAQ、表单和 Cookie 交互均通过。见 `tests/report.json` 和 `tests/audit.json`。
- 匿名与离线验证：1440×900、390×844 均通过；离线模式外部网络请求 0，无控制台错误。见 `tests/access.json`。
- 桌面截图：`tests/screenshots/anonymous-online-1440-zh.png`；手机截图：`tests/screenshots/anonymous-online-390-zh.png`。
- 离线包：`Ezpz-offline-review.zip`，解压后双击根目录 `index.html`。

未知 APK、其他商店和充值地址保留同位入口与待确认反馈。联系表单为前端校验预览。未接生产支付、后台或统计。

后续仅更新文档和测试证据的提交不会重复发布页面；工作流只在 `dist/` 或发布配置改变时触发。完整源码的最新提交可用 `git rev-parse HEAD` 查看，页面部署对应上面记录的源码提交。
