# Ezpz website review

独立项目，2026-11-13 开始重建，2026-11-17 完成交付校验。完整复用已确认 Ola 第 19 版的页面、断点、控件和交互结构。母版提交 `f8026d91802eb907a54d9f84c349aa306ef098cd`，指纹见 `alignment-reference.json`。

2026-11-17 用户最新确认：所有展示文案、标题完整复用 Ola，只替换产品名及核验后的主体信息；品牌图标、Logo、配色和装饰换为 Ezpz。正式协议保留 Ezpz 官方正文。

## 修改和构建

- 文案：`product-copy.json`，语言 en / zh / hi / id。
- `sync-template-copy.py` 可重新从固定母版同步全部展示文案，只替换产品名和联系方式。构建前不会自动覆盖用户后续修改。
- 主体、邮箱、真实目的地址、品牌基础色：`product-config.json`。
- 色彩与背景装饰：`brand-paint.py`。配置中 colors 为基础色清单，完整同色阶转换在此文件实现。
- 占位图集中由 `build-aligned.py` 生成；首屏 1600×900 / 900×1600，五个场景均为 720×1280。替换同名资源即可，不改 DOM 槽位。
- 母版源码与通用字体、下载徽章已复制在 `template/`。保留母版作为版本证据，产品运行文件不加载该目录。

```powershell
python -m pip install pillow
python build-aligned.py
python -m http.server 8766 --bind 127.0.0.1 --directory dist
```

构建仅依赖本项目文件，不再读取其他产品目录或共享盘。`research*.py` 为官方来源采集记录，正常构建无需重新访问网络。

## 评审与离线

双击 `dist/index.html` 即可离线打开，全部字体和图片均为本地资源。通过链接访问时，使用 `?lang=zh#/home`，其余页面采用母版 hash 路由。

GitHub Pages 自动发布已构建的 `dist/`。修改配置后先运行 Python 构建再提交。部署信息、当前提交与验证结果见 `DEPLOYMENT.md` 和 `tests/report.json`。

`npm ci` 安装浏览器验证依赖，默认使用本机 Chrome；可设置 `QA_CHANNEL=msedge` 使用 Edge。运行 `npm test` 自动启动测试服务器，覆盖 1440×900 / 390×844、四语言、页面路由和交互。母版默认从指定原始目录只读加载，可用 `BASELINE_DIRECTORY` 指定其副本；只有对照测试需要该外部参考，正常构建和部署均独立。浏览器测试不依赖生产统计或支付。

## 内容边界

下载仅 App Store、Google Play 已核实并启用；其余下载渠道与网页充值保留同位入口并显示待确认反馈。联系表单只做前端校验，不发送消息。Cookie 设置保存在本浏览器，无统计与广告服务。三份正式协议来自 Ezpz 官方正文，其他政策保留母版待确认页面。

来源与事实差异见 `SOURCES.md`，生产接入清单见 `HANDOFF.md`。首页展示素材均为占位，Logo 使用原官网真实横版文件，无新绘制标识。
