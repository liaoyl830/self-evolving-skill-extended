# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## 🛠️ 我的工具配置

### 代码工具 (默认)

- **OpenCode** → 首选代码工具 (v1.2.25)
- 命令：`opencode run '任务描述'`
- 模式：`pty:true` (需要伪终端)
- 用途：写代码、改代码、调试、重构、代码审查

### 使用规范

**所有代码任务自动调用 OpenCode：**

```bash
# 基本用法
bash pty:true workdir:<项目路径> command:"opencode run '任务描述'"

# 后台运行 (长时间任务)
bash pty:true workdir:<项目路径> background:true command:"opencode run '任务描述'"
```

**触发场景：**
- 写代码/创建新功能
- 修改现有代码
- 调试问题
- 代码审查
- 重构代码

---

Add whatever helps you do your job. This is your cheat sheet.
