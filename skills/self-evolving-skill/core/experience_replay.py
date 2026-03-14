"""
缁忛獙鍥炴斁缂撳瓨

缂撳瓨宸插妯″紡锛岄檷浣庨噸澶嶈Е鍙?"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np
from collections import OrderedDict


@dataclass
class ExperiencePattern:
    """缁忛獙妯″紡"""
    id: str
    embedding_hash: str
    context_signature: str
    success_count: int = 0
    failure_count: int = 0
    avg_value: float = 0.0
    last_used: str = field(default_factory=lambda: datetime.now().isoformat())
    pattern_data: Dict[str, Any] = field(default_factory=dict)


class ExperienceReplay:
    """缁忛獙鍥炴斁缂撳瓨"""
    
    def __init__(self, capacity: int = 1000, similarity_threshold: float = 0.85):
        """
        鍒濆鍖栫粡楠屽洖鏀?        
        Args:
            capacity: 缂撳瓨瀹归噺
            similarity_threshold: 鐩镐技搴﹂槇鍊?        """
        self.capacity = capacity
        self.similarity_threshold = similarity_threshold
        
        # LRU 缂撳瓨
        self.cache: OrderedDict[str, ExperiencePattern] = OrderedDict()
        
        # 绱㈠紩
        self.by_context: Dict[str, List[str]] = {}
        self.by_hash: Dict[str, str] = {}
    
    def add(
        self,
        embedding: List[float],
        context: Dict[str, Any],
        success: bool = True,
        value: float = 1.0,
        pattern_data: Optional[Dict] = None
    ) -> Optional[ExperiencePattern]:
        """
        娣诲姞缁忛獙
        
        Args:
            embedding: 宓屽叆鍚戦噺
            context: 涓婁笅鏂?            success: 鏄惁鎴愬姛
            value: 浠峰€?            pattern_data: 妯″紡鏁版嵁
            
        Returns:
            鍖归厤鐨勬ā寮?(濡傛灉鏈?
        """
        # 璁＄畻宓屽叆鍝堝笇
        embedding_hash = self._hash_embedding(embedding)
        context_sig = self._context_signature(context)
        
        # 鏌ユ壘鐩镐技妯″紡
        existing = self._find_similar(embedding, context_sig)
        
        if existing:
            # 鏇存柊鐜版湁妯″紡
            existing.success_count += 1 if success else 0
            existing.failure_count += 0 if success else 1
            existing.avg_value = (existing.avg_value * (existing.success_count + existing.failure_count - 1) + value) / (existing.success_count + existing.failure_count)
            existing.last_used = datetime.now().isoformat()
            
            # 绉诲埌 LRU 鏈熬
            self.cache.move_to_end(existing.id)
            
            return existing
        else:
            # 鍒涘缓鏂版ā寮?            pattern_id = f"pattern_{len(self.cache) + 1:04d}"
            pattern = ExperiencePattern(
                id=pattern_id,
                embedding_hash=embedding_hash,
                context_signature=context_sig,
                success_count=1 if success else 0,
                failure_count=0 if success else 1,
                avg_value=value,
                pattern_data=pattern_data or {}
            )
            
            # 娣诲姞鍒扮紦瀛?            if len(self.cache) >= self.capacity:
                # 绉婚櫎鏈€鏃х殑
                self.cache.popitem(last=False)
            
            self.cache[pattern_id] = pattern
            self.by_hash[embedding_hash] = pattern_id
            
            # 绱㈠紩涓婁笅鏂?            if context_sig not in self.by_context:
                self.by_context[context_sig] = []
            self.by_context[context_sig].append(pattern_id)
            
            return None
    
    def query(
        self,
        embedding: List[float],
        context: Dict[str, Any]
    ) -> Optional[ExperiencePattern]:
        """
        鏌ヨ鐩镐技缁忛獙
        
        Args:
            embedding: 宓屽叆鍚戦噺
            context: 涓婁笅鏂?            
        Returns:
            鏈€鐩镐技鐨勬ā寮?        """
        context_sig = self._context_signature(context)
        
        # 鍏堟寜涓婁笅鏂囨煡鎵?        if context_sig in self.by_context:
            for pattern_id in self.by_context[context_sig]:
                if pattern_id in self.cache:
                    return self.cache[pattern_id]
        
        # 鍐嶆寜宓屽叆鐩镐技搴︽煡鎵?        return self._find_similar(embedding, context_sig)
    
    def _find_similar(
        self,
        embedding: List[float],
        context_sig: str
    ) -> Optional[ExperiencePattern]:
        """鏌ユ壘鐩镐技妯″紡"""
        # 绠€鍖栵細鍙鏌ュ搱甯屽尮閰?        embedding_hash = self._hash_embedding(embedding)
        
        if embedding_hash in self.by_hash:
            pattern_id = self.by_hash[embedding_hash]
            if pattern_id in self.cache:
                return self.cache[pattern_id]
        
        return None
    
    def _hash_embedding(self, embedding: List[float]) -> str:
        """璁＄畻宓屽叆鍝堝笇"""
        # 绠€鍖栵細浣跨敤 quantized 鍝堝笇
        arr = np.array(embedding)
        quantized = np.digitize(arr, bins=np.linspace(-3, 3, 10))
        return hash(tuple(quantized)) & 0xFFFFFFFF
    
    def _context_signature(self, context: Dict[str, Any]) -> str:
        """鐢熸垚涓婁笅鏂囩鍚?""
        # 绠€鍖栵細浣跨敤浠诲姟绫诲瀷浣滀负绛惧悕
        return context.get('task', 'unknown')
    
    def get_patterns(self, limit: int = 100) -> List[ExperiencePattern]:
        """鑾峰彇鎵€鏈夋ā寮?""
        return list(self.cache.values())[:limit]
    
    def get_stats(self) -> Dict[str, Any]:
        """鑾峰彇缁熻"""
        if not self.cache:
            return {
                'pattern_count': 0,
                'cache_usage': 0.0,
                'avg_success_rate': 0.0,
                'avg_value': 0.0
            }
        
        patterns = list(self.cache.values())
        total = sum(p.success_count + p.failure_count for p in patterns)
        successes = sum(p.success_count for p in patterns)
        total_value = sum(p.avg_value for p in patterns)
        
        return {
            'pattern_count': len(patterns),
            'cache_usage': len(patterns) / self.capacity,
            'avg_success_rate': successes / total if total > 0 else 0.0,
            'avg_value': total_value / len(patterns) if patterns else 0.0
        }
    
    def clear(self):
        """娓呯┖缂撳瓨"""
        self.cache.clear()
        self.by_hash.clear()
        self.by_context.clear()


# 娴嬭瘯
if __name__ == '__main__':
    replay = ExperienceReplay(capacity=100)
    
    # 娣诲姞娴嬭瘯缁忛獙
    import random
    for i in range(10):
        embedding = [random.gauss(0, 1) for _ in range(128)]
        context = {'task': 'test', 'difficulty': random.randint(1, 5)}
        success = random.choice([True, False])
        value = random.uniform(0, 1)
        
        replay.add(embedding, context, success, value)
    
    # 鏌ヨ
    test_embedding = [random.gauss(0, 1) for _ in range(128)]
    result = replay.query(test_embedding, {'task': 'test'})
    
    print(f"鏌ヨ缁撴灉锛歿result}")
    print(f"缁熻锛歿replay.get_stats()}")
