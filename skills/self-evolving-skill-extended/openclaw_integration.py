#!/usr/bin/env python3
"""
OpenClaw 闆嗘垚灏佽

鎻愪緵 OpenClaw sessions_yield 璋冪敤鎺ュ彛
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# 娣诲姞璺緞
sys.path.insert(0, str(Path(__file__).parent))

from sessions_yield_adapter import SessionsYieldAdapter, execute_review_sync
from notification_manager import NotificationManager


class OpenClawReviewTool:
    """OpenClaw 澶嶇洏宸ュ叿"""
    
    def __init__(self):
        """鍒濆鍖?OpenClaw 宸ュ叿"""
        self.adapter = SessionsYieldAdapter()
        self.notifier = NotificationManager()
        
        print(f"[OpenClawTool] 鍒濆鍖栧畬鎴?)
        print(f"[OpenClawTool] 寮傛閫傞厤鍣細宸插惎鐢?)
        print(f"[OpenClawTool] 閫氱煡绠＄悊鍣細宸插惎鐢?)
    
    def daily_review(
        self,
        context: Optional[Dict[str, Any]] = None,
        async_mode: bool = True
    ) -> Dict[str, Any]:
        """
        姣忔棩澶嶇洏
        
        Args:
            context: 澶嶇洏涓婁笅鏂?            async_mode: 鏄惁寮傛鎵ц
            
        Returns:
            澶嶇洏缁撴灉
        """
        
        if context is None:
            context = {}
        
        print(f"\n[OpenClawTool] 寮€濮嬫瘡鏃ュ鐩?..")
        print(f"  妯″紡锛歿'寮傛' if async_mode else '鍚屾'}")
        
        if async_mode:
            # 寮傛妯″紡
            result = self.adapter.start_background_review(context)
            
            # 杩斿洖 sessions_yield 鏍煎紡
            return {
                'yield': True,
                'message': '馃 鏀跺埌锛屽紑濮嬪鐩樹粖鏃ヤ换鍔?..',
                'followUp': {
                    'task': 'daily_review_background',
                    'task_id': result['task_id'],
                    'context': context
                },
                'immediate_response': {
                    'type': 'acknowledgment',
                    'text': result['message'],
                    'task_id': result['task_id'],
                    'estimated_time': result.get('estimated_time', '30-40 绉?)
                }
            }
        else:
            # 鍚屾妯″紡
            result = execute_review_sync(context)
            
            return {
                'yield': False,
                'immediate_response': {
                    'type': 'completion',
                    'text': '鉁?澶嶇洏瀹屾垚',
                    'details': result
                }
            }
    
    def handle_followUp(self, followUp_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        澶勭悊璺熻繘浠诲姟 (鍚庡彴瀹屾垚鍚庤皟鐢?
        
        Args:
            followUp_data: 璺熻繘鏁版嵁
            
        Returns:
            瀹屾垚閫氱煡
        """
        
        task_id = followUp_data.get('task_id')
        context = followUp_data.get('context', {})
        
        print(f"\n[OpenClawTool] 澶勭悊璺熻繘浠诲姟...")
        print(f"  浠诲姟 ID: {task_id}")
        
        # 杩欓噷搴旇妫€鏌ュ悗鍙拌繘绋嬬姸鎬?        # 绠€鍖栧疄鐜帮細鍋囪宸插畬鎴?        
        return {
            'type': 'completion_notification',
            'task_id': task_id,
            'message': '鉁?浠婃棩澶嶇洏瀹屾垚锛?,
            'summary': self._generate_summary(context)
        }
    
    def _generate_summary(self, context: Dict[str, Any]) -> str:
        """鐢熸垚绠€瑕佹€荤粨"""
        
        tasks = context.get('tasks_completed', 0)
        skills = context.get('skills_installed', 0)
        
        return f"馃搳 瀹屾垚浠诲姟锛歿tasks} 涓猏n馃 瀹夎鎶€鑳斤細{skills} 涓?
    
    def get_status(self) -> Dict[str, Any]:
        """鑾峰彇宸ュ叿鐘舵€?""
        
        return {
            'initialized': True,
            'async_mode': True,
            'adapter_status': 'ready',
            'notifier_status': 'ready'
        }


# OpenClaw sessions_yield 璋冪敤绀轰緥
def openclaw_sessions_yield_example():
    """
    OpenClaw sessions_yield 璋冪敤绀轰緥
    
    杩欐槸鍦?OpenClaw 涓殑瀹為檯浣跨敤鏂瑰紡
    """
    
    # 绀轰緥 1: 寮傛澶嶇洏
    print("="*60)
    print("绀轰緥 1: 寮傛澶嶇洏")
    print("="*60)
    
    tool = OpenClawReviewTool()
    
    # 鍦?OpenClaw 涓繖鏍疯皟鐢?
    # await sessions_yield({
    #     message: "馃 鏀跺埌锛屽紑濮嬪鐩樹粖鏃ヤ换鍔?..",
    #     followUp: {
    #         task: "daily_review_background",
    #         context: {...}
    #     }
    # })
    
    result = tool.daily_review(
        context={'tasks_completed': 9, 'skills_installed': 7},
        async_mode=True
    )
    
    print(f"缁撴灉锛歿json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # 绀轰緥 2: 鍚屾澶嶇洏
    print("\n" + "="*60)
    print("绀轰緥 2: 鍚屾澶嶇洏")
    print("="*60)
    
    result = tool.daily_review(
        context={'tasks_completed': 9},
        async_mode=False
    )
    
    print(f"缁撴灉锛歿json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # 绀轰緥 3: 澶勭悊璺熻繘
    print("\n" + "="*60)
    print("绀轰緥 3: 澶勭悊璺熻繘")
    print("="*60)
    
    followUp_result = tool.handle_followUp({
        'task_id': 'review_001',
        'context': {'tasks_completed': 9}
    })
    
    print(f"缁撴灉锛歿json.dumps(followUp_result, indent=2, ensure_ascii=False)}")


# CLI 鍏ュ彛
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--example':
        # 杩愯绀轰緥
        openclaw_sessions_yield_example()
    else:
        # 绠€鍗曟祴璇?        print("OpenClaw 闆嗘垚宸ュ叿")
        print("鐢ㄦ硶锛歱y openclaw_integration.py --example")
        
        tool = OpenClawReviewTool()
        status = tool.get_status()
        print(f"\n宸ュ叿鐘舵€侊細{status}")
