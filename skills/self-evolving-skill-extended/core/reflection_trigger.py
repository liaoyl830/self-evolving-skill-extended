"""
鑷€傚簲鍙嶆€濊Е鍙戝櫒

鍩轰簬娈嬪樊鑳介噺鍜屼环鍊煎鐩婅嚜鍔ㄥ垽鏂綍鏃堕渶瑕佸涔?"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class TriggerResult:
    """瑙﹀彂缁撴灉"""
    should_trigger: bool
    reason: str
    energy_ratio: float
    value_gain: Optional[float] = None


class ReflectionTrigger:
    """鑷€傚簲鍙嶆€濊Е鍙戝櫒"""
    
    def __init__(
        self,
        min_energy_ratio: float = 0.10,
        value_gain_threshold: float = 0.20,
        target_trigger_rate: float = 0.15
    ):
        """
        鍒濆鍖栬Е鍙戝櫒
        
        Args:
            min_energy_ratio: 鏈€灏忔畫宸兘閲忔瘮鐜囬槇鍊?            value_gain_threshold: 浠峰€煎鐩婇槇鍊?            target_trigger_rate: 鐩爣瑙﹀彂鐜?(0-1)
        """
        self.min_energy_ratio = min_energy_ratio
        self.value_gain_threshold = value_gain_threshold
        self.target_trigger_rate = target_trigger_rate
        
        # 鑷€傚簲璋冩暣
        self.actual_trigger_rate = 0.0
        self.trigger_count = 0
        self.total_checks = 0
    
    def check(
        self,
        residual_ratio: float,
        value_gain: Optional[float] = None,
        suggested_abstraction: str = 'SUB_SKILL'
    ) -> TriggerResult:
        """
        妫€鏌ユ槸鍚﹀簲璇ヨЕ鍙戝弽鎬?        
        Args:
            residual_ratio: 娈嬪樊鑳介噺姣旂巼
            value_gain: 浠峰€煎鐩?(鍙€?
            suggested_abstraction: 寤鸿鐨勬娊璞″眰绾?            
        Returns:
            TriggerResult: 瑙﹀彂缁撴灉
        """
        self.total_checks += 1
        
        # 鍩虹鍒ゆ柇锛氭畫宸兘閲忔槸鍚﹁秴杩囬槇鍊?        energy_exceeded = residual_ratio >= self.min_energy_ratio
        
        # 浠峰€煎鐩婂垽鏂?(濡傛灉鏈?
        value_ok = True
        if value_gain is not None:
            value_ok = value_gain >= self.value_gain_threshold
        
        # 鎶借薄灞傜骇褰卞搷
        abstraction_bonus = 0.0
        if suggested_abstraction == 'POLICY':
            abstraction_bonus = 0.05  # 绛栫暐灞傛洿瀹规槗瑙﹀彂
        elif suggested_abstraction == 'PREDICATE':
            abstraction_bonus = -0.05  # 璋撹瘝灞傛洿闅捐Е鍙?        
        # 鑷€傚簲璋冩暣闃堝€?        adjusted_threshold = self._adjust_threshold()
        
        # 缁煎悎鍒ゆ柇
        should_trigger = (
            energy_exceeded and 
            value_ok and 
            (residual_ratio >= adjusted_threshold - abstraction_bonus)
        )
        
        if should_trigger:
            self.trigger_count += 1
            self.actual_trigger_rate = self.trigger_count / self.total_checks
        
        # 鐢熸垚鍘熷洜
        reason = self._generate_reason(
            should_trigger,
            residual_ratio,
            adjusted_threshold,
            value_gain,
            suggested_abstraction
        )
        
        return TriggerResult(
            should_trigger=should_trigger,
            reason=reason,
            energy_ratio=residual_ratio,
            value_gain=value_gain
        )
    
    def _adjust_threshold(self) -> float:
        """鏍规嵁瀹為檯瑙﹀彂鐜囪皟鏁撮槇鍊?""
        if self.total_checks < 10:
            return self.min_energy_ratio
        
        # 濡傛灉瀹為檯瑙﹀彂鐜囦綆浜庣洰鏍囷紝闄嶄綆闃堝€?        # 濡傛灉瀹為檯瑙﹀彂鐜囬珮浜庣洰鏍囷紝鎻愰珮闃堝€?        rate_diff = self.actual_trigger_rate - self.target_trigger_rate
        
        if abs(rate_diff) < 0.05:
            return self.min_energy_ratio
        
        adjustment = rate_diff * 0.1
        adjusted = self.min_energy_ratio - adjustment
        
        # 闄愬埗鍦ㄥ悎鐞嗚寖鍥?        return max(0.05, min(0.30, adjusted))
    
    def _generate_reason(
        self,
        should_trigger: bool,
        residual_ratio: float,
        threshold: float,
        value_gain: Optional[float],
        abstraction: str
    ) -> str:
        """鐢熸垚瑙﹀彂鍘熷洜"""
        reasons = []
        
        if should_trigger:
            reasons.append(f"娈嬪樊鑳介噺 {residual_ratio:.2f} >= 闃堝€?{threshold:.2f}")
            if value_gain is not None:
                reasons.append(f"浠峰€煎鐩?{value_gain:.2f} 杈炬爣")
            reasons.append(f"鎶借薄灞傜骇锛歿abstraction}")
            return "瑙﹀彂鍙嶆€濓細" + ", ".join(reasons)
        else:
            if residual_ratio < threshold:
                reasons.append(f"娈嬪樊鑳介噺 {residual_ratio:.2f} < 闃堝€?{threshold:.2f}")
            if value_gain is not None and value_gain < self.value_gain_threshold:
                reasons.append(f"浠峰€煎鐩?{value_gain:.2f} < {self.value_gain_threshold}")
            return "涓嶈Е鍙戯細" + ", ".join(reasons)
    
    def get_stats(self) -> dict:
        """鑾峰彇瑙﹀彂鍣ㄧ粺璁?""
        return {
            'total_checks': self.total_checks,
            'trigger_count': self.trigger_count,
            'actual_trigger_rate': self.actual_trigger_rate,
            'target_trigger_rate': self.target_trigger_rate,
            'current_threshold': self._adjust_threshold()
        }
    
    def reset(self):
        """閲嶇疆缁熻"""
        self.trigger_count = 0
        self.total_checks = 0
        self.actual_trigger_rate = 0.0


# 娴嬭瘯
if __name__ == '__main__':
    trigger = ReflectionTrigger(
        min_energy_ratio=0.10,
        target_trigger_rate=0.15
    )
    
    # 妯℃嫙妫€鏌?    import random
    for i in range(20):
        residual = random.uniform(0.05, 0.25)
        value = random.uniform(0.1, 0.9)
        
        result = trigger.check(
            residual_ratio=residual,
            value_gain=value,
            suggested_abstraction='SUB_SKILL'
        )
        
        print(f"Check {i+1}: residual={residual:.2f}, value={value:.2f}")
        print(f"  -> {result.reason}")
    
    print(f"\n缁熻锛歿trigger.get_stats()}")
