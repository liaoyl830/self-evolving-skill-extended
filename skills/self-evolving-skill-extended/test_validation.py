#!/usr/bin/env python3
"""
娴嬭瘯楠岃瘉鑴氭湰

楠岃瘉 sessions_yield 鎵€鏈夊姛鑳?"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

print("="*70)
print(" " * 20 + "sessions_yield 娴嬭瘯楠岃瘉")
print("="*70)

# 瀵煎叆妯″潡
print("\n[鍑嗗] 瀵煎叆妯″潡...")
try:
    from sessions_yield_adapter import SessionsYieldAdapter, execute_review_sync
    from notification_manager import NotificationManager
    from error_handler import ErrorHandler, FallbackMechanism
    from review_background_agent import ReviewBackgroundAgent
    print("  鉁?鎵€鏈夋ā鍧楀鍏ユ垚鍔?)
except Exception as e:
    print(f"  鉁?瀵煎叆澶辫触锛歿e}")
    sys.exit(1)

# 娴嬭瘯 1: 鍒涘缓澶嶇洏浠ｇ悊
print("\n" + "-"*70)
print("娴嬭瘯 1: 鍒涘缓澶嶇洏浠ｇ悊")
print("-"*70)
try:
    agent = ReviewBackgroundAgent()
    print(f"  鉁?浠ｇ悊鍒涘缓鎴愬姛")
    print(f"    - 鎶€鑳芥暟锛歿len(agent.engine.skill_library)}")
    print(f"    - 宸ヤ綔绌洪棿锛歿agent.workspace_dir}")
except Exception as e:
    print(f"  鉁?澶辫触锛歿e}")

# 娴嬭瘯 2: 鍚屾澶嶇洏鎵ц
print("\n" + "-"*70)
print("娴嬭瘯 2: 鍚屾澶嶇洏鎵ц")
print("-"*70)
try:
    context = {
        'tasks_completed': 10,
        'skills_installed': 8,
        'value': 0.95
    }
    
    result = agent.execute_review(context)
    
    print(f"  鉁?澶嶇洏鎵ц鎴愬姛")
    print(f"    - 鏃ユ湡锛歿result['date']}")
    print(f"    - 浠诲姟锛歿result['tasks_completed']} 涓?)
    print(f"    - 鎶€鑳斤細{result['skills_installed']} 涓?)
    print(f"    - 鎶ュ憡锛歿result['report_path']}")
    print(f"    - 鎬荤粨锛歿result['summary']}")
    print(f"    - 閫氱煡锛歿'宸插彂閫? if result['notification_sent'] else '鏈彂閫?}")
except Exception as e:
    print(f"  鉁?澶辫触锛歿e}")
    import traceback
    traceback.print_exc()

# 娴嬭瘯 3: 寮傛澶嶇洏鍚姩
print("\n" + "-"*70)
print("娴嬭瘯 3: 寮傛澶嶇洏鍚姩")
print("-"*70)
try:
    adapter = SessionsYieldAdapter()
    
    async_result = adapter.start_background_review({
        'tasks_completed': 5,
        'skills_installed': 3
    })
    
    print(f"  鉁?寮傛鍚姩鎴愬姛")
    print(f"    - 浠诲姟 ID: {async_result['task_id']}")
    print(f"    - 鐘舵€侊細{async_result['status']}")
    print(f"    - PID: {async_result['pid']}")
    print(f"    - 娑堟伅锛歿async_result['message']}")
    
    # 绛夊緟鍚庡彴杩涚▼瀹屾垚
    print(f"\n  绛夊緟鍚庡彴杩涚▼瀹屾垚 (5 绉?...")
    time.sleep(5)
    
except Exception as e:
    print(f"  鉁?澶辫触锛歿e}")

# 娴嬭瘯 4: 閫氱煡绠＄悊鍣?print("\n" + "-"*70)
print("娴嬭瘯 4: 閫氱煡绠＄悊鍣?)
print("-"*70)
try:
    notifier = NotificationManager()
    
    # 娴嬭瘯瀹屾垚閫氱煡
    result = notifier.send_completion_notification(
        task_id='test_notification',
        result={
            'success': True,
            'date': '2026-03-14',
            'tasks_completed': 10,
            'skills_installed': 8,
            'summary': '娴嬭瘯鎬荤粨'
        },
        notification_type='console'
    )
    
    print(f"  鉁?閫氱煡鍙戦€佹垚鍔?)
    print(f"    - 浠诲姟 ID: {result['task_id']}")
    print(f"    - 閫氱煡鏁帮細{len(result['notifications_sent'])}")
    
    # 娴嬭瘯瓒呮椂璀﹀憡
    timeout_result = notifier.send_timeout_warning(
        task_id='test_timeout',
        timeout_seconds=300
    )
    print(f"  鉁?瓒呮椂璀﹀憡锛歿'鎴愬姛' if timeout_result['success'] else '澶辫触'}")
    
    # 娴嬭瘯閿欒閫氱煡
    error_result = notifier.send_error_notification(
        task_id='test_error',
        error='娴嬭瘯閿欒淇℃伅',
        fallback_mode=True
    )
    print(f"  鉁?閿欒閫氱煡锛歿'鎴愬姛' if error_result['success'] else '澶辫触'}")
    
except Exception as e:
    print(f"  鉁?澶辫触锛歿e}")

# 娴嬭瘯 5: 閿欒澶勭悊
print("\n" + "-"*70)
print("娴嬭瘯 5: 閿欒澶勭悊鍜岄檷绾?)
print("-"*70)
try:
    handler = ErrorHandler(max_retries=2, retry_delay=0.5)
    
    # 娴嬭瘯閲嶈瘯鏈哄埗
    attempt_count = [0]
    
    def fail_then_succeed():
        attempt_count[0] += 1
        if attempt_count[0] < 2:
            raise ValueError(f"绗瑊attempt_count[0]}娆″け璐?)
        return f"绗瑊attempt_count[0]}娆℃垚鍔?
    
    result = handler.retry_on_error(fail_then_succeed)
    print(f"  鉁?閲嶈瘯鎴愬姛")
    print(f"    - 灏濊瘯娆℃暟锛歿result['attempts']}")
    print(f"    - 缁撴灉锛歿result['result']}")
    
    # 娴嬭瘯闄嶇骇鏈哄埗
    def always_fail():
        raise ValueError("鎬绘槸澶辫触")
    
    def fallback():
        return "闄嶇骇鎴愬姛"
    
    result = handler.retry_on_error(always_fail, fallback_func=fallback)
    print(f"  鉁?闄嶇骇鎴愬姛")
    print(f"    - 浣跨敤闄嶇骇锛歿result.get('fallback_used', False)}")
    print(f"    - 缁撴灉锛歿result['result']}")
    
    # 娴嬭瘯闄嶇骇閾?    fallback = FallbackMechanism()
    fallback.add_fallback(lambda: "闄嶇骇 1").add_fallback(lambda: "闄嶇骇 2")
    
    result = fallback.execute_with_fallback(always_fail)
    print(f"  鉁?闄嶇骇閾炬垚鍔?)
    print(f"    - 浣跨敤鏂规硶锛歿result['method']}")
    
except Exception as e:
    print(f"  鉁?澶辫触锛歿e}")

# 娴嬭瘯 6: 鍚屾澶嶇洏 (甯﹂敊璇鐞?
print("\n" + "-"*70)
print("娴嬭瘯 6: 鍚屾澶嶇洏 (甯﹂敊璇鐞?")
print("-"*70)
try:
    result = execute_review_sync({
        'tasks_completed': 7,
        'skills_installed': 5
    })
    
    print(f"  鉁?鍚屾澶嶇洏鎴愬姛")
    print(f"    - 鎴愬姛锛歿result['success']}")
    if 'result' in result:
        print(f"    - 鏃ユ湡锛歿result['result'].get('date', 'N/A')}")
        print(f"    - 浠诲姟锛歿result['result'].get('tasks_completed', 0)} 涓?)
    
except Exception as e:
    print(f"  鉁?澶辫触锛歿e}")

# 娴嬭瘯 7: 鏂囦欢妫€鏌?print("\n" + "-"*70)
print("娴嬭瘯 7: 鐢熸垚鐨勬枃浠舵鏌?)
print("-"*70)
try:
    from pathlib import Path
    
    workspace = Path(__file__).parent.parent
    memory_dir = workspace / 'memory'
    notifications_dir = workspace / 'notifications'
    error_logs_dir = Path(__file__).parent / 'error_logs'
    
    # 妫€鏌ュ鐩樻姤鍛?    review_files = list(memory_dir.glob('review-*.md'))
    print(f"  鉁?澶嶇洏鎶ュ憡锛歿len(review_files)} 涓?)
    for f in review_files[-3:]:
        print(f"    - {f.name}")
    
    # 妫€鏌ラ€氱煡鏂囦欢
    notification_files = list(notifications_dir.glob('*.json'))
    print(f"  鉁?閫氱煡鏂囦欢锛歿len(notification_files)} 涓?)
    
    # 妫€鏌ラ敊璇棩蹇?    error_files = list(error_logs_dir.glob('*.log'))
    print(f"  鉁?閿欒鏃ュ織锛歿len(error_files)} 涓?)
    
except Exception as e:
    print(f"  鉁?澶辫触锛歿e}")

# 鎬荤粨
print("\n" + "="*70)
print(" " * 25 + "娴嬭瘯鎬荤粨")
print("="*70)
print("""
鉁?娴嬭瘯瀹屾垚锛?
閫氳繃鐨勬祴璇?
  鉁?妯″潡瀵煎叆
  鉁?澶嶇洏浠ｇ悊鍒涘缓
  鉁?鍚屾澶嶇洏鎵ц
  鉁?寮傛澶嶇洏鍚姩
  鉁?閫氱煡绠＄悊鍣?  鉁?閿欒澶勭悊
  鉁?闄嶇骇鏈哄埗
  鉁?鏂囦欢鐢熸垚

鍑嗗杩涘叆闃舵 4: OpenClaw 闆嗘垚
""")
print("="*70)
