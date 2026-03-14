# OpenClaw 贡献指南

## 核心分支

| 分支名 | 类型 | 用途 | 保护规则 |
|--------|------|------|----------|
| **main** | 主分支 | 稳定可发布版本 | 🔒 仅通过 PR 合并 |
| **dev** | 开发分支 | 日常开发集成 | 🟡 可直接推送 |
| **feature/\*** | 功能分支 | 单个新功能开发 | 🟢 临时分支，合并后删除 |
| **hotfix/\*** | 修复分支 | 紧急 Bug 修复 | 🟢 临时分支，合并后删除 |

---

## 开发流程

### 1. 新功能开发

```bash
# 从 dev 切出功能分支
git checkout dev
git checkout -b feature/功能描述

# 开发完成后提交
git add -A
git commit -m "feat: 新增 XX 功能"

# 推送到远程
git push -u origin feature/功能描述

# GitHub 上创建 PR 到 dev 分支
# Review 通过后合并，删除分支
```

### 2. 紧急 Bug 修复

```bash
# 从 main 切出修复分支
git checkout main
git checkout -b hotfix/问题描述

# 修复后合并到 main 和 dev
git checkout main && git merge hotfix/问题描述
git checkout dev && git merge hotfix/问题描述
git push origin main dev
```

### 3. 版本发布

```bash
# dev 稳定后 PR 到 main
# 在 main 上打标签
git tag -a v1.0.0 -m "版本 1.0.0"
git push origin v1.0.0
```

---

## 提交信息规范

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: 新增异步复盘系统` |
| `fix` | Bug 修复 | `fix: 修复 UTF-8 编码问题` |
| `docs` | 文档更新 | `docs: 更新 README` |
| `refactor` | 重构 | `refactor: 优化代码结构` |
| `style` | 格式调整 | `style: 调整代码缩进` |
| `test` | 测试用例 | `test: 添加单元测试` |
| `chore` | 构建/工具 | `chore: 更新依赖` |

**格式**：
```
<type>: <描述>

[可选的详细说明]
```

---

## 编码规范

- **文件编码**：统一使用 UTF-8
- **换行符**：LF (`\n`)
- **缩进**：4 个空格
- **文件名**：不使用中文和特殊符号

---

## 代码审查清单

### 发布前检查
- [ ] 文件编码：UTF-8
- [ ] 敏感信息：无 Token/密码明文
- [ ] 本地预览：`git status` + `git diff`
- [ ] 中文内容：确认无乱码

### 发布后验证
- [ ] GitHub 网页显示正常
- [ ] 检查中文注释/文档
- [ ] 回复确认完成

---

## 分支保护规则（仓库管理员配置）

**进入 Settings → Branches → Add branch protection rule**

| 规则 | 设置 |
|------|------|
| 分支名称 | `main` |
| 禁止直接推送 | ✅ Require pull request reviews |
| Review 人数 | ✅ 至少 1 人 |
| 禁止强制推送 | ✅ Do not allow force pushes |
| 禁止删除分支 | ✅ Do not allow deletions |

---

**感谢你的贡献！** 🦞
