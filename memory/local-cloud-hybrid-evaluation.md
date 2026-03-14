# 本地模型 + 云端混合方案可行性评估报告

**评估时间:** 2026-03-14 00:15  
**评估者:** 小斗 🦞  
**主机配置:** ASUS + AMD Ryzen 7 9800X3D + AMD Radeon RX 9070 XT + 48GB RAM

---

## 📋 执行摘要

| 维度 | 评估 |
|------|------|
| **硬件可行性** | ✅ 高 (75%) |
| **GPU 兼容性** | ⚠️ 中 (AMD ROCm) |
| **内存充足度** | ✅ 优秀 (48GB) |
| **存储空间** | ✅ 优秀 (1.8TB 可用) |
| **网络条件** | ✅ 1 Gbps |
| **推荐优先级** | ⭐⭐ 中低 |

**结论:** 硬件配置足够，但 AMD GPU 在 Windows 上的 LLM 支持有限，建议以 CPU 推理 + 云端协作为主。

---

## 1️⃣ 主机配置分析

### 1.1 硬件规格

| 组件 | 规格 | LLM 推理评分 |
|------|------|-------------|
| **CPU** | AMD Ryzen 7 9800X3D (8 核 16 线程, 4.7GHz) | ⭐⭐⭐⭐ |
| **GPU** | AMD Radeon RX 9070 XT (16GB VRAM) | ⭐⭐ (ROCm 支持有限) |
| **内存** | 48 GB DDR5 | ⭐⭐⭐⭐⭐ |
| **存储** | 1.8TB 可用 SSD | ⭐⭐⭐⭐⭐ |
| **网络** | 1 Gbps 以太网 | ⭐⭐⭐⭐ |

### 1.2 优势分析

| 优势 | 说明 |
|------|------|
| **大内存** | 48GB 可加载 7B-13B 参数模型 |
| **多核心** | 8 核 16 线程适合 CPU 推理 |
| **大存储** | 可存储多个模型文件 |
| **新 CPU** | 9800X3D 的 3D V-Cache 对推理友好 |

### 1.3 劣势分析

| 劣势 | 说明 |
|------|------|
| **AMD GPU** | ROCm Windows 支持不成熟 |
| **无 CUDA** | 无法使用优化的 NVIDIA 生态 |
| **VRAM 限制** | 16GB 只能运行小模型 |

---

## 2️⃣ 本地模型方案对比

### 2.1 方案 A: Ollama (CPU 推理)

**推荐指数:** ⭐⭐⭐⭐

| 项目 | 详情 |
|------|------|
| **安装** | `winget install Ollama.Ollama` |
| **推理后端** | CPU (AVX2 优化) |
| **支持模型** | Llama 3.2, Phi-3, Mistral, Qwen2.5 |
| **内存需求** | 7B 模型约 4-8GB |
| **推理速度** | 7B 模型 ~5-10 tokens/s |
| **Windows 支持** | ✅ 完美 |

**适合场景:**
- 快速原型开发
- 代码补全/审查
- 简单问答
- 离线环境

**示例命令:**
```bash
# 安装
winget install Ollama.Ollama

# 运行 7B 模型
ollama run llama3.2:7b

# 运行 3B 模型 (更快)
ollama run llama3.2:3b

# 运行代码专用模型
ollama run codellama:7b
```

### 2.2 方案 B: LM Studio (GPU 加速)

**推荐指数:** ⭐⭐⭐

| 项目 | 详情 |
|------|------|
| **安装** | 下载 exe 安装包 |
| **推理后端** | Vulkan (支持 AMD) |
| **支持模型** | GGUF 格式 |
| **GPU 加速** | ✅ AMD Vulkan |
| **推理速度** | 7B 模型 ~10-20 tokens/s |
| **Windows 支持** | ✅ 良好 |

**适合场景:**
- 需要 GPU 加速
- 图形化界面需求
- 模型实验

**注意:** AMD GPU 需要 Vulkan 支持，性能不如 CUDA。

### 2.3 方案 C: KoboldCPP (CPU+GPU 混合)

**推荐指数:** ⭐⭐⭐⭐

| 项目 | 详情 |
|------|------|
| **安装** | 下载单文件 exe |
| **推理后端** | CPU + OpenCL (AMD) |
| **支持模型** | GGUF 格式 |
| **混合推理** | ✅ CPU+GPU 分层 |
| **推理速度** | 7B 模型 ~15-25 tokens/s |
| **Windows 支持** | ✅ 良好 |

**适合场景:**
- 最大化硬件利用
- 中等规模模型 (7B-13B)
- 需要 API 接口

---

## 3️⃣ 混合架构设计

### 3.1 推荐架构

```
┌─────────────────────────────────────────┐
│          用户请求 (OpenClaw)             │
└─────────────────┬───────────────────────┘
                  │
         ┌────────▼────────┐
         │   智能路由器     │
         │  (任务分类器)    │
         └────────┬────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌────────┐  ┌────────┐  ┌────────────┐
│ 简单任务│  │ 中等任务│  │  复杂任务   │
│ <5 秒   │  │ 5-30 秒  │  │ >30 秒     │
└───┬────┘  └───┬────┘  └─────┬──────┘
    │          │             │
    ▼          ▼             ▼
┌────────┐  ┌────────┐  ┌────────────┐
│ 本地   │  │ 本地   │  │  云端       │
│ CPU    │  │ CPU+GPU│  │  百炼      │
│ 3B 模型 │  │ 7B 模型 │  │  qwen3.5  │
└────────┘  └────────┘  └────────────┘
```

### 3.2 任务分类规则

| 任务类型 | 路由目标 | 判断依据 |
|----------|----------|----------|
| **代码补全** | 本地 | 短文本、低延迟需求 |
| **简单问答** | 本地 | 事实性问题、<100 tokens |
| **文档总结** | 云端 | 长文本、需要理解 |
| **复杂推理** | 云端 | 多步骤、逻辑复杂 |
| **创意写作** | 云端 | 需要高质量输出 |
| **数据提取** | 本地 | 结构化任务 |
| **翻译** | 混合 | 短文本本地，长文本云端 |

### 3.3 智能路由实现

```python
# smart_router.py
class SmartRouter:
    def __init__(self):
        self.local_model = LocalModel()  # Ollama
        self.cloud_model = CloudModel()  # 百炼
    
    def route(self, task: str, context: dict) -> str:
        # 任务分类
        task_type = self.classify_task(task, context)
        
        if task_type == 'simple':
            # 本地快速处理
            return self.local_model.generate(task, max_tokens=256)
        
        elif task_type == 'medium':
            # 尝试本地，超时切云端
            try:
                return self.local_model.generate(
                    task, 
                    max_tokens=512,
                    timeout=10  # 10 秒超时
                )
            except TimeoutError:
                return self.cloud_model.generate(task)
        
        else:  # complex
            # 直接云端
            return self.cloud_model.generate(task, max_tokens=2048)
    
    def classify_task(self, task: str, context: dict) -> str:
        # 简单规则分类
        if len(task) < 100 and context.get('type') == 'code_completion':
            return 'simple'
        
        if len(task) < 500 and context.get('type') in ['qa', 'extraction']:
            return 'medium'
        
        return 'complex'
```

---

## 4️⃣ 应用场景评估

### 4.1 高价值场景 (推荐)

#### 场景 1: 代码补全 ⭐⭐⭐⭐⭐

**需求:** 低延迟 (<1 秒)  
**本地方案:** Ollama + CodeLlama-7B  
**预期效果:**
- 响应时间：0.5-2 秒
- 准确率：70-80%
- 离线可用：✅

**配置:**
```bash
ollama run codellama:7b
```

**成本对比:**
| 方案 | 延迟 | 成本 | 质量 |
|------|------|------|------|
| 本地 | 1 秒 | $0 | 70% |
| 云端 | 3 秒 | $0.01/次 | 95% |

**建议:** 代码补全用本地，复杂重构用云端

---

#### 场景 2: 离线隐私场景 ⭐⭐⭐⭐⭐

**需求:** 数据不出本地  
**本地方案:** Ollama + Llama-3.2-3B  
**预期效果:**
- 完全离线
- 隐私保护
- 响应时间：1-3 秒

**适用:**
- 敏感文档处理
- 内部数据查询
- 合规要求场景

---

#### 场景 3: 高频简单任务 ⭐⭐⭐⭐

**需求:** 大量重复简单查询  
**本地方案:** Ollama + Phi-3-mini (3.8B)  
**预期效果:**
- 响应时间：<2 秒
- 成本：$0
- 并发：10-20 请求/分钟

**适用:**
- 日志分析
- 数据提取
- 格式转换

---

### 4.2 中价值场景 (可选)

#### 场景 4: 文档总结 ⭐⭐⭐

**需求:** 中长文本理解  
**混合方案:** 本地预处理 + 云端总结  
**流程:**
```
本地：提取关键句 → 云端：生成总结 → 本地：格式化输出
```

**预期效果:**
- 减少云端 token 消耗 40-60%
- 保持总结质量
- 总成本降低 30%

---

#### 场景 5: 多轮对话 ⭐⭐⭐

**需求:** 上下文保持  
**混合方案:** 本地短期记忆 + 云端长期记忆  
**架构:**
```
本地缓存：最近 5 轮对话
云端存储：完整对话历史
```

---

### 4.3 低价值场景 (不推荐)

#### 场景 6: 复杂推理 ⭐

**原因:**
- 本地模型能力有限
- 容易出错
- 调试困难

**建议:** 直接用云端

#### 场景 7: 创意写作 ⭐

**原因:**
- 本地模型质量差距大
- 需要多次迭代
- 时间成本高

**建议:** 直接用云端

---

## 5️⃣ 实施成本估算

### 5.1 硬件成本

| 项目 | 当前 | 需要升级 | 成本 |
|------|------|----------|------|
| CPU | ✅ 9800X3D | 否 | $0 |
| GPU | ⚠️ RX 9070 XT | 可选 | $0 |
| 内存 | ✅ 48GB | 否 | $0 |
| 存储 | ✅ 1.8TB | 否 | $0 |
| **总计** | - | - | **$0** |

### 5.2 软件成本

| 软件 | 许可 | 成本 |
|------|------|------|
| Ollama | Apache 2.0 | $0 |
| LM Studio | 免费 | $0 |
| KoboldCPP | MIT | $0 |
| **总计** | - | **$0** |

### 5.3 模型成本

| 模型 | 大小 | 下载时间 | 存储 |
|------|------|----------|------|
| Llama-3.2-3B | 2GB | 5 分钟 | 2GB |
| Llama-3.2-7B | 4GB | 10 分钟 | 4GB |
| CodeLlama-7B | 4GB | 10 分钟 | 4GB |
| Phi-3-mini | 2GB | 5 分钟 | 2GB |
| **总计** | - | **30 分钟** | **12GB** |

### 5.4 时间成本

| 任务 | 时间 |
|------|------|
| 安装 Ollama | 10 分钟 |
| 下载模型 | 30 分钟 |
| 配置路由 | 1-2 小时 |
| 测试调优 | 2-3 小时 |
| **总计** | **4-6 小时** |

---

## 6️⃣ 预期收益

### 6.1 成本节约

**假设场景:** 每日 100 次请求

| 请求类型 | 本地比例 | 云端节省 | 月节省 |
|----------|----------|----------|--------|
| 代码补全 | 80% | $24/月 | $19/月 |
| 简单问答 | 60% | $18/月 | $11/月 |
| 数据提取 | 70% | $21/月 | $15/月 |
| **总计** | - | **$63/月** | **$45/月** |

**年节省:** ~$540

### 6.2 性能提升

| 指标 | 纯云端 | 混合方案 | 提升 |
|------|--------|----------|------|
| 简单任务延迟 | 3 秒 | 1 秒 | ⬆️ 67% |
| 离线可用性 | ❌ | ✅ | 100% |
| 隐私保护 | ❌ | ✅ | 100% |

### 6.3 用户体验

| 场景 | 当前 | 优化后 |
|------|------|--------|
| 代码补全 | 等 3 秒 |  instant |
| 离线环境 | 不可用 | 正常用 |
| 敏感数据 | 担心泄露 | 本地处理 |

---

## 7️⃣ 技术风险

### 7.1 风险矩阵

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| AMD GPU 驱动问题 | 高 (60%) | 中 | 用 CPU 推理 |
| 模型质量不足 | 中 (40%) | 中 | 智能路由切云端 |
| 内存不足 | 低 (10%) | 高 | 监控 + 自动卸载 |
| 推理速度慢 | 中 (30%) | 低 | 用小模型 |

### 7.2 兼容性检查

| 组件 | 状态 | 说明 |
|------|------|------|
| Windows 11 | ✅ 兼容 | 当前系统 |
| AMD ROCm | ⚠️ 有限 | 不支持所有模型 |
| Ollama | ✅ 兼容 | 原生支持 |
| 48GB RAM | ✅ 充足 | 可跑 13B 模型 |

---

## 8️⃣ 推荐实施方案

### 阶段 1: 基础安装 (30 分钟)

```bash
# 1. 安装 Ollama
winget install Ollama.Ollama

# 2. 验证安装
ollama --version

# 3. 下载轻量模型
ollama pull llama3.2:3b
ollama pull phi3:mini

# 4. 测试运行
ollama run llama3.2:3b "Hello"
```

### 阶段 2: 集成 OpenClaw (1-2 小时)

```python
# 创建本地模型适配器
# local_model_adapter.py

import requests
import json

class LocalModelAdapter:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, prompt: str, model: str = "llama3.2:3b", timeout: int = 10):
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 256
                }
            },
            timeout=timeout
        )
        return response.json()["response"]
    
    def chat(self, messages: list, model: str = "llama3.2:3b"):
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": model,
                "messages": messages,
                "stream": False
            },
            timeout=10
        )
        return response.json()["message"]["content"]
```

### 阶段 3: 智能路由 (2-3 小时)

```python
# smart_router.py (集成到 Self-Evolving Skill)

class HybridRouter:
    def __init__(self):
        self.local = LocalModelAdapter()
        self.cloud = CloudModelAdapter()  # 百炼
    
    def execute(self, task: str, context: dict):
        # 分类任务
        task_type = self.classify(task, context)
        
        if task_type == 'local':
            try:
                return self.local.generate(task, timeout=10)
            except:
                # 降级到云端
                return self.cloud.generate(task)
        else:
            return self.cloud.generate(task)
```

### 阶段 4: 测试优化 (1-2 小时)

```bash
# 测试脚本
py test_hybrid_router.py

# 性能基准
# - 简单任务：本地 vs 云端
# - 复杂任务：质量对比
# - 混合场景：成本分析
```

---

## 9️⃣ 最终建议

### ✅ 推荐实施

**理由:**
1. **零硬件成本** - 利用现有配置
2. **显著延迟降低** - 简单任务 67% 提升
3. **离线能力** - 隐私保护
4. **成本节约** - 月省$45

### 📋 实施范围

**优先场景:**
1. 代码补全 (高频、低延迟)
2. 离线场景 (隐私需求)
3. 简单问答 (成本优化)

**暂不实施:**
1. 复杂推理 (质量不足)
2. 创意写作 (效果差)
3. 长文本处理 (内存限制)

### ⚠️ 注意事项

1. **AMD GPU 限制** - 主要用 CPU 推理
2. **模型质量** - 本地模型只适合简单任务
3. **智能路由** - 必须实现自动降级
4. **监控指标** - 追踪成功率/延迟

---

## 🔟 成功标准

### 技术指标

- [ ] 简单任务本地化率 > 60%
- [ ] 本地响应时间 < 2 秒
- [ ] 降级成功率 > 99%
- [ ] 月度成本节约 > $30

### 用户体验指标

- [ ] 代码补全延迟 < 1 秒
- [ ] 离线功能可用
- [ ] 用户无感知切换

---

**评估结论：** 建议实施基础本地模型方案 (Ollama + CPU 推理),4-6 小时完成，优先代码补全和离线场景。

**下一步:** 等待主人批准后开始阶段 1 安装。

---

*报告生成时间：2026-03-14 00:15*  
*评估者：小斗 🦞*
