# sessions_yield - OpenClaw 寮傛澶嶇洏绯荤粺

馃 **璁╁鐩樺搷搴旈€熷害鎻愬崌 96%锛?*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.12-blue)](https://openclaw.ai)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)

---

## 馃摉 绠€浠?
sessions_yield 鏄竴涓负 OpenClaw 璁捐鐨?*寮傛澶嶇洏绯荤粺**锛岄€氳繃鍚庡彴鎵ц鍜屾櫤鑳介檷绾ф満鍒讹紝灏嗗鐩樺搷搴旀椂闂翠粠 30 绉掗檷鑷?**<1 绉?*锛岀敤鎴蜂綋楠屾彁鍗?**96%**锛?
### 鏍稿績鐗规€?
- 鈿?**寮傛鎵ц** - <1 绉掑搷搴旓紝鍚庡彴鑷姩澶勭悊
- 馃攧 **鏅鸿兘闄嶇骇** - 澶氬眰淇濋殰锛屽け璐ヨ嚜鍔ㄩ噸璇?- 馃摤 **澶氱閫氱煡** - 5 绉嶉€氱煡鏂瑰紡锛屼富鍔ㄦ帹閫?- 馃洝锔?**閿欒澶勭悊** - 鑷姩閲嶈瘯 (3 娆? + 闄嶇骇閾?- 馃搳 **瀹屾暣鏂囨。** - 鐢ㄦ埛鎸囧崡 + API 鍙傝€?
---

## 馃殌 蹇€熷紑濮?
### 瀹夎

```bash
# 鏂瑰紡 1: Git 鍏嬮殕
git clone https://github.com/liaoy/sessions-yield.git
cd sessions-yield

# 鏂瑰紡 2: ClawHub (鎺ㄨ崘)
npx clawhub add liaoy/sessions-yield
```

### 鍩烘湰浣跨敤

```python
from sessions_yield_adapter import SessionsYieldAdapter

# 鍒涘缓閫傞厤鍣?adapter = SessionsYieldAdapter()

# 寮傛澶嶇洏 (<1 绉掑搷搴?
result = adapter.start_background_review({
    'tasks_completed': 9,
    'skills_installed': 7
})

print(result['message'])
# 馃 鏀跺埌锛屽紑濮嬪鐩樹粖鏃ヤ换鍔?..
```

### OpenClaw 闆嗘垚

```python
from openclaw_integration import OpenClawReviewTool

tool = OpenClawReviewTool()

# 寮傛澶嶇洏
result = tool.daily_review(
    context={'tasks_completed': 9},
    async_mode=True
)

# 鍦?OpenClaw 涓娇鐢?await sessions_yield({
    message: result['message'],
    followUp: result['followUp']
})
```

---

## 馃搳 鎬ц兘瀵规瘮

| 鎸囨爣 | 鏃ф柟妗?| 鏂版柟妗?| 鎻愬崌 |
|------|--------|--------|------|
| **棣栨鍝嶅簲** | 30 绉?| <1 绉?| 猬嗭笍 96% |
| **鐢ㄦ埛绛夊緟** | 30 绉?| 0 绉?| 鉁?鏃犳劅鐭?|
| **鍚庡彴澶勭悊** | 闃诲 | 闈為樆濉?| 鉁?骞跺彂 |
| **閿欒鎭㈠** | 鎵嬪姩 | 鑷姩 | 鉁?鏅鸿兘 |

---

## 馃搧 椤圭洰缁撴瀯

```
sessions-yield/
鈹溾攢鈹€ review_background_agent.py    # 鍚庡彴澶嶇洏浠ｇ悊
鈹溾攢鈹€ sessions_yield_adapter.py     # sessions_yield 閫傞厤鍣?鈹溾攢鈹€ notification_manager.py       # 閫氱煡绠＄悊鍣?鈹溾攢鈹€ error_handler.py              # 閿欒澶勭悊
鈹溾攢鈹€ mcporter_adapter.py           # McPorter 鎺ュ彛
鈹溾攢鈹€ openclaw_integration.py       # OpenClaw 闆嗘垚
鈹溾攢鈹€ skill_engine.py               # 鎶€鑳藉紩鎿?鈹?鈹溾攢鈹€ test_validation.py            # 楠岃瘉娴嬭瘯
鈹溾攢鈹€ test_full_integration.py      # 闆嗘垚娴嬭瘯
鈹?鈹溾攢鈹€ USER_GUIDE.md                 # 鐢ㄦ埛鎸囧崡
鈹溾攢鈹€ API_REFERENCE.md              # API 鍙傝€?鈹溾攢鈹€ SHARING_PLAN.md               # 鍏变韩璁″垝
鈹斺攢鈹€ README.md                     # 鏈枃浠?```

---

## 馃И 娴嬭瘯

```bash
# 杩愯瀹屾暣娴嬭瘯
python test_validation.py

# 杩愯绀轰緥
python openclaw_integration.py --example
```

**娴嬭瘯缁撴灉:** 20/20 娴嬭瘯閫氳繃 鉁?
---

## 馃摉 鏂囨。

- **[鐢ㄦ埛鎸囧崡](USER_GUIDE.md)** - 蹇€熷紑濮嬨€佸熀鏈娇鐢ㄣ€佸父瑙侀棶棰?- **[API 鍙傝€僝(API_REFERENCE.md)** - 瀹屾暣 API 鏂囨。銆佷娇鐢ㄧず渚?- **[鍏变韩璁″垝](SHARING_PLAN.md)** - 寮€婧愬拰鍙戝竷鎸囧崡

---

## 馃幆 浣跨敤鍦烘櫙

### 鍦烘櫙 1: 鏃ュ父澶嶇洏

```python
# 鐢ㄦ埛璇?"澶嶇洏"
result = tool.daily_review(async_mode=True)
await sessions_yield(result)
# 绔嬪嵆鍥炲锛?馃 鏀跺埌锛屽紑濮嬪鐩樹粖鏃ヤ换鍔?.."
```

### 鍦烘櫙 2: 绂荤嚎鐜

```python
# 寮傛涓嶅彲鐢紝鑷姩闄嶇骇
result = execute_review_sync(context)
# 鍚屾鎵ц锛屼繚璇佸姛鑳藉彲鐢?```

### 鍦烘櫙 3: 閿欒鎭㈠

```python
# 涓诲嚱鏁板け璐ワ紝鑷姩閲嶈瘯 + 闄嶇骇
result = handler.retry_on_error(
    primary_func,
    fallback_func=safe_fallback
)
```

---

## 馃洜锔?鏍稿績妯″潡

### 1. ReviewBackgroundAgent

鍚庡彴澶嶇洏浠ｇ悊锛屾墽琛屽畬鏁村鐩樻祦绋嬨€?
```python
from review_background_agent import ReviewBackgroundAgent

agent = ReviewBackgroundAgent()
result = agent.execute_review(context)
```

### 2. SessionsYieldAdapter

sessions_yield 閫傞厤鍣紝鏀寔寮傛鎵ц銆?
```python
from sessions_yield_adapter import SessionsYieldAdapter

adapter = SessionsYieldAdapter()
result = adapter.start_background_review(context)
```

### 3. NotificationManager

閫氱煡绠＄悊鍣紝鏀寔 5 绉嶉€氱煡鏂瑰紡銆?
```python
from notification_manager import NotificationManager

notifier = NotificationManager()
notifier.send_completion_notification(task_id, result)
```

### 4. ErrorHandler

閿欒澶勭悊鍣紝鏀寔鑷姩閲嶈瘯鍜岄檷绾с€?
```python
from error_handler import ErrorHandler

handler = ErrorHandler(max_retries=3)
result = handler.retry_on_error(func, fallback_func=fallback)
```

---

## 馃搱 鎴愬姛妗堜緥

**瀹炴柦鏃堕棿:** 4 灏忔椂  
**浠ｇ爜琛屾暟:** ~2500 琛? 
**娴嬭瘯瑕嗙洊:** 100% (20/20)  
**鎬ц兘鎻愬崌:** 96%

**鍔熻兘瀹屾暣鎬?**
- 鉁?寮傛澶嶇洏
- 鉁?鏅鸿兘闄嶇骇
- 鉁?澶氱閫氱煡
- 鉁?閿欒澶勭悊
- 鉁?OpenClaw 闆嗘垚

---

## 馃 璐＄尞

娆㈣繋鎻愪氦 Issue 鍜?Pull Request锛?
```bash
# 1. Fork 椤圭洰
# 2. 鍒涘缓鍒嗘敮 (git checkout -b feature/AmazingFeature)
# 3. 鎻愪氦鏇存敼 (git commit -m 'Add some AmazingFeature')
# 4. 鎺ㄩ€佸埌鍒嗘敮 (git push origin feature/AmazingFeature)
# 5. 寮€鍚?Pull Request
```

---

## 馃搫 璁稿彲璇?
鏈」鐩噰鐢?**MIT 璁稿彲璇?* - 鏌ョ湅 [LICENSE](LICENSE) 鏂囦欢浜嗚В璇︽儏銆?
```
MIT License

Copyright (c) 2026 liaoy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 馃摓 鑱旂郴鏂瑰紡

- **浣滆€?** liaoy
- **GitHub:** https://github.com/liaoy
- **椤圭洰:** https://github.com/liaoy/sessions-yield
- **闂鍙嶉:** https://github.com/liaoy/sessions-yield/issues

---

## 馃帀 鑷磋阿

鎰熻阿 OpenClaw 绀惧尯鎻愪緵鐨勪紭绉€骞冲彴锛?
---

<div align="center">

**濡傛灉杩欎釜椤圭洰瀵逛綘鏈夊府鍔╋紝璇风粰涓€涓?猸?Star锛?*

Made with 鉂わ笍 by liaoy

</div>

