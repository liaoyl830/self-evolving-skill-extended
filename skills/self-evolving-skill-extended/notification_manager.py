#!/usr/bin/env python3
"""
閫氱煡绠＄悊鍣?
澶勭悊澶嶇洏瀹屾垚鍚庣殑閫氱煡鍙戦€?鏀寔澶氱閫氱煡鏂瑰紡锛氱郴缁熶簨浠躲€佹秷鎭€佹枃浠剁瓑
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List


class NotificationManager:
    """閫氱煡绠＄悊鍣?""
    
    def __init__(self, workspace_dir: Optional[str] = None):
        """
        鍒濆鍖栭€氱煡绠＄悊鍣?        
        Args:
            workspace_dir: 宸ヤ綔绌洪棿鐩綍
        """
        if workspace_dir is None:
            workspace_dir = Path(__file__).parent.parent
        
        self.workspace_dir = Path(workspace_dir)
        self.memory_dir = self.workspace_dir / 'memory'
        self.notifications_dir = self.workspace_dir / 'notifications'
        
        # 纭繚鐩綍瀛樺湪
        self.notifications_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"[NotificationManager] 鍒濆鍖栧畬鎴?)
        print(f"[NotificationManager] 宸ヤ綔绌洪棿锛歿self.workspace_dir}")
    
    def send_completion_notification(
        self,
        task_id: str,
        result: Dict[str, Any],
        notification_type: str = 'all'
    ) -> Dict[str, Any]:
        """
        鍙戦€佸畬鎴愰€氱煡
        
        Args:
            task_id: 浠诲姟 ID
            result: 浠诲姟缁撴灉
            notification_type: 閫氱煡绫诲瀷 (all/system/file/console)
            
        Returns:
            閫氱煡鍙戦€佺粨鏋?        """
        print(f"\n[Notification] 鍙戦€佸畬鎴愰€氱煡...")
        print(f"  浠诲姟 ID: {task_id}")
        print(f"  閫氱煡绫诲瀷锛歿notification_type}")
        
        notifications_sent = []
        
        # 1. 鎺у埗鍙伴€氱煡 (鎬绘槸鍙戦€?
        console_result = self._send_console_notification(result)
        notifications_sent.append({
            'type': 'console',
            'success': console_result['success']
        })
        
        if notification_type in ['all', 'system']:
            # 2. 绯荤粺浜嬩欢閫氱煡
            system_result = self._send_system_event(result)
            notifications_sent.append({
                'type': 'system',
                'success': system_result['success'],
                'message': system_result.get('message', '')
            })
        
        if notification_type in ['all', 'file']:
            # 3. 鏂囦欢閫氱煡
            file_result = self._write_notification_file(task_id, result)
            notifications_sent.append({
                'type': 'file',
                'success': file_result['success'],
                'path': file_result.get('path', '')
            })
        
        # 姹囨€荤粨鏋?        all_success = all(n['success'] for n in notifications_sent)
        
        return {
            'success': all_success,
            'task_id': task_id,
            'notifications_sent': notifications_sent,
            'timestamp': datetime.now().isoformat()
        }
    
    def _send_console_notification(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """鍙戦€佹帶鍒跺彴閫氱煡"""
        
        try:
            print("\n" + "="*60)
            print("鉁?澶嶇洏瀹屾垚锛?)
            print("="*60)
            print(f"馃搳 鏃ユ湡锛歿result.get('date', 'N/A')}")
            print(f"馃摑 瀹屾垚浠诲姟锛歿result.get('tasks_completed', 0)} 涓?)
            print(f"馃 瀹夎鎶€鑳斤細{result.get('skills_installed', 0)} 涓?)
            print(f"馃挕 鍙嶆€濊Е鍙戯細{'鏄? if result.get('reflection_triggered') else '鍚?}")
            print(f"馃搫 鎶ュ憡璺緞锛歿result.get('report_path', 'N/A')}")
            print(f"馃搵 鎬荤粨锛歿result.get('summary', 'N/A')}")
            print("="*60 + "\n")
            
            return {
                'success': True,
                'message': 'Console notification sent'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _send_system_event(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        鍙戦€佺郴缁熶簨浠堕€氱煡
        
        浣跨敤 OpenClaw system event 鍛戒护
        """
        
        try:
            # 鏋勫缓閫氱煡娑堟伅
            summary = result.get('summary', '澶嶇洏瀹屾垚')
            tasks = result.get('tasks_completed', 0)
            skills = result.get('skills_installed', 0)
            
            message = (
                f"鉁?浠婃棩澶嶇洏瀹屾垚锛乗n"
                f"馃搳 瀹屾垚浠诲姟锛歿tasks} 涓猏n"
                f"馃 瀹夎鎶€鑳斤細{skills} 涓猏n"
                f"馃搫 璇︾粏鎶ュ憡锛歿result.get('report_path', '鏌ョ湅 memory/ 鐩綍')}"
            )
            
            # 璋冪敤 OpenClaw system event
            # 娉ㄦ剰锛氳繖闇€瑕佸湪 OpenClaw 鐜涓繍琛?            cmd = f'openclaw system event --text "{message}" --mode now'
            
            # 灏濊瘯鎵ц (濡傛灉 OpenClaw 鍙敤)
            import subprocess
            process_result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if process_result.returncode == 0:
                return {
                    'success': True,
                    'message': message,
                    'command': cmd
                }
            else:
                # OpenClaw 涓嶅彲鐢紝闄嶇骇鍒版帶鍒跺彴
                print(f"[SystemEvent] 鍛戒护鎵ц澶辫触锛歿process_result.stderr}")
                return {
                    'success': False,
                    'error': process_result.stderr,
                    'fallback': 'console'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'fallback': 'console'
            }
    
    def _write_notification_file(self, task_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """鍐欏叆閫氱煡鏂囦欢"""
        
        try:
            file_path = self.notifications_dir / f'{task_id}.json'
            
            notification = {
                'task_id': task_id,
                'type': 'review_completion',
                'timestamp': datetime.now().isoformat(),
                'result': result,
                'read': False
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(notification, f, indent=2, ensure_ascii=False)
            
            return {
                'success': True,
                'path': str(file_path)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_timeout_warning(
        self,
        task_id: str,
        timeout_seconds: int
    ) -> Dict[str, Any]:
        """
        鍙戦€佽秴鏃惰鍛?        
        Args:
            task_id: 浠诲姟 ID
            timeout_seconds: 瓒呮椂鏃堕棿 (绉?
            
        Returns:
            閫氱煡缁撴灉
        """
        
        message = (
            f"鈿狅笍 澶嶇洏浠诲姟瓒呮椂璀﹀憡\n"
            f"浠诲姟 ID: {task_id}\n"
            f"瓒呮椂鏃堕棿锛歿timeout_seconds} 绉抃n"
            f"鐘舵€侊細浠嶅湪鍚庡彴杩愯锛屼絾宸茶秴杩囬鏈熸椂闂?
        )
        
        print("\n" + "="*60)
        print("鈿狅笍 瓒呮椂璀﹀憡")
        print("="*60)
        print(message)
        print("="*60 + "\n")
        
        # 鍐欏叆瓒呮椂璁板綍
        timeout_file = self.notifications_dir / f'{task_id}_timeout.json'
        
        try:
            with open(timeout_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'task_id': task_id,
                    'type': 'timeout_warning',
                    'timeout_seconds': timeout_seconds,
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
            
            return {
                'success': True,
                'message': message
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_error_notification(
        self,
        task_id: str,
        error: str,
        fallback_mode: bool = False
    ) -> Dict[str, Any]:
        """
        鍙戦€侀敊璇€氱煡
        
        Args:
            task_id: 浠诲姟 ID
            error: 閿欒淇℃伅
            fallback_mode: 鏄惁鍚敤闄嶇骇妯″紡
            
        Returns:
            閫氱煡缁撴灉
        """
        
        message = (
            f"鉂?澶嶇洏浠诲姟澶辫触\n"
            f"浠诲姟 ID: {task_id}\n"
            f"閿欒锛歿error}\n"
            f"{'宸插垏鎹㈠埌闄嶇骇妯″紡' if fallback_mode else ''}"
        )
        
        print("\n" + "="*60)
        print("鉂?閿欒閫氱煡")
        print("="*60)
        print(message)
        print("="*60 + "\n")
        
        # 鍐欏叆閿欒璁板綍
        error_file = self.notifications_dir / f'{task_id}_error.json'
        
        try:
            with open(error_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'task_id': task_id,
                    'type': 'error',
                    'error': error,
                    'fallback_mode': fallback_mode,
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
            
            return {
                'success': True,
                'message': message
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_unread_notifications(self) -> List[Dict[str, Any]]:
        """鍒楀嚭鏈閫氱煡"""
        
        unread = []
        
        for file in self.notifications_dir.glob('*.json'):
            if '_timeout' in file.stem or '_error' in file.stem:
                continue
            
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    notification = json.load(f)
                    if not notification.get('read', False):
                        unread.append(notification)
            except:
                pass
        
        return unread
    
    def mark_as_read(self, task_id: str) -> bool:
        """鏍囪涓哄凡璇?""
        
        file_path = self.notifications_dir / f'{task_id}.json'
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                notification = json.load(f)
            
            notification['read'] = True
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(notification, f, indent=2, ensure_ascii=False)
            
            return True
        except:
            return False


# 娴嬭瘯
if __name__ == '__main__':
    print("="*60)
    print("閫氱煡绠＄悊鍣?- 娴嬭瘯")
    print("="*60)
    
    manager = NotificationManager()
    
    # 娴嬭瘯瀹屾垚閫氱煡
    result = {
        'success': True,
        'date': '2026-03-14',
        'tasks_completed': 9,
        'skills_installed': 7,
        'reflection_triggered': False,
        'report_path': 'memory/review-2026-03-14.md',
        'summary': '浠婃棩瀹屾垚 9 涓换鍔★紝瀹夎 7 涓妧鑳?
    }
    
    print("\n[娴嬭瘯 1] 鍙戦€佸畬鎴愰€氱煡...")
    notification_result = manager.send_completion_notification(
        task_id='test_001',
        result=result,
        notification_type='console'
    )
    
    print(f"閫氱煡缁撴灉锛歿notification_result}")
    
    # 娴嬭瘯瓒呮椂璀﹀憡
    print("\n[娴嬭瘯 2] 鍙戦€佽秴鏃惰鍛?..")
    timeout_result = manager.send_timeout_warning(
        task_id='test_001',
        timeout_seconds=300
    )
    
    print(f"瓒呮椂缁撴灉锛歿timeout_result}")
    
    # 娴嬭瘯閿欒閫氱煡
    print("\n[娴嬭瘯 3] 鍙戦€侀敊璇€氱煡...")
    error_result = manager.send_error_notification(
        task_id='test_001',
        error='娴嬭瘯閿欒',
        fallback_mode=True
    )
    
    print(f"閿欒缁撴灉锛歿error_result}")
    
    # 鍒楀嚭鏈閫氱煡
    print("\n[娴嬭瘯 4] 鍒楀嚭鏈閫氱煡...")
    unread = manager.list_unread_notifications()
    print(f"鏈閫氱煡锛歿len(unread)} 涓?)
    
    print("\n" + "="*60)
    print("娴嬭瘯瀹屾垚")
    print("="*60)
