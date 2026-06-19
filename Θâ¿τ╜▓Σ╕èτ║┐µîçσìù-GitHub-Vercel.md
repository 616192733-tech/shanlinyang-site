# 衫琳漾独立站 · GitHub + Vercel 上线指南

域名:**www.shanlinyang.com**(站内 canonical 全部用 www)

## A. 部署(纯静态,无需构建)
1. 把本文件夹**作为仓库根目录**推到 GitHub。
2. Vercel → New Project → Import 这个仓库。
   - Framework Preset: **Other**
   - Build Command: 留空     Output Directory: 留空(根目录)
3. Deploy,拿到 `*.vercel.app` 预览地址,先确认站点正常。
   - `vercel.json` 已配置安全响应头 + 锁定 URL 形态(`.html` 直出,匹配 canonical),无需改动。

## B. 绑定域名
4. Vercel 项目 → Settings → Domains → 添加 `shanlinyang.com` 与 `www.shanlinyang.com`。
5. **把 `www.shanlinyang.com` 设为 Primary**,让 `shanlinyang.com` → www 做 301(与 canonical 一致,避免重复内容)。
6. 按 Vercel 给的记录在域名注册商配 DNS(apex 用 A/ALIAS,www 用 CNAME)。HTTPS 由 Vercel 自动签发。

## C. 上线前必做的替换(代码里是占位,务必改)
7. **GA4**:全仓库查找替换 `G-XXXXXXXXXX` → 你在 analytics.google.com 的真实 Measurement ID(26 页都有)。
8. **询盘表单**:`contact.html` 里 `YOUR-WEB3FORMS-ACCESS-KEY` → web3forms.com 申请的真实 key(收件箱 616192733@qq.com 先点验证邮件)。
   - 表单已做成:提交后**页面内显示成功**;若发送失败**自动回退**到邮箱 / WhatsApp。换上 key 即完整可用。
   - 备选(送达更稳):改用 Vercel 无服务器函数 + Resend,用自有域名发信。
   - 建议:别用个人 qq 收询盘,换成送达更好的邮箱(Gmail / 自有域名企业邮箱 sales@shanlinyang.com)。

## D. 收录(决定有没有自然流量)
9. **Google Search Console**:添加 `https://www.shanlinyang.com` 资源 → 验证 → 提交 `sitemap.xml` → 请求编入索引。
10. **Bing Webmaster Tools**:同样操作(Copilot 等 AI 取数靠 Bing)。

## 已就位(无需再动)
全站 WebP(图片 -63%)· 唯一 title / canonical / JSON-LD(Product/FAQPage/BreadcrumbList/Organization/Article…)· robots 放行 GPTBot/ClaudeBot/PerplexityBot/Google-Extended · llms.txt · 安全响应头(vercel.json)· 404 页 · 移动端自适应。

## 待补(可上线后做)
20 张 catalog 占位图换真图 · 丝绒详情页换图 · 持有真实认证时上证书 · 偏长 title/description 可精简 · 博客持续更新。
