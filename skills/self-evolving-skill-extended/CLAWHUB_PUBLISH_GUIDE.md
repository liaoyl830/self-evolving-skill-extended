# ClawHub 手动发布指南

**创建时间:** 2026-03-14 01:22

---

## ⚠️ CLI 发布失败

**原因:** clawhub CLI 版本验证问题

**解决方案:** 通过 ClawHub 网站手动发布

---

## 🌐 方法 1: 网站发布 (推荐)

### 步骤 1: 登录 ClawHub

访问：https://clawhub.ai

1. 点击右上角 "Sign In"
2. 使用 GitHub 账号登录
3. 进入 Dashboard

---

### 步骤 2: 创建新技能

1. 点击 "Create New Skill"
2. 填写技能信息:

```
Name: sessions-yield
Version: 1.0.0
Description: OpenClaw async review system with 96% performance improvement
Category: Productivity
License: MIT
Repository: https://github.com/liaoyl830/openclaw-skills-ext
```

3. 点击 "Create"

---

### 步骤 3: 上传代码

1. 选择 "Upload from GitHub"
2. 选择仓库：`liaoyl830/openclaw-skills-ext`
3. 选择分支：`main`
4. 确认文件列表
5. 点击 "Publish"

---

### 步骤 4: 审核发布

1. 等待审核 (通常 5-10 分钟)
2. 审核通过后技能上线
3. 用户可以搜索和安装

---

## 💻 方法 2: 修复 CLI 后发布

### 检查 claw.json

确保版本格式正确:

```json
{
  "name": "sessions-yield",
  "version": "1.0.0",
  "description": "OpenClaw async review system",
  "author": "liaoy",
  "license": "MIT"
}
```

### 更新 clawhub CLI

```bash
npm install -g clawhub@latest
```

### 重新登录

```bash
npx clawhub logout
npx clawhub login
```

### 发布

```bash
cd C:\Users\liaoy\.openclaw\workspace\skills\self-evolving-skill
npx clawhub publish .
```

---

## 📊 技能信息

**用于填写 ClawHub:**

| 字段 | 值 |
|------|-----|
| **Name** | sessions-yield |
| **Version** | 1.0.0 |
| **Description** | OpenClaw async review system with 96% performance improvement |
| **Author** | liaoy |
| **License** | MIT |
| **Category** | Productivity |
| **Tags** | review, async, productivity, openclaw |
| **Repository** | https://github.com/liaoyl830/openclaw-skills-ext |
| **Homepage** | https://github.com/liaoyl830/openclaw-skills-ext#readme |

---

## 🎯 发布后验证

### 搜索技能

```bash
npx clawhub search sessions-yield
```

### 查看技能详情

```bash
npx clawhub inspect liaoy/sessions-yield
```

### 测试安装

```bash
npx clawhub add liaoy/sessions-yield
```

---

## ❓ 常见问题

### Q: 技能审核需要多久？

**A:** 通常 5-10 分钟，最长 24 小时

### Q: 如何查看发布状态？

**A:** 登录 ClawHub Dashboard 查看

### Q: 发布失败怎么办？

**A:** 
1. 检查 claw.json 格式
2. 确认所有必需文件存在
3. 联系 ClawHub 支持

---

## 📞 需要帮助？

- ClawHub 文档：https://docs.clawhub.ai
- 社区支持：https://discord.gg/openclaw
- GitHub Issues: https://github.com/liaoyl830/openclaw-skills-ext/issues

---

*指南版本：1.0*  
*最后更新：2026-03-14*

