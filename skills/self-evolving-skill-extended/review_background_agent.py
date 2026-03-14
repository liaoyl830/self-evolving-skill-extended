#!/usr/bin/env python3
"""
澶嶇洏鍚庡彴浠ｇ悊

浣跨敤 sessions_yield 瀹炵幇寮傛澶嶇洏娴佺▼
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# 娣诲姞鏍稿績妯″潡璺緞
CORE_DIR = Path(__file__).parent / 'core'
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from skill_engine import SelfEvolvingSkillEngine
from notification_manager import NotificationManager


class ReviewBackgroundAgent:
    """澶嶇洏鍚庡彴浠ｇ悊"""
    
    def __init__(self, storage_dir: Optional[str] = None):
        """
        鍒濆鍖栧鐩樹唬鐞?        
        Args:
            storage_dir: 瀛樺偍鐩綍
        """
        self.engine = SelfEvolvingSkillEngine(storage_dir=storage_dir)
        self.workspace_dir = Path(__file__).parent.parent
        self.memory_dir = self.workspace_dir / 'memory'
        self.notification_manager = NotificationManager(self.workspace_dir)
        
        # 纭繚鐩綍瀛樺湪
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"[ReviewAgent] 鍒濆鍖栧畬鎴?)
        print(f"[ReviewAgent] 宸ヤ綔绌洪棿锛歿self.workspace_dir}")
        print(f"[ReviewAgent] 宸插姞杞?{len(self.engine.skill_library)} 涓妧鑳?)
    
    def execute_review(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        鎵ц澶嶇洏
        
        Args:
            context: 澶嶇洏涓婁笅鏂?            
        Returns:
            澶嶇洏缁撴灉
        """
        print(f"\n{'='*50}")
        print(f"寮€濮嬪鐩樻祦绋?)
        print(f"{'='*50}\n")
        
        # 1. 鎵ц鎶€鑳?        print("[1/5] 鎵ц鎶€鑳借褰?..")
        skill_id = context.get('skill_id', list(self.engine.skill_library.keys())[0])
        
        result = self.engine.execute(
            skill_id=skill_id,
            context=context,
            embedding=[0.1] * 128,
            success=True,
            value=context.get('value', 0.95)
        )
        
        print(f"  鉁?鎶€鑳芥墽琛岋細{'鎴愬姛' if result.success else '澶辫触'}")
        print(f"  鉁?鍙嶆€濊Е鍙戯細{result.reflection_triggered}\n")
        
        # 2. 鏀堕泦浠婃棩鏁版嵁
        print("[2/5] 鏀堕泦浠婃棩鏁版嵁...")
        today = datetime.now().strftime('%Y-%m-%d')
        tasks_completed = context.get('tasks_completed', 0)
        skills_installed = context.get('skills_installed', 0)
        
        print(f"  鉁?鏃ユ湡锛歿today}")
        print(f"  鉁?瀹屾垚浠诲姟锛歿tasks_completed} 涓?)
        print(f"  鉁?瀹夎鎶€鑳斤細{skills_installed} 涓猏n")
        
        # 3. 鐢熸垚澶嶇洏鎶ュ憡
        print("[3/5] 鐢熸垚澶嶇洏鎶ュ憡...")
        report = self._generate_report(context, result)
        print(f"  鉁?鎶ュ憡鐢熸垚瀹屾垚\n")
        
        # 4. 鍐欏叆鏂囦欢
        print("[4/5] 鍐欏叆璁板繂鏂囦欢...")
        report_path = self._write_review_file(today, report)
        print(f"  鉁?宸蹭繚瀛樺埌锛歿report_path}\n")
        
        # 5. 鏇存柊 MEMORY.md
        print("[5/5] 鏇存柊闀挎湡璁板繂...")
        self._update_memory_md(report)
        print(f"  鉁?MEMORY.md 宸叉洿鏂癨n")
        
        # 6. 鍙戦€佸畬鎴愰€氱煡
        print("[6/6] 鍙戦€佸畬鎴愰€氱煡...")
        notification_result = self.notification_manager.send_completion_notification(
            task_id=f"review_{today}",
            result={
                'success': True,
                'date': today,
                'tasks_completed': int(tasks_completed),
                'skills_installed': int(skills_installed),
                'skill_executed': skill_id,
                'reflection_triggered': bool(result.reflection_triggered),
                'report_path': str(report_path),
                'summary': report.get('summary', '')
            },
            notification_type='console'
        )
        print(f"  鉁?閫氱煡宸插彂閫侊細{notification_result['success']}\n")
        
        # 杩斿洖缁撴灉
        return {
            'success': True,
            'date': today,
            'tasks_completed': int(tasks_completed),
            'skills_installed': int(skills_installed),
            'skill_executed': skill_id,
            'reflection_triggered': bool(result.reflection_triggered),
            'report_path': str(report_path),
            'summary': report.get('summary', ''),
            'notification_sent': notification_result['success']
        }
    
    def _generate_report(self, context: Dict[str, Any], execution_result) -> Dict[str, Any]:
        """鐢熸垚澶嶇洏鎶ュ憡"""
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 浠庝笂涓嬫枃鎻愬彇鎴栫敓鎴愭暟鎹?        tasks = context.get('tasks', [])
        if not tasks:
            # 榛樿浠诲姟鍒楄〃
            tasks = [
                "OpenClaw 绯荤粺鑷",
                "寮曞浠诲姟 - 韬唤閰嶇疆",
                "绠＄悊鍛樻潈闄愰厤缃?,
                "瀹夎 Tavily 鎼滅储鎶€鑳?,
                "閰嶇疆 OpenCode 涓洪粯璁や唬鐮佸伐鍏?,
                "瀹夎 Self-Evolving Skill",
                "閰嶇疆 Python 鏍稿績妯″潡",
                "纭琛屼负瑙勫垯",
                "鏇存柊 AGENTS.md"
            ]
        
        issues = context.get('issues', [
            "PowerShell GBK 缂栫爜闂",
            "JSON 搴忓垪鍖栭敊璇?,
            "ClawHub 闄愭祦"
        ])
        
        lessons = context.get('lessons', [
            "绠＄悊鍛樻潈闄愰渶瑕佷慨鏀?Scheduled Task RunLevel",
            "Self-Evolving Skill 闇€瑕?numpy/scipy",
            "Windows 鍛戒护琛岄渶瑕?UTF-8 璁剧疆"
        ])
        
        improvements = context.get('improvements', [
            "鍚姩 MCP 鏈嶅姟鍣?,
            "閰嶇疆蹇冭烦浠诲姟",
            "閰嶇疆娑堟伅娓犻亾",
            "瀹屽杽澶嶇洏鑷姩鍖?
        ])
        
        # 鐢熸垚鎶ュ憡
        report = {
            'date': today,
            'summary': f"浠婃棩瀹屾垚 {len(tasks)} 涓换鍔★紝瀹夎 {context.get('skills_installed', 7)} 涓妧鑳?,
            'tasks': tasks,
            'issues': issues,
            'lessons': lessons,
            'improvements': improvements,
            'skill_execution': {
                'skill_id': execution_result.skill_id,
                'success': execution_result.success,
                'reflection_triggered': execution_result.reflection_triggered
            },
            'stats': self.engine.get_stats()
        }
        
        return report
    
    def _write_review_file(self, date: str, report: Dict[str, Any]) -> Path:
        """鍐欏叆澶嶇洏鏂囦欢"""
        
        file_path = self.memory_dir / f'review-{date}.md'
        
        content = f"""# 澶嶇洏 {date}

## 鎬荤粨

{report['summary']}

## 瀹屾垚鐨勪换鍔?
"""
        
        for i, task in enumerate(report['tasks'], 1):
            content += f"{i}. {task}\n"
        
        content += "\n## 閬囧埌鐨勯棶棰榎n\n"
        for issue in report['issues']:
            content += f"- {issue}\n"
        
        content += "\n## 瀛﹀埌鐨勬暀璁璡n\n"
        for lesson in report['lessons']:
            content += f"- {lesson}\n"
        
        content += "\n## 涓嬩竴姝ユ敼杩沑n\n"
        for imp in report['improvements']:
            content += f"- [ ] {imp}\n"
        
        content += f"""
---
**Self-Evolving Skill 鎵ц璁板綍:**
- 鎶€鑳?ID: {report['skill_execution']['skill_id']}
- 鎵ц鎴愬姛锛歿report['skill_execution']['success']}
- 鍙嶆€濊Е鍙戯細{report['skill_execution']['reflection_triggered']}
- 绯荤粺缁熻锛歿json.dumps(report['stats'], indent=2, ensure_ascii=False)}
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return file_path
    
    def _update_memory_md(self, report: Dict[str, Any]) -> None:
        """鏇存柊 MEMORY.md"""
        
        memory_path = self.workspace_dir / 'MEMORY.md'
        
        # 璇诲彇鐜版湁鍐呭
        if memory_path.exists():
            with open(memory_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = "# MEMORY.md - 闀挎湡璁板繂\n\n_閲嶈浜嬩欢銆佸喅绛栥€佷笂涓嬫枃鍜屾暀璁殑绮鹃€夎褰昣\n\n---\n\n"
        
        # 妫€鏌ユ槸鍚﹀凡鏈変粖鏃ュ鐩?        today_marker = f"## {report['date']}"
        if today_marker not in content:
            # 娣诲姞鏂扮殑澶嶇洏璁板綍
            new_section = f"""
## {report['date']}

- **澶嶇洏**: {report['summary']}
- **鎶€鑳芥墽琛?*: {report['skill_execution']['skill_id']}
- **鍙嶆€濊Е鍙?*: {report['skill_execution']['reflection_triggered']}

"""
            # 鎻掑叆鍒版枃浠舵湯灏句箣鍓?            lines = content.split('\n')
            if len(lines) > 3:
                # 鍦ㄥ€掓暟绗笁琛屾彃鍏ワ紙鍦ㄦ渶鍚庣殑娉ㄩ噴涔嬪墠锛?                insert_pos = -3 if len(lines) > 3 else -1
                lines.insert(insert_pos, new_section)
                content = '\n'.join(lines)
            
            # 鍐欏叆鏇存柊
            with open(memory_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    def get_status(self) -> Dict[str, Any]:
        """鑾峰彇浠ｇ悊鐘舵€?""
        return {
            'initialized': True,
            'skills_loaded': len(self.engine.skill_library),
            'storage_dir': str(self.engine.storage.storage_dir),
            'memory_dir': str(self.memory_dir)
        }


# 涓诲叆鍙?- 鐢ㄤ簬鍛戒护琛屾祴璇?if __name__ == '__main__':
    print("="*60)
    print("澶嶇洏鍚庡彴浠ｇ悊 - 娴嬭瘯妯″紡")
    print("="*60)
    
    # 鍒涘缓浠ｇ悊
    agent = ReviewBackgroundAgent()
    
    # 娴嬭瘯澶嶇洏
    context = {
        'skill_id': list(agent.engine.skill_library.keys())[0],
        'tasks_completed': 9,
        'skills_installed': 7,
        'value': 0.95
    }
    
    result = agent.execute_review(context)
    
    print(f"\n{'='*60}")
    print("澶嶇洏瀹屾垚锛?)
    print(f"{'='*60}")
    print(f"鏃ユ湡锛歿result['date']}")
    print(f"浠诲姟锛歿result['tasks_completed']} 涓?)
    print(f"鎶€鑳斤細{result['skills_installed']} 涓?)
    print(f"鎶ュ憡锛歿result['report_path']}")
    print(f"鎬荤粨锛歿result['summary']}")
