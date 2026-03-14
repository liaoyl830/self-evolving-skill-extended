# GitHub 推送指南

**创建时间:** 2026-03-14 01:10  
**仓库地址:** https://github.com/liaoyl830/openclaw-skills-ext

---

## ⚠️ 推送失败原因

网络连接超时，可能是：
- 网络问题
- GitHub 访问限制
- 防火墙阻止

---

## ✅ 手动推送步骤

### 方法 1: 使用 Git 命令行

```bash
cd C:\Users\liaoy\.openclaw\workspace\skills\self-evolving-skill

# 1. 确认远程仓库
git remote -v
# 应该显示：origin  https://github.com/liaoyl830/openclaw-skills-ext.git

# 2. 推送
git push -u origin main
```

**需要输入:**
- GitHub 用户名：`liaoyl830`
- GitHub 密码或 Token

**如果使用 Token:**
```
Username: liaoyl830
Password: ghp_xxxxxxxxxxxx (您的 Personal Access Token)
```

---

### 方法 2: 使用 GitHub Desktop

1. 下载 GitHub Desktop: https://desktop.github.com/
2. 登录 GitHub 账号
3. 添加本地仓库
4. 点击 "Push origin"

---

### 方法 3: 使用 VS Code

1. 打开 VS Code
2. 打开文件夹：`C:\Users\liaoy\.openclaw\workspace\skills\self-evolving-skill`
3. 点击左侧 Git 图标
4. 点击 "..." → Push

---

## 🔑 获取 GitHub Token

如果密码登录失败，需要创建 Personal Access Token:

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写说明：`sessions-yield`
4. 选择权限：
   - ✅ repo (全部勾选)
   - ✅ workflow
5. 点击 "Generate token"
6. **复制 Token** (只显示一次！)
7. 推送时使用 Token 作为密码

---

## 📊 当前状态

| 项目 | 状态 |
|------|------|
| Git 仓库 | ✅ 已初始化 |
| 文件提交 | ✅ 323 个文件 |
| 远程仓库 | ✅ 已配置 |
| 分支名称 | ✅ main |
| 推送状态 | ⏸️ 待推送 |

---

## 🎯 推送成功后

1. **访问仓库:** https://github.com/liaoyl830/openclaw-skills-ext
2. **检查文件:** 确认所有文件已上传
3. **完善 README:** 在 GitHub 上查看 README 显示
4. **添加 Topics:** 
   - openclaw
   - async
   - review
   - productivity
   - sessions-yield

---

## 📦 ClawHub 发布

GitHub 推送完成后，发布到 ClawHub:

```bash
cd C:\Users\liaoy\.openclaw\workspace\skills\self-evolving-skill
publish-to-clawhub.bat
```

**或手动:**
```bash
npx clawhub login
npx clawhub publish .
```

---

## ❓ 常见问题

### Q: 推送时提示认证失败？

**A:** 使用 Personal Access Token 代替密码

### Q: 连接超时？

**A:** 
- 检查网络连接
- 尝试使用代理
- 稍后重试

### Q: 权限不足？

**A:** 确认您是仓库所有者或有写入权限

---

*指南版本：1.0*  
*最后更新：2026-03-14*

