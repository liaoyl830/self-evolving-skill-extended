# MEMORY.md - 长期记忆

_重要事件、决策、上下文和教训的精选记录_

---

## 2026-03-13

- **系统初始化完成** - OpenClaw 2026.3.12 部署完成
- **身份确立** - 小斗，直接干练风格
- **模型配置** - 百炼 qwen3.5-plus (1000k 上下文)
- **位置** - 深圳
- **权限配置** - Gateway 以管理员身份运行 (HighestAvailable)
- **网络搜索** - Tavily API 已配置
- **代码工具** - OpenCode v1.2.25 设为默认代码工具

---

## 代码工具配置

**默认代码工具：OpenCode**

所有代码相关任务自动使用 OpenCode：
- 写代码/创建新功能
- 修改现有代码
- 调试问题
- 代码审查
- 重构

命令：`opencode run '任务描述'` (pty:true)

---

## 行为规则 (2026-03-13)

### 模棱两可指令处理
- 指令有歧义时立即暂停
- 列出所有可能性和选项
- 等用户选择后再执行

### 复盘规则
- **触发词**: "复盘"、"回顾"、"总结今天"
- **动作**: 调用 self-evolving-skill + 人工反思
- **记录**: memory/YYYY-MM-DD.md + MEMORY.md

---

## API Token 配置

### GitHub

- **Token:** `已存储在 ~/.openclaw/.env`
- **类型:** Personal Access Token (Classic)
- **用途:** GitHub API 访问、PR 操作、仓库管理
- **存储:** `~/.openclaw/.env` → `GITHUB_TOKEN`

### ClawHub

- **Token:** `clh_nLRaCWXfzGiC7-4-NLwmvtvA8mMO8TpmjQ2JsA93P5g`
- **用途:** ClawHub 技能注册表访问、安装/发布技能
- **存储:** `~/.openclaw/.env` → `CLAWHUB_TOKEN`

---

_随时间更新重要事件和教训_
