# self-evolving-skill-extended

> **自进化技能系统 - 扩展增强版**  
> **Self-Evolving Skill System - Extended & Enhanced Version**

🦞 **让复盘响应速度提升 96%**  
🦞 **Improve Review Response Speed by 96%**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.12-blue)](https://openclaw.ai)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)

---

## 📖 开发背景 / Development Background

**中文：**
本项目是基于原始 [self-evolving-skill](https://github.com/whtoo/self-evolving-bot) 的扩展增强版本。

**为什么要开发扩展版本？**
- ✅ 异步复盘系统（30 秒 → <1 秒，提升 96%）
- ✅ 新增通知管理器（5 种通知方式）
- ✅ 完整错误处理（自动重试 + 降级链）
- ✅ OpenClaw 深度集成

详见：[开发背景与动机](DEVELOPMENT_BACKGROUND.md)

**English:**
This project is an extended and enhanced version of the original [self-evolving-skill](https://github.com/whtoo/self-evolving-bot).

**Why develop this extended version?**
- ✅ Async review system (30s → <1s, 96% improvement)
- ✅ New notification manager (5 notification methods)
- ✅ Complete error handling (auto-retry + degradation chain)
- ✅ Deep OpenClaw integration

See details: [Development Background & Motivation](DEVELOPMENT_BACKGROUND.md)

---

## 🎯 核心特性 / Core Features

- ⚡ **异步执行 / Async Execution** - <1 秒响应，后台自动处理 / <1s response, background auto-processing
- 🛡️ **智能降级 / Smart Degradation** - 多层保障，失败自动重试 / Multi-layer protection, auto-retry on failure
- 🔔 **多种通知 / Multiple Notifications** - 5 种通知方式，主动推送 / 5 notification methods, proactive push
- 🏗️ **错误处理 / Error Handling** - 自动重试 (3 次) + 降级链 / Auto-retry (3 times) + degradation chain
- 📚 **完整文档 / Complete Documentation** - 用户指南 + API 参考 / User guide + API reference

---

## 🚀 快速开始 / Quick Start

### 安装 / Installation

```bash
# 方式 1: Git 克隆 / Git Clone
git clone https://github.com/liaoyl830/self-evolving-skill-extended.git
cd self-evolving-skill-extended

# 方式 2: ClawHub (推荐) / ClawHub (Recommended)
npx clawhub install self-evolving-skill-extended
```

### 基本使用 / Basic Usage

```python
from sessions_yield_adapter import SessionsYieldAdapter

# 创建适配器 / Create adapter
adapter = SessionsYieldAdapter()

# 异步复盘 (<1 秒响应) / Async review (<1s response)
result = adapter.start_background_review({
    'tasks_completed': 9,
    'skills_installed': 7
})

print(result['message'])
# 🫡 收到，开始复盘今日任务...
# 🫡 Received, starting today's task review...
```

### OpenClaw 集成 / OpenClaw Integration

```python
from openclaw_integration import OpenClawReviewTool

tool = OpenClawReviewTool()

# 异步复盘 / Async review
result = tool.daily_review(
    context={'tasks_completed': 9},
    async_mode=True
)

# 在 OpenClaw 中使用 / Use in OpenClaw
await sessions_yield({
    message: result['message'],
    followUp: result['followUp']
})
```

---

## 📊 性能对比 / Performance Comparison

| 指标 / Metric | 旧方案 / Old | 新方案 / New | 提升 / Improvement |
|---------------|--------------|--------------|-------------------|
| **首次响应 / First Response** | 30 秒 / 30s | <1 秒 / <1s | ⬆️ 96% |
| **用户等待 / User Wait** | 30 秒 / 30s | 0 秒 / 0s | ✅ 无感知 / Imperceptible |
| **后台处理 / Background** | 阻塞 / Blocking | 非阻塞 / Non-blocking | ✅ 并发 / Concurrent |
| **错误恢复 / Error Recovery** | 手动 / Manual | 自动 / Auto | ✅ 智能 / Smart |

---

## 📁 项目结构 / Project Structure

```
self-evolving-skill-extended/
├── core/                          # Python 核心 / Python Core
│   ├── residual_pyramid.py        # 残差金字塔 / Residual Pyramid
│   ├── reflection_trigger.py      # 反思触发器 / Reflection Trigger
│   ├── experience_replay.py       # 经验回放 / Experience Replay
│   ├── skill_engine.py            # 技能引擎 / Skill Engine
│   ├── storage.py                 # 持久化 / Persistence
│   └── mcp_server.py              # MCP 服务器 / MCP Server
├── review_background_agent.py     # 后台复盘代理 ⭐ / Background Review Agent ⭐
├── sessions_yield_adapter.py      # 异步适配器 ⭐ / Async Adapter ⭐
├── notification_manager.py        # 通知管理器 ⭐ / Notification Manager ⭐
├── error_handler.py               # 错误处理 ⭐ / Error Handler ⭐
├── mcporter_adapter.py            # McPorter 接口 / McPorter Interface
├── openclaw_integration.py        # OpenClaw 集成 ⭐ / OpenClaw Integration ⭐
├── src/                           # TypeScript SDK
│   ├── index.ts                   # 主入口 / Main Entry
│   ├── cli.ts                     # CLI
│   └── mcp-tools.ts               # 工具定义 / Tool Definitions
├── DEVELOPMENT_BACKGROUND.md      # 开发背景 ⭐ / Development Background ⭐
├── USER_GUIDE.md                  # 用户指南 / User Guide
├── API_REFERENCE.md               # API 参考 / API Reference
└── README.md                      # 本文件 / This File

⭐ = 新增模块 / New Module
```

---

## 🧪 测试 / Testing

```bash
# 运行验证测试 / Run validation tests
python test_validation.py

# 运行完整集成测试 / Run full integration tests
python test_full_integration.py

# 运行所有测试 / Run all tests
pytest tests/
```

---

## 📚 文档 / Documentation

| 文档 / Document | 说明 / Description |
|-----------------|-------------------|
| [DEVELOPMENT_BACKGROUND.md](DEVELOPMENT_BACKGROUND.md) | 开发背景与动机 / Development Background & Motivation |
| [USER_GUIDE.md](USER_GUIDE.md) | 用户指南 / User Guide |
| [API_REFERENCE.md](API_REFERENCE.md) | API 参考 / API Reference |
| [INSTALLATION.md](INSTALLATION.md) | 安装指南 / Installation Guide |
| [PUBLISH_GUIDE.md](PUBLISH_GUIDE.md) | 发布指南 / Publish Guide |

---

## 🔧 MCP 工具 / MCP Tools

| 工具 / Tool | 说明 / Description |
|-------------|-------------------|
| `skill_review_async` | 异步复盘 / Async Review |
| `skill_review_sync` | 同步复盘（降级方案）/ Sync Review (Fallback) |
| `skill_record_execution` | 记录技能执行 / Record Skill Execution |
| `skill_check_status` | 检查任务状态 / Check Task Status |

---

## 📝 版本历史 / Version History

| 版本 / Version | 日期 / Date | 变更 / Changes |
|----------------|-------------|----------------|
| 2.0.0-extended | 2026-03-14 | 初始扩展版本 / Initial extended release |
| 1.0.0 | - | 原始版本 / Original version |

---

## 🤝 贡献 / Contributing

欢迎贡献代码、报告问题或提出建议！

Contributions, issue reports, and suggestions are welcome!

详见：[贡献指南](CONTRIBUTING.md)（待创建）

See: [Contributing Guide](CONTRIBUTING.md) (TODO)

---

## 📄 许可证 / License

本项目基于原始 self-evolving-skill 进行扩展开发，遵循原项目的许可证。

This project is an extended development based on the original self-evolving-skill, following the original project's license.

---

## 🔗 相关链接 / Related Links

- **原始项目 / Original Project:** https://github.com/whtoo/self-evolving-bot
- **扩展版本 / Extended Version:** https://github.com/liaoyl830/self-evolving-skill-extended
- **OpenClaw 官网 / OpenClaw Website:** https://openclaw.ai
- **OpenClaw 文档 / OpenClaw Docs:** https://docs.openclaw.ai

---

**最后更新 / Last Updated:** 2026-03-14  
**维护者 / Maintainer:** 小斗 🦞
