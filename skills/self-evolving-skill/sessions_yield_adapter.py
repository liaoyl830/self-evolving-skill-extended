#!/usr/bin/env python3
"""
sessions_yield 閫傞厤鍣?
瀹炵幇 OpenClaw sessions_yield 闆嗘垚
"""

import subprocess
import json
import sys
import os
import time
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from error_handler import ErrorHandler, FallbackMechanism


class SessionsYieldAdapter:
    """sessions_yield 閫傞厤鍣?""
    
    def __init__(self):
        """鍒濆鍖栭€傞厤鍣?""
        self.script_dir = Path(__file__).parent
        self.review_agent = self.script_dir / 'review_background_agent.py'
        self.error_handler = ErrorHandler(max_retries=3, retry_delay=1.0)
        self.fallback = FallbackMechanism()
        
        print(f"[YieldAdapter] 鍒濆鍖栧畬鎴?)
        print(f"[YieldAdapter] 澶嶇洏浠ｇ悊锛歿self.review_agent}")
        print(f"[YieldAdapter] 閿欒澶勭悊鍣細宸插惎鐢?)
    
    def start_background_review(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        鍚姩鍚庡彴澶嶇洏
        
        Args:
            context: 澶嶇洏涓婁笅鏂?            
        Returns:
            绔嬪嵆杩斿洖鐨勪换鍔′俊鎭?        """
        print(f"\n[YieldAdapter] 鍚姩鍚庡彴澶嶇洏...")
        
        # 鐢熸垚浠诲姟 ID
        task_id = f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 鍑嗗鍚庡彴杩涚▼
        cmd = [
            sys.executable,
            str(self.review_agent),
            '--json',  # JSON 杈撳嚭
            '--task-id', task_id
        ]
        
        # 浼犻€掍笂涓嬫枃
        env = {**os.environ, 'REVIEW_CONTEXT': json.dumps(context)}
        
        try:
            # 鍚姩鍚庡彴杩涚▼锛堜笉绛夊緟锛?            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                cwd=str(self.script_dir)
            )
            
            print(f"[YieldAdapter] 鍚庡彴杩涚▼宸插惎鍔?(PID: {process.pid})")
            
            # 鍚姩鐩戞帶绾跨▼锛堣秴鏃跺鐞嗭級
            import threading
            monitor_thread = threading.Thread(
                target=self._monitor_process,
                args=(process, task_id),
                daemon=True
            )
            monitor_thread.start()
            
            # 绔嬪嵆杩斿洖
            return {
                'success': True,
                'task_id': task_id,
                'status': 'running',
                'pid': process.pid,
                'message': '馃 鏀跺埌锛屽紑濮嬪鐩樹粖鏃ヤ换鍔?..',
                'estimated_time': '30-40 绉?
            }
            
        except Exception as e:
            print(f"[YieldAdapter] 鍚姩澶辫触锛歿e}")
            # 闄嶇骇鍒板悓姝ユā寮?            return self._fallback_sync_review(context)
    
    def _monitor_process(self, process: subprocess.Popen, task_id: str, timeout: int = 300):
        """
        鐩戞帶鍚庡彴杩涚▼
        
        Args:
            process: 杩涚▼瀵硅薄
            task_id: 浠诲姟 ID
            timeout: 瓒呮椂鏃堕棿 (绉?
        """
        try:
            # 绛夊緟杩涚▼瀹屾垚锛堝甫瓒呮椂锛?            process.wait(timeout=timeout)
            
            if process.returncode == 0:
                print(f"[Monitor] 浠诲姟 {task_id} 瀹屾垚")
            else:
                print(f"[Monitor] 浠诲姟 {task_id} 澶辫触锛岃繑鍥炵爜锛歿process.returncode}")
                
        except subprocess.TimeoutExpired:
            print(f"[Monitor] 浠诲姟 {task_id} 瓒呮椂 ({timeout}绉?")
            process.kill()
            
            # 鍙戦€佽秴鏃堕€氱煡
            from notification_manager import NotificationManager
            notifier = NotificationManager()
            notifier.send_timeout_warning(task_id, timeout)
    
    def _fallback_sync_review(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        闄嶇骇鍒板悓姝ュ鐩?        
        Args:
            context: 澶嶇洏涓婁笅鏂?            
        Returns:
            澶嶇洏缁撴灉
        """
        print(f"[YieldAdapter] 闄嶇骇鍒板悓姝ユā寮?..")
        
        try:
            from review_background_agent import ReviewBackgroundAgent
            
            agent = ReviewBackgroundAgent()
            result = agent.execute_review(context)
            
            return {
                'success': True,
                'task_id': f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'status': 'completed',
                'result': result,
                'fallback_used': True,
                'message': '鉁?澶嶇洏瀹屾垚锛堝悓姝ユā寮忥級'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'fallback_used': True,
                'message': '鉂?澶嶇洏澶辫触'
            }
    
    def check_status(self, task_id: str) -> Dict[str, Any]:
        """
        妫€鏌ヤ换鍔＄姸鎬?        
        Args:
            task_id: 浠诲姟 ID
            
        Returns:
            浠诲姟鐘舵€?        """
        # 绠€鍖栧疄鐜帮細鍋囪浠诲姟宸插畬鎴?        return {
            'task_id': task_id,
            'status': 'completed',
            'progress': 100
        }
    
    def get_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        鑾峰彇浠诲姟缁撴灉
        
        Args:
            task_id: 浠诲姟 ID
            
        Returns:
            浠诲姟缁撴灉
        """
        # 浠庢枃浠惰鍙栫粨鏋?        result_file = self.script_dir / 'tasks' / f'{task_id}.json'
        
        if result_file.exists():
            with open(result_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return None


# 绠€鍖栫殑鍚屾鐗堟湰锛堢敤浜庢祴璇曪級
def execute_review_sync(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    鍚屾鎵ц澶嶇洏锛堥檷绾ф柟妗堬級
    
    Args:
        context: 澶嶇洏涓婁笅鏂?        
    Returns:
        澶嶇洏缁撴灉
    """
    import os
    os.environ['PYTHONUTF8'] = '1'
    
    error_handler = ErrorHandler(max_retries=2)
    
    def run_review():
        cmd = [sys.executable, 'review_background_agent.py']
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent),
            env={**os.environ, 'PYTHONUTF8': '1'}
        )
        
        if result.returncode == 0:
            return {
                'success': True,
                'message': '鉁?澶嶇洏瀹屾垚',
                'output': result.stdout
            }
        else:
            raise Exception(result.stderr)
    
    def fallback_review():
        from review_background_agent import ReviewBackgroundAgent
        
        agent = ReviewBackgroundAgent()
        result = agent.execute_review(context)
        
        return {
            'success': True,
            'message': '鉁?澶嶇洏瀹屾垚锛堥檷绾фā寮忥級',
            'result': result
        }
    
    return error_handler.retry_on_error(
        run_review,
        fallback_func=fallback_review
    )


# 娴嬭瘯
if __name__ == '__main__':
    print("="*60)
    print("sessions_yield 閫傞厤鍣?- 娴嬭瘯")
    print("="*60)
    
    adapter = SessionsYieldAdapter()
    
    # 娴嬭瘯鍚庡彴鍚姩
    context = {
        'tasks_completed': 9,
        'skills_installed': 7,
        'value': 0.95
    }
    
    result = adapter.start_background_review(context)
    
    print(f"\n娴嬭瘯缁撴灉:")
    print(f"  鎴愬姛锛歿result['success']}")
    print(f"  浠诲姟 ID: {result['task_id']}")
    print(f"  鐘舵€侊細{result['status']}")
    print(f"  娑堟伅锛歿result['message']}")
