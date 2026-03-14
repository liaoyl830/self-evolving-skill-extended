# GitHub 发布检查清单

> **重要**：发布前必须逐项检查，发布后必须验证

---

## 📋 发布前检查

### 1. 文件编码检查

- [ ] 所有文本文件使用 UTF-8 编码
- [ ] `.gitattributes` 已配置强制 UTF-8
- [ ] Python 文件有 `# -*- coding: utf-8 -*-` 声明（可选，推荐）
- [ ] 中文内容在本地编辑器中显示正常

**检查命令**:
```bash
# 查看要提交的文件
git status

# 检查文件内容
git diff --cached
```

---

### 2. 敏感信息检查

- [ ] 无 API Token 明文（ghp_*, sk-*, clh_* 等）
- [ ] 无密码明文
- [ ] 无私钥文件（*.pem, *.key）
- [ ] `.env` 文件已添加到 `.gitignore`
- [ ] 配置文件中的敏感信息已移除或用占位符

**敏感信息模式**:
```
ghp_*      # GitHub Token
sk-*       # API Key
clh_*      # ClawHub Token
password   # 密码
secret     # 密钥
api_key    # API 密钥
```

**检查命令**:
```bash
# 搜索可能的敏感信息
grep -r "ghp_\|sk-\|clh_\|password\|secret\|api_key" --include="*.py" --include="*.md" --include="*.json" .
```

---

### 3. Git 状态检查

- [ ] `git status` 预览要提交的文件
- [ ] 无意外文件（node_modules/, __pycache__/, .env 等）
- [ ] `.gitignore` 已配置
- [ ] 提交信息清晰描述变更

**检查命令**:
```bash
# 查看状态
git status

# 查看变更内容
git diff --cached

# 查看提交历史
git log --oneline -5
```

---

### 4. 中文内容检查

- [ ] README.md 中文显示正常
- [ ] 代码注释中文正常
- [ ] 文档文件中文正常
- [ ] 无乱码字符（鍓佺爜等）

---

## 🚀 发布步骤

```bash
# 1. 添加文件
git add -A

# 2. 预览
git status
git diff --cached

# 3. 提交
git commit -m "feat: 描述变更内容"

# 4. 推送
git push -u origin master
```

---

## ✅ 发布后验证

### 1. GitHub 网页验证

- [ ] 打开仓库页面：https://github.com/liaoyl830/openclaw-skills-ext
- [ ] 检查 README 显示正常
- [ ] 检查代码文件中文注释正常
- [ ] 检查文件列表完整
- [ ] 检查最新提交记录

### 2. 用户确认

- [ ] 回复用户确认完成
- [ ] 提供仓库链接
- [ ] 说明主要变更

---

## 📝 检查记录模板

```markdown
## 发布检查记录

**日期**: YYYY-MM-DD HH:mm
**版本**: v1.x.x
**检查者**: 小斗

### 发布前检查
- [x] 文件编码：UTF-8
- [x] 敏感信息：无泄露
- [x] Git 状态：正常
- [x] 中文内容：无乱码

### 发布后验证
- [x] GitHub 网页：显示正常
- [x] 用户确认：已完成

**备注**: （如有问题在此说明）
```

---

## 🔄 持续改进

每次发布后复盘：
1. 是否有遗漏的检查项？
2. 是否有可以自动化的步骤？
3. 是否需要更新检查清单？

---

**最后更新**: 2026-03-14  
**版本**: v1.0
