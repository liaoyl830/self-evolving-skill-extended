# OpenClaw Skills Extension

> **OpenClaw 技能扩展项目**

本项目包含为 OpenClaw 开发的扩展技能，当前主要项目：

## 📦 已包含技能

### self-evolving-skill-extended

**自进化技能系统 - 扩展增强版**

- 🚀 异步复盘系统（30 秒 → <1 秒，提升 96%）
- 🔔 通知管理器（5 种通知方式）
- 🛡️ 完整错误处理（自动重试 + 降级链）
- 🔌 OpenClaw 深度集成

**位置**: [`skills/self-evolving-skill-extended/`](skills/self-evolving-skill-extended/)

**详细说明**: [查看子项目 README](skills/self-evolving-skill-extended/README.md)

---

## 📁 项目结构

```
openclaw-skills-extension/
├── skills/
│   └── self-evolving-skill-extended/    # 自进化技能（扩展版）
├── memory/                               # 记忆文件
├── .gitattributes                        # Git 编码配置
├── .gitignore                            # Git 排除规则
└── README.md                             # 本文件
```

---

## 🚀 快速开始

### 安装 OpenClaw

参考官方文档：https://docs.openclaw.ai

### 使用技能

```python
from sessions_yield_adapter import SessionsYieldAdapter

adapter = SessionsYieldAdapter()
result = adapter.start_background_review({
    'tasks_completed': 9
})

print(result['message'])
# 🫡 收到，开始复盘今日任务...
```

详细用法：[self-evolving-skill-extended 用户指南](skills/self-evolving-skill-extended/USER_GUIDE.md)

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [开发背景](skills/self-evolving-skill-extended/DEVELOPMENT_BACKGROUND.md) | 为什么要开发扩展版本 |
| [用户指南](skills/self-evolving-skill-extended/USER_GUIDE.md) | 详细使用说明 |
| [API 参考](skills/self-evolving-skill-extended/API_REFERENCE.md) | API 文档 |
| [安装指南](skills/self-evolving-skill-extended/INSTALLATION.md) | 安装步骤 |

---

## 🎯 开发背景

本项目是基于原始 [self-evolving-skill](https://github.com/whtoo/self-evolving-bot) 的扩展增强版本。

**为什么要开发扩展版本？**
- ✅ 异步复盘系统（响应速度提升 96%）
- ✅ 新增通知管理器
- ✅ 完整错误处理
- ✅ OpenClaw 深度集成

详见：[开发背景与动机](skills/self-evolving-skill-extended/DEVELOPMENT_BACKGROUND.md)

---

## 📊 性能对比

| 指标 | 旧方案 | 新方案 | 提升 |
|------|--------|--------|------|
| 首次响应 | 30 秒 | <1 秒 | ⬆️ 96% |
| 用户等待 | 30 秒 | 0 秒 | ✅ 无感知 |
| 后台处理 | 阻塞 | 非阻塞 | ✅ 并发 |

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

### 分支管理

- `main` - 稳定版本
- `dev` - 开发分支

### 提交流程

1. 从 `dev` 切出功能分支：`feature/xxx`
2. 开发完成后提交 PR 到 `dev`
3. Review 通过后合并

详见：[贡献指南](CONTRIBUTING.md)（待创建）

---

## 📄 许可证

遵循原项目许可证。

---

## 🔗 相关链接

- **OpenClaw 官网**: https://openclaw.ai
- **OpenClaw 文档**: https://docs.openclaw.ai
- **原始项目**: https://github.com/whtoo/self-evolving-bot

---

**最后更新**: 2026-03-14  
**维护者**: 小斗 🦞
