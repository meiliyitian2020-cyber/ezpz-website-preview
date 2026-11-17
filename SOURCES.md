# 内容与品牌来源

首次采集 2026-11-13，交付验证 2026-11-17。原始文件、接口响应和抓取记录在 `sources/`。网页正文由官方脚本或官方协议接口读取，未用其他产品协议改名。

| 内容 | 官方来源 | 采用结果 |
| --- | --- | --- |
| 当前官网身份 | https://ezpzapp.net/ | HTTP 200，无跳转至其他产品；标题 ezpz，官网口号 Ez to make friends |
| 横版标识 | 官网脚本引用 https://static.ezpzapp.net/a/ezpz-site-pc/assets/logo-DQER-zi7.png | 使用原始完整横版标识，等比置于母版图标画布；无绘制字标 |
| Google Play | https://play.google.com/store/apps/details?id=com.party.ezpz | Ezpz - easy chat easy game，展示开发者 igo team，法律主体 HAGO SINGAPORE PTE. LTD.；包名 com.party.ezpz |
| App Store | https://apps.apple.com/bh/app/ezpz-dera/id1625619255 | 官网原链接 /dera-3d-avatar-meet-chat/ 自动跳转至 /ezpz-dera/；当前名 Ezpz (Dera)，bundleId com.joyy.dera，seller HAGO Singapore PTE. LTD |
| 客服与地址 | 官网 bundle、Google Play、隐私政策 | contactezpzapp@gmail.com；HAGO SINGAPORE PTE. LTD.；30 Pasir Panjang Road #15-31A Mapletree Business City Singapore 117440 |
| About Us 与全部展示文案、标题 | 用户 2026-11-17 最新确认的 Ola 第 19 版 | 逐字复用母版的四语言展示内容，仅将产品名替换为 Ezpz；不再采用此前提炼的产品专属展示文案 |
| 五个功能场景 | 同上 | 数量、标题、描述和顺序完全复用 Ola；本次按用户确认的统一文案口径交付 |
| 服务协议 | https://www.ezpzapp.net/a/license/ezpz-user.html?lang=en | 原站脚本 appName=ezpz，postType=user，os=android；官方正文 latest updated 02 February 2026 |
| 隐私政策 | https://www.ezpzapp.net/a/license/ezpz-privacy.html?lang=en | appName=ezpz，postType=privacy，os=android；Last Updated 02/02/2026 |
| 儿童安全政策 | https://www.ezpzapp.net/a/license/ezpz-children-policy.html?lang=en | 官方正文 Latest Updated 28 October 2025 |

协议接口：`https://feapi.ezpzapp.net/post-platform/getPostDetail?lang=en`。请求头 `x-app-name: ezpz`，`x-app-post-type: user/privacy/children-policy`，服务与隐私为 `x-app-os: android`，儿童为 `web`。原站 HTML 为 JS 容器，正文通过同产品接口获取。

## 保留的来源差异

1. Google Play 头像与共享盘“新”不同，采集时仍为另一版人物头像；官网横标、App Store 与“新”同一人物姿态。`sources/brand-comparison.png` 并列保留。官网品牌采用官网真实横标，favicon/app icon 使用经官网、iOS 交叉核验的新版 iOS 图标；未把目录“新”视作唯一证据。
2. Google Play 展示开发者为 igo team，法律主体为 HAGO SINGAPORE PTE. LTD.；官网与当前隐私正文主体一致，仅拼写空格、大小写和地址括号格式不同，不伪造为另一公司。
3. Google Play 客服、官网、服务及隐私正文邮箱为 `contactezpzapp@gmail.com`，儿童正文出现 `serviceezpz@gmail.com`；商店还列开发者邮箱 `kaixin180329@gmail.com`。联系页用前者，儿童官方正文原样保留后者，待产品方确认职责分工。
4. App Store 的历史名称 Dera、bundleId `com.joyy.dera` 与 Android `com.party.ezpz` 不同，但官网直接链接同一 Apple ID，当前 Apple lookup 明确返回 Ezpz (Dera)。保留这项历史命名事实。
5. 官网首页与底部代码的版权起始年分别出现 2023、2024；评审版只显示当前年 2026 与核验主体，不自定成立日期。

## 缺失项清单来源

飞书链接 https://lp3jrqympq.feishu.cn/wiki/X4Czwro8ci1QBikh3uRccNDMnsb?sheet=ymlzGV 匿名请求被重定向到 Feishu 登录页，本次没有读取在线工作表权限。没有把登录页当作清单正文。

为继续核对，读取用户工作区现有 `G:\26.11.05-官网优化\官网缺失项.xlsx` 的本地快照，仅提取、不改写。它列有 Ezpz 的下载导航、支付、用户支持、安全政策、多语言、产品介绍、统计七类缺失；提取记录为 `sources/local-checklist.json`。本地快照不代表飞书最新状态，差异需工作表负责人复核；逐项接入状态见 `HANDOFF.md`。

## 素材与母版

共享盘原件保持不变。项目 `brand/android-original.png`、`brand/ios-original.png` 为副本。原站真实横标与图标比较图在 `sources/`。

`template/ola19.html` 是指定提交的结构证据，保留原始品牌、协议和内部事件；这些原文仅用于布局测量，不会作为 Ezpz 正式内容显示。构建输出中不加载旧品牌素材或目的链接。通用字体、下载徽章原样复用。
