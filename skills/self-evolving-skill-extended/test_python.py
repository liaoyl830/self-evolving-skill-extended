#!/usr/bin/env python3
"""
瀹屾暣鍔熻兘娴嬭瘯
"""

import sys
import os

# 娣诲姞鏍稿績妯″潡璺緞
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from skill_engine import SelfEvolvingSkillEngine

print("=" * 50)
print("Self-Evolving Skill 瀹屾暣娴嬭瘯")
print("=" * 50)

# 鍒濆鍖栧紩鎿?print("\n1. 鍒濆鍖栧紩鎿?..")
engine = SelfEvolvingSkillEngine()

# 鍒涘缓鎶€鑳?print("\n2. 鍒涘缓鎶€鑳?..")
skill1 = engine.create_skill("PythonExpert", "Python 缂栫▼涓撳")
skill2 = engine.create_skill("DataAnalyzer", "鏁版嵁鍒嗘瀽涓撳")
print(f"   [OK] {skill1.id}: {skill1.name}")
print(f"   [OK] {skill2.id}: {skill2.name}")

# 鍒楀嚭鎶€鑳?print("\n3. 鍒楀嚭鎶€鑳?..")
skills = engine.list_skills()
for s in skills:
    print(f"   - {s.id}: {s.name} (鎵ц锛歿s.execution_count})")

# 鎵ц鎶€鑳?print("\n4. 鎵ц鎶€鑳?..")
result = engine.execute(
    skill_id=skill1.id,
    context={'task': 'code_review', 'language': 'python'},
    embedding=[0.1] * 128,
    success=True,
    value=0.85
)
print(f"   [OK] 鎵ц锛歿result.executed}")
print(f"   [OK] 鍙嶆€濊Е鍙戯細{result.reflection_triggered}")

# 鍒嗘瀽宓屽叆
print("\n5. 鍒嗘瀽宓屽叆...")
analysis = engine.analyze([0.2] * 128)
print(f"   [OK] 鎬昏兘閲忥細{analysis.total_energy:.2f}")
print(f"   [OK] 娈嬪樊姣旂巼锛歿analysis.residual_ratio:.2f}")
print(f"   [OK] 寤鸿鎶借薄锛歿analysis.suggested_abstraction}")
print(f"   [OK] 鏂伴鎬э細{analysis.novelty_score:.2f}")

# 绯荤粺缁熻
print("\n6. 绯荤粺缁熻...")
stats = engine.get_stats()
print(f"   [OK] 鎶€鑳芥暟锛歿stats['skills_count']}")
print(f"   [OK] 缁忛獙鏁帮細{stats['experiences_count']}")
print(f"   [OK] 鎬绘墽琛岋細{stats['engine']['total_executions']}")
print(f"   [OK] 瀛樺偍澶у皬锛歿stats['storage_size_mb']:.4f} MB")

# 淇濆瓨鎶€鑳?print("\n7. 淇濆瓨鎶€鑳?..")
saved = engine.save(skill1.id)
print(f"   [OK] 淇濆瓨锛歿saved}")

print("\n" + "=" * 50)
print("娴嬭瘯瀹屾垚锛?)
print("=" * 50)
