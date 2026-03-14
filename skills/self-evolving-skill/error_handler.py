#!/usr/bin/env python3
"""
閿欒澶勭悊鍜岄檷绾ф満鍒?
鎻愪緵閿欒鎹曡幏銆侀噸璇曘€侀檷绾х瓑鍔熻兘
"""

import sys
import os
import time
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
import json


class ErrorHandler:
    """閿欒澶勭悊鍣?""
    
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        """
        鍒濆鍖栭敊璇鐞嗗櫒
        
        Args:
            max_retries: 鏈€澶ч噸璇曟鏁?            retry_delay: 閲嶈瘯寤惰繜 (绉?
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.error_log_dir = Path(__file__).parent / 'error_logs'
        
        # 纭繚鐩綍瀛樺湪
        self.error_log_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"[ErrorHandler] 鍒濆鍖栧畬鎴?)
        print(f"[ErrorHandler] 鏈€澶ч噸璇曪細{max_retries}")
        print(f"[ErrorHandler] 閲嶈瘯寤惰繜锛歿retry_delay}绉?)
    
    def retry_on_error(
        self,
        func: Callable,
        *args,
        fallback_func: Optional[Callable] = None,
        error_types: tuple = (Exception,),
        **kwargs
    ) -> Dict[str, Any]:
        """
        甯﹂噸璇曠殑閿欒澶勭悊
        
        Args:
            func: 瑕佹墽琛岀殑鍑芥暟
            *args: 鍑芥暟鍙傛暟
            fallback_func: 闄嶇骇鍑芥暟 (閲嶈瘯澶辫触鏃惰皟鐢?
            error_types: 瑕佹崟鑾风殑閿欒绫诲瀷
            **kwargs: 鍑芥暟鍏抽敭瀛楀弬鏁?            
        Returns:
            鎵ц缁撴灉
        """
        
        last_error = None
        
        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"\n[Retry] 灏濊瘯 {attempt}/{self.max_retries}...")
                
                # 鎵ц鍑芥暟
                result = func(*args, **kwargs)
                
                print(f"[Retry] 鎴愬姛锛?)
                
                return {
                    'success': True,
                    'result': result,
                    'attempts': attempt,
                    'error': None
                }
                
            except error_types as e:
                last_error = e
                print(f"[Retry] 澶辫触锛歿e}")
                
                if attempt < self.max_retries:
                    print(f"[Retry] {self.retry_delay}绉掑悗閲嶈瘯...")
                    time.sleep(self.retry_delay)
                else:
                    print(f"[Retry] 宸茶揪鏈€澶ч噸璇曟鏁?)
        
        # 鎵€鏈夐噸璇曞け璐?        print(f"[Retry] 鎵€鏈夐噸璇曞け璐ワ紝璋冪敤闄嶇骇鍑芥暟...")
        
        # 璁板綍閿欒
        self._log_error(func.__name__, last_error, args, kwargs)
        
        # 璋冪敤闄嶇骇鍑芥暟
        if fallback_func:
            try:
                fallback_result = fallback_func(*args, **kwargs)
                return {
                    'success': True,
                    'result': fallback_result,
                    'attempts': self.max_retries,
                    'error': str(last_error),
                    'fallback_used': True
                }
            except Exception as fallback_error:
                return {
                    'success': False,
                    'error': f"涓诲嚱鏁板け璐ワ細{last_error}, 闄嶇骇鍑芥暟澶辫触锛歿fallback_error}",
                    'attempts': self.max_retries,
                    'fallback_used': True
                }
        else:
            return {
                'success': False,
                'error': str(last_error),
                'attempts': self.max_retries,
                'fallback_used': False
            }
    
    def _log_error(
        self,
        func_name: str,
        error: Exception,
        args: tuple,
        kwargs: dict
    ) -> None:
        """璁板綍閿欒鏃ュ織"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = self.error_log_dir / f'{func_name}_{timestamp}.log'
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"閿欒鏃ュ織\n")
                f.write(f"="*60 + "\n\n")
                f.write(f"鏃堕棿锛歿datetime.now().isoformat()}\n")
                f.write(f"鍑芥暟锛歿func_name}\n")
                f.write(f"閿欒锛歿error}\n\n")
                f.write(f"鍙傛暟:\n")
                f.write(f"  args: {args}\n")
                f.write(f"  kwargs: {kwargs}\n\n")
                f.write(f"鍫嗘爤璺熻釜:\n")
                f.write(traceback.format_exc())
            
            print(f"[ErrorHandler] 閿欒鏃ュ織宸蹭繚瀛橈細{log_file}")
            
        except Exception as e:
            print(f"[ErrorHandler] 淇濆瓨閿欒鏃ュ織澶辫触锛歿e}")
    
    def safe_execute(
        self,
        func: Callable,
        *args,
        default_value: Any = None,
        **kwargs
    ) -> Any:
        """
        瀹夊叏鎵ц (涓嶆姏鍑哄紓甯?
        
        Args:
            func: 瑕佹墽琛岀殑鍑芥暟
            *args: 鍑芥暟鍙傛暟
            default_value: 澶辫触鏃剁殑榛樿鍊?            **kwargs: 鍑芥暟鍏抽敭瀛楀弬鏁?            
        Returns:
            鍑芥暟缁撴灉鎴栭粯璁ゅ€?        """
        
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[SafeExecute] {func.__name__} 澶辫触锛歿e}")
            self._log_error(func.__name__, e, args, kwargs)
            return default_value


class FallbackMechanism:
    """闄嶇骇鏈哄埗"""
    
    def __init__(self):
        """鍒濆鍖栭檷绾ф満鍒?""
        self.fallback_chain: List[Callable] = []
        print(f"[Fallback] 鍒濆鍖栧畬鎴?)
    
    def add_fallback(self, func: Callable) -> 'FallbackMechanism':
        """
        娣诲姞闄嶇骇鍑芥暟
        
        Args:
            func: 闄嶇骇鍑芥暟
            
        Returns:
            self (鏀寔閾惧紡璋冪敤)
        """
        self.fallback_chain.append(func)
        print(f"[Fallback] 娣诲姞闄嶇骇鍑芥暟锛歿func.__name__}")
        return self
    
    def execute_with_fallback(
        self,
        primary_func: Callable,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """
        鎵ц涓诲嚱鏁帮紝澶辫触鏃朵緷娆″皾璇曢檷绾у嚱鏁?        
        Args:
            primary_func: 涓诲嚱鏁?            *args: 鍑芥暟鍙傛暟
            **kwargs: 鍑芥暟鍏抽敭瀛楀弬鏁?            
        Returns:
            鎵ц缁撴灉
        """
        
        # 灏濊瘯涓诲嚱鏁?        try:
            print(f"[Fallback] 鎵ц涓诲嚱鏁帮細{primary_func.__name__}")
            result = primary_func(*args, **kwargs)
            
            return {
                'success': True,
                'result': result,
                'method': 'primary'
            }
            
        except Exception as e:
            print(f"[Fallback] 涓诲嚱鏁板け璐ワ細{e}")
            
            # 渚濇灏濊瘯闄嶇骇鍑芥暟
            for fallback_func in self.fallback_chain:
                try:
                    print(f"[Fallback] 灏濊瘯闄嶇骇鍑芥暟锛歿fallback_func.__name__}")
                    result = fallback_func(*args, **kwargs)
                    
                    return {
                        'success': True,
                        'result': result,
                        'method': fallback_func.__name__
                    }
                    
                except Exception as fallback_error:
                    print(f"[Fallback] 闄嶇骇鍑芥暟 {fallback_func.__name__} 澶辫触锛歿fallback_error}")
                    continue
            
            # 鎵€鏈夊嚱鏁伴兘澶辫触
            return {
                'success': False,
                'error': f"涓诲嚱鏁板拰鎵€鏈夐檷绾у嚱鏁伴兘澶辫触",
                'method': 'none'
            }


# 娴嬭瘯
if __name__ == '__main__':
    print("="*60)
    print("閿欒澶勭悊 - 娴嬭瘯")
    print("="*60)
    
    # 娴嬭瘯鍑芥暟
    def success_func():
        return "鎴愬姛"
    
    def fail_func():
        raise ValueError("娴嬭瘯閿欒")
    
    def fallback_func():
        return "闄嶇骇鎴愬姛"
    
    # 娴嬭瘯 1: 鎴愬姛鎵ц
    print("\n[娴嬭瘯 1] 鎴愬姛鎵ц...")
    handler = ErrorHandler(max_retries=3)
    result = handler.retry_on_error(success_func)
    print(f"缁撴灉锛歿result}")
    
    # 娴嬭瘯 2: 澶辫触鍚庨噸璇曟垚鍔?    print("\n[娴嬭瘯 2] 澶辫触鍚庨噸璇?..")
    attempt_count = [0]
    
    def fail_then_succeed():
        attempt_count[0] += 1
        if attempt_count[0] < 3:
            raise ValueError(f"绗瑊attempt_count[0]}娆″け璐?)
        return f"绗瑊attempt_count[0]}娆℃垚鍔?
    
    result = handler.retry_on_error(fail_then_succeed)
    print(f"缁撴灉锛歿result}")
    
    # 娴嬭瘯 3: 浣跨敤闄嶇骇鍑芥暟
    print("\n[娴嬭瘯 3] 浣跨敤闄嶇骇鍑芥暟...")
    result = handler.retry_on_error(
        fail_func,
        fallback_func=fallback_func
    )
    print(f"缁撴灉锛歿result}")
    
    # 娴嬭瘯 4: 闄嶇骇閾?    print("\n[娴嬭瘯 4] 闄嶇骇閾?..")
    fallback = FallbackMechanism()
    fallback.add_fallback(lambda: "闄嶇骇 1").add_fallback(lambda: "闄嶇骇 2")
    
    result = fallback.execute_with_fallback(fail_func)
    print(f"缁撴灉锛歿result}")
    
    print("\n" + "="*60)
    print("娴嬭瘯瀹屾垚")
    print("="*60)
