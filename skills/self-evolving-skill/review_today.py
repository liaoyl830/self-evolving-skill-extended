#!/usr/bin/env python3
"""
浠婃棩澶嶇洏璁板綍
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from skill_engine import SelfEvolvingSkillEngine

# 鍒濆鍖栧紩鎿?engine = SelfEvolvingSkillEngine()

# 鎵ц澶嶇洏鎶€鑳?result = engine.execute(
    skill_id='skill_1773417052936',  # TestSkill
    context={
        'task': 'daily_review',
        'date': '2026-03-13',
        'tasks_completed': 14,
        'skills_installed': 7,
        'configurations_done': 8
    },
    embedding=[0.1] * 128,
    success=True,
    value=0.95
)

print(f"澶嶇洏璁板綍瀹屾垚:")
print(f"  鎵ц锛歿result.executed}")
print(f"  鍙嶆€濊Е鍙戯細{result.reflection_triggered}")

# 鑾峰彇缁熻
stats = engine.get_stats()
print(f"\n绯荤粺缁熻:")
print(f"  鎶€鑳芥暟锛歿stats['skills_count']}")
print(f"  缁忛獙鏁帮細{stats['experiences_count']}")
print(f"  鎬绘墽琛岋細{stats['engine']['total_executions']}")
