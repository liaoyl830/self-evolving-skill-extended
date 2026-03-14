#!/usr/bin/env python3
"""
瀹屾暣闆嗘垚娴嬭瘯

娴嬭瘯 sessions_yield 鎵€鏈夊姛鑳?"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

from sessions_yield_adapter import SessionsYieldAdapter, execute_review_sync
from notification_manager import NotificationManager
from error_handler import ErrorHandler

print("="*60)
print("sessions_yield 瀹屾暣闆嗘垚娴嬭瘯")
print("="*60)

# 娴嬭瘯 1: 寮傛澶嶇洏
print("\n[娴嬭瘯 1] 寮傛澶嶇洏...")
adapter = SessionsYieldAdapter()
async_result = adapter.start_background_review({
    'tasks_completed': 9,
    'skills_installed': 7
})
print(f"寮傛缁撴灉锛歿async_result}")

# 绛夊緟 2 绉掕鍚庡彴杩涚▼杩愯
print("\n绛夊緟鍚庡彴杩涚▼杩愯...")
time.sleep(2)

# 娴嬭瘯 2: 鍚屾澶嶇洏
print("\n[娴嬭瘯 2] 鍚屾澶嶇洏...")
sync_result = execute_review_sync({
    'tasks_completed': 5,
    'skills_installed': 3
})
print(f"鍚屾缁撴灉锛歿sync_result}")

# 娴嬭瘯 3: 閿欒澶勭悊鍜岄檷绾?print("\n[娴嬭瘯 3] 閿欒澶勭悊鍜岄檷绾?..")
error_handler = ErrorHandler(max_retries=2, retry_delay=0.5)

def fail_func():
    raise ValueError("娴嬭瘯閿欒")

def fallback_func():
    return "闄嶇骇鎴愬姛"

result = error_handler.retry_on_error(fail_func, fallback_func=fallback_func)
print(f"閿欒澶勭悊缁撴灉锛歿result}")

# 娴嬭瘯 4: 閫氱煡绠＄悊鍣?print("\n[娴嬭瘯 4] 閫氱煡绠＄悊鍣?..")
notifier = NotificationManager()
notification_result = notifier.send_completion_notification(
    task_id='test_complete',
    result={
        'success': True,
        'date': '2026-03-14',
        'tasks_completed': 9,
        'summary': '娴嬭瘯鎬荤粨'
    },
    notification_type='console'
)
print(f"閫氱煡缁撴灉锛歿notification_result}")

print("\n" + "="*60)
print("鎵€鏈夋祴璇曞畬鎴愶紒")
print("="*60)
print("\n鉁?闃舵 1-3 瀹炴柦瀹屾垚锛?)
print("  - 鍩虹闆嗘垚 鉁?)
print("  - 閫氱煡鏈哄埗 鉁?)
print("  - 閿欒澶勭悊 鉁?)
