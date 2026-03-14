# sessions_yield API 参考

**版本:** 1.0  
**更新时间:** 2026-03-14  
**适用对象:** 开发者

---

## 📋 目录

1. [核心模块](#核心模块)
2. [API 详解](#api-详解)
3. [使用示例](#使用示例)
4. [错误处理](#错误处理)
5. [最佳实践](#最佳实践)

---

## 🔧 核心模块

### 模块结构

```
self-evolving-skill/
├── review_background_agent.py    # 后台复盘代理
├── sessions_yield_adapter.py     # sessions_yield 适配器
├── notification_manager.py       # 通知管理器
├── error_handler.py              # 错误处理
├── mcporter_adapter.py           # McPorter 接口
├── openclaw_integration.py       # OpenClaw 集成
└── skill_engine.py               # 技能引擎
```

---

## 📖 API 详解

### 1. ReviewBackgroundAgent

**文件:** `review_background_agent.py`

**类:** `ReviewBackgroundAgent`

#### 初始化

```python
from review_background_agent import ReviewBackgroundAgent

agent = ReviewBackgroundAgent(storage_dir=None)
```

**参数:**
- `storage_dir` (可选): 存储目录，默认使用系统目录

**返回:**
- `ReviewBackgroundAgent` 实例

---

#### execute_review()

执行完整复盘流程

```python
result = agent.execute_review(context={
    'tasks_completed': 9,
    'skills_installed': 7,
    'value': 0.95
})
```

**参数:**
- `context` (dict): 复盘上下文
  - `tasks_completed` (int): 完成任务数
  - `skills_installed` (int): 安装技能数
  - `value` (float): 价值实现度 (0-1)

**返回:**
```python
{
    'success': bool,
    'date': str,
    'tasks_completed': int,
    'skills_installed': int,
    'skill_executed': str,
    'reflection_triggered': bool,
    'report_path': str,
    'summary': str,
    'notification_sent': bool
}
```

---

#### get_status()

获取代理状态

```python
status = agent.get_status()
```

**返回:**
```python
{
    'initialized': bool,
    'skills_loaded': int,
    'storage_dir': str,
    'memory_dir': str
}
```

---

### 2. SessionsYieldAdapter

**文件:** `sessions_yield_adapter.py`

**类:** `SessionsYieldAdapter`

#### 初始化

```python
from sessions_yield_adapter import SessionsYieldAdapter

adapter = SessionsYieldAdapter()
```

---

#### start_background_review()

启动后台复盘 (立即返回)

```python
result = adapter.start_background_review(context={
    'tasks_completed': 9,
    'skills_installed': 7
})
```

**参数:**
- `context` (dict): 复盘上下文

**返回:**
```python
{
    'success': bool,
    'task_id': str,
    'status': 'running',
    'pid': int,
    'message': str,
    'estimated_time': str
}
```

**使用场景:**
```python
# OpenClaw 中
result = adapter.start_background_review(context)
await sessions_yield({
    message: result['message'],
    followUp: {
        'task_id': result['task_id'],
        'context': context
    }
})
```

---

#### check_status()

检查任务状态

```python
status = adapter.check_status(task_id='review_001')
```

**参数:**
- `task_id` (str): 任务 ID

**返回:**
```python
{
    'task_id': str,
    'status': str,  # 'running' | 'completed' | 'failed' | 'timeout'
    'progress': int  # 0-100
}
```

---

#### get_result()

获取任务结果

```python
result = adapter.get_result(task_id='review_001')
```

**参数:**
- `task_id` (str): 任务 ID

**返回:**
- `dict`: 任务结果，如果未完成则返回 `None`

---

### 3. NotificationManager

**文件:** `notification_manager.py`

**类:** `NotificationManager`

#### 初始化

```python
from notification_manager import NotificationManager

notifier = NotificationManager(workspace_dir=None)
```

---

#### send_completion_notification()

发送完成通知

```python
result = notifier.send_completion_notification(
    task_id='review_001',
    result={
        'success': True,
        'date': '2026-03-14',
        'tasks_completed': 9,
        'summary': '今日完成 9 个任务'
    },
    notification_type='all'  # 'all' | 'console' | 'system' | 'file'
)
```

**参数:**
- `task_id` (str): 任务 ID
- `result` (dict): 任务结果
- `notification_type` (str): 通知类型

**返回:**
```python
{
    'success': bool,
    'task_id': str,
    'notifications_sent': [
        {
            'type': str,
            'success': bool
        }
    ],
    'timestamp': str
}
```

---

#### send_timeout_warning()

发送超时警告

```python
result = notifier.send_timeout_warning(
    task_id='review_001',
    timeout_seconds=300
)
```

**参数:**
- `task_id` (str): 任务 ID
- `timeout_seconds` (int): 超时时间 (秒)

**返回:**
```python
{
    'success': bool,
    'message': str
}
```

---

#### send_error_notification()

发送错误通知

```python
result = notifier.send_error_notification(
    task_id='review_001',
    error='错误信息',
    fallback_mode=True
)
```

**参数:**
- `task_id` (str): 任务 ID
- `error` (str): 错误信息
- `fallback_mode` (bool): 是否降级模式

**返回:**
```python
{
    'success': bool,
    'message': str
}
```

---

#### list_unread_notifications()

列出未读通知

```python
unread = notifier.list_unread_notifications()
```

**返回:**
```python
[
    {
        'task_id': str,
        'type': str,
        'timestamp': str,
        'result': dict,
        'read': bool
    }
]
```

---

#### mark_as_read()

标记为已读

```python
success = notifier.mark_as_read(task_id='review_001')
```

**参数:**
- `task_id` (str): 任务 ID

**返回:**
- `bool`: 是否成功

---

### 4. ErrorHandler

**文件:** `error_handler.py`

**类:** `ErrorHandler`

#### 初始化

```python
from error_handler import ErrorHandler

handler = ErrorHandler(max_retries=3, retry_delay=1.0)
```

**参数:**
- `max_retries` (int): 最大重试次数
- `retry_delay` (float): 重试延迟 (秒)

---

#### retry_on_error()

带重试的错误处理

```python
result = handler.retry_on_error(
    func,
    *args,
    fallback_func=None,
    error_types=(Exception,),
    **kwargs
)
```

**参数:**
- `func` (callable): 要执行的函数
- `*args`: 函数参数
- `fallback_func` (callable): 降级函数
- `error_types` (tuple): 错误类型
- `**kwargs`: 函数关键字参数

**返回:**
```python
{
    'success': bool,
    'result': any,
    'attempts': int,
    'error': str or None,
    'fallback_used': bool
}
```

**使用示例:**
```python
def risky_func():
    # 可能失败的函数
    pass

def safe_fallback():
    # 降级函数
    pass

result = handler.retry_on_error(
    risky_func,
    fallback_func=safe_fallback
)
```

---

#### safe_execute()

安全执行 (不抛出异常)

```python
result = handler.safe_execute(
    func,
    *args,
    default_value=None,
    **kwargs
)
```

**参数:**
- `func` (callable): 要执行的函数
- `*args`: 函数参数
- `default_value` (any): 失败时的默认值
- `**kwargs`: 函数关键字参数

**返回:**
- 函数结果或默认值

---

### 5. FallbackMechanism

**文件:** `error_handler.py`

**类:** `FallbackMechanism`

#### 初始化

```python
from error_handler import FallbackMechanism

fallback = FallbackMechanism()
```

---

#### add_fallback()

添加降级函数

```python
fallback.add_fallback(func1)
        .add_fallback(func2)
        .add_fallback(func3)
```

**参数:**
- `func` (callable): 降级函数

**返回:**
- `self` (支持链式调用)

---

#### execute_with_fallback()

执行主函数，失败时依次尝试降级

```python
result = fallback.execute_with_fallback(
    primary_func,
    *args,
    **kwargs
)
```

**参数:**
- `primary_func` (callable): 主函数
- `*args`: 函数参数
- `**kwargs`: 函数关键字参数

**返回:**
```python
{
    'success': bool,
    'result': any,
    'method': str  # 'primary' or fallback function name
}
```

---

### 6. OpenClawReviewTool

**文件:** `openclaw_integration.py`

**类:** `OpenClawReviewTool`

#### 初始化

```python
from openclaw_integration import OpenClawReviewTool

tool = OpenClawReviewTool()
```

---

#### daily_review()

每日复盘

```python
result = tool.daily_review(
    context=None,
    async_mode=True
)
```

**参数:**
- `context` (dict): 复盘上下文
- `async_mode` (bool): 是否异步执行

**返回:**
```python
{
    'yield': bool,
    'message': str,
    'followUp': dict,
    'immediate_response': dict
}
```

**OpenClaw 使用:**
```python
result = tool.daily_review(async_mode=True)
await sessions_yield(result)
```

---

#### handle_followUp()

处理跟进任务

```python
result = tool.handle_followUp(followUp_data={
    'task_id': 'review_001',
    'context': {...}
})
```

**参数:**
- `followUp_data` (dict): 跟进数据

**返回:**
```python
{
    'type': 'completion_notification',
    'task_id': str,
    'message': str,
    'summary': str
}
```

---

## 💡 使用示例

### 示例 1: 基本异步复盘

```python
from sessions_yield_adapter import SessionsYieldAdapter

adapter = SessionsYieldAdapter()
result = adapter.start_background_review({
    'tasks_completed': 9,
    'skills_installed': 7
})

print(f"任务已启动：{result['task_id']}")
print(f"消息：{result['message']}")
```

---

### 示例 2: 完整复盘流程

```python
from review_background_agent import ReviewBackgroundAgent

agent = ReviewBackgroundAgent()
result = agent.execute_review({
    'tasks_completed': 10,
    'skills_installed': 8,
    'value': 0.95
})

print(f"日期：{result['date']}")
print(f"任务：{result['tasks_completed']} 个")
print(f"技能：{result['skills_installed']} 个")
print(f"报告：{result['report_path']}")
```

---

### 示例 3: 错误处理

```python
from error_handler import ErrorHandler

handler = ErrorHandler(max_retries=3)

def risky_operation():
    # 可能失败的操作
    pass

def fallback():
    # 降级方案
    pass

result = handler.retry_on_error(
    risky_operation,
    fallback_func=fallback
)

if result['success']:
    print(f"成功！尝试次数：{result['attempts']}")
else:
    print(f"失败：{result['error']}")
```

---

### 示例 4: 降级链

```python
from error_handler import FallbackMechanism

fallback = FallbackMechanism()
fallback.add_fallback(lambda: "降级 1")
        .add_fallback(lambda: "降级 2")
        .add_fallback(lambda: "降级 3")

result = fallback.execute_with_fallback(primary_func)
print(f"使用方法：{result['method']}")
```

---

### 示例 5: 通知管理

```python
from notification_manager import NotificationManager

notifier = NotificationManager()

# 发送完成通知
result = notifier.send_completion_notification(
    task_id='review_001',
    result={
        'success': True,
        'date': '2026-03-14',
        'tasks_completed': 9
    },
    notification_type='all'
)

# 查看未读通知
unread = notifier.list_unread_notifications()
print(f"未读通知：{len(unread)} 个")

# 标记为已读
notifier.mark_as_read('review_001')
```

---

### 示例 6: OpenClaw 集成

```python
from openclaw_integration import OpenClawReviewTool

tool = OpenClawReviewTool()

# 异步复盘
result = tool.daily_review(
    context={'tasks_completed': 9},
    async_mode=True
)

# 在 OpenClaw 中
await sessions_yield({
    message: result['message'],
    followUp: result['followUp']
})
```

---

## ⚠️ 错误处理

### 常见错误

#### 1. JSON 序列化错误

**错误:**
```
TypeError: Object of type bool is not JSON serializable
```

**解决:**
```python
# 显式转换
'reflection_triggered': bool(value)
'tasks_completed': int(value)
```

---

#### 2. 经验文件损坏

**错误:**
```
[Storage] 加载经验失败：Expecting value: line 144
```

**解决:**
- 删除损坏的经验文件
- 系统会自动重新创建

---

#### 3. 后台进程启动失败

**错误:**
```
[YieldAdapter] 启动失败：...
```

**解决:**
- 系统自动降级到同步模式
- 检查 Python 环境
- 检查文件权限

---

### 错误代码

| 代码 | 说明 | 处理 |
|------|------|------|
| `ERR_STORAGE_LOAD` | 存储加载失败 | 自动重建 |
| `ERR_JSON_SERIALIZE` | JSON 序列化失败 | 显式转换 |
| `ERR_PROCESS_START` | 进程启动失败 | 降级同步 |
| `ERR_TIMEOUT` | 超时 | 发送警告 |
| `ERR_NOTIFICATION` | 通知失败 | 降级控制台 |

---

## 🌟 最佳实践

### 1. 选择合适的模式

**异步模式:**
- ✅ 日常复盘
- ✅ 长时间任务
- ✅ 多任务并行

**同步模式:**
- ✅ 需要立即结果
- ✅ 调试和测试
- ✅ 简单任务

---

### 2. 错误处理

```python
# 推荐做法
handler = ErrorHandler(max_retries=3)
result = handler.retry_on_error(
    func,
    fallback_func=fallback
)

# 不推荐
try:
    result = func()
except:
    pass  # 忽略错误
```

---

### 3. 资源管理

```python
# 推荐：使用上下文管理器
with ReviewBackgroundAgent() as agent:
    result = agent.execute_review(context)

# 不推荐：忘记清理
agent = ReviewBackgroundAgent()
result = agent.execute_review(context)
# agent 未释放
```

---

### 4. 日志记录

```python
# 推荐：详细日志
import logging
logging.basicConfig(level=logging.INFO)

# 不推荐：无日志
# 无法追踪问题
```

---

## 📊 性能建议

### 1. 并发控制

```python
# 推荐：限制并发数
MAX_CONCURRENT = 5
current_tasks = 0

if current_tasks < MAX_CONCURRENT:
    start_task()

# 不推荐：无限制并发
start_task()  # 可能耗尽资源
```

---

### 2. 超时设置

```python
# 推荐：设置超时
result = adapter.start_background_review(
    context,
    timeout=300  # 5 分钟
)

# 不推荐：无超时
result = adapter.start_background_review(context)
# 可能永远等待
```

---

### 3. 缓存使用

```python
# 推荐：缓存结果
@cache
def get_review_data(date):
    return load_from_file(date)

# 不推荐：重复加载
data = load_from_file(date)
data = load_from_file(date)  # 重复 IO
```

---

## 🎯 完整示例

### OpenClaw 复盘机器人

```python
from openclaw_integration import OpenClawReviewTool

class ReviewBot:
    def __init__(self):
        self.tool = OpenClawReviewTool()
    
    async def handle_review_command(self, context):
        """处理复盘命令"""
        
        # 启动异步复盘
        result = self.tool.daily_review(
            context=context,
            async_mode=True
        )
        
        # 使用 sessions_yield
        await sessions_yield({
            message: result['message'],
            followUp: result['followUp']
        })
    
    async def handle_followUp(self, followUp_data):
        """处理跟进"""
        
        result = self.tool.handle_followUp(followUp_data)
        
        # 发送完成通知
        await send_message(result['message'])
        await send_message(result['summary'])

# 使用
bot = ReviewBot()
await bot.handle_review_command({'tasks_completed': 9})
```

---

## 📝 总结

### 核心 API

| 模块 | 主要功能 | 关键方法 |
|------|----------|----------|
| `ReviewBackgroundAgent` | 后台复盘 | `execute_review()` |
| `SessionsYieldAdapter` | 异步执行 | `start_background_review()` |
| `NotificationManager` | 通知管理 | `send_completion_notification()` |
| `ErrorHandler` | 错误处理 | `retry_on_error()` |
| `FallbackMechanism` | 降级链 | `execute_with_fallback()` |
| `OpenClawReviewTool` | OpenClaw 集成 | `daily_review()` |

---

### 快速参考

```python
# 1. 异步复盘
adapter.start_background_review(context)

# 2. 同步复盘
agent.execute_review(context)

# 3. 错误处理
handler.retry_on_error(func, fallback)

# 4. 通知
notifier.send_completion_notification(...)

# 5. OpenClaw
await sessions_yield(result)
```

---

*API 版本：1.0*  
*最后更新：2026-03-14*

