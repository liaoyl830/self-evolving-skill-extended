#!/usr/bin/env python3
"""
娴嬭瘯寮傛澶嶇洏
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from mcporter_adapter import skill_review_sync, skill_review_async

print("="*60)
print("娴嬭瘯澶嶇洏鍔熻兘")
print("="*60)

# 娴嬭瘯鍚屾澶嶇洏
print("\n[1] 娴嬭瘯鍚屾澶嶇洏...")
result = skill_review_sync({
    'context': {
        'tasks_completed': 9,
        'skills_installed': 7,
        'value': 0.95
    }
})

print(f"缁撴灉锛歿result}")

# 娴嬭瘯寮傛澶嶇洏
print("\n[2] 娴嬭瘯寮傛澶嶇洏...")
result = skill_review_async({
    'context': {
        'tasks_completed': 9,
        'skills_installed': 7
    }
})

print(f"缁撴灉锛歿result}")

print("\n" + "="*60)
print("娴嬭瘯瀹屾垚")
print("="*60)
