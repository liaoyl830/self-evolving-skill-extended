"""
娈嬪樊閲戝瓧濉斿垎瑙ｆā鍧?
浣跨敤 SVD 鍒嗚В灏嗗祵鍏ュ悜閲忓垎瑙ｄ负澶氬眰鎶借薄锛岃瘑鍒鐭ョ己鍙?"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class PyramidLayer:
    """閲戝瓧濉斿眰"""
    level: int  # 灞傜骇 (0=鏈€楂樻娊璞?
    energy: float  # 鑳介噺
    components: np.ndarray  # 涓绘垚鍒?    coverage: float  # 瑕嗙洊鐜?

@dataclass
class DecompositionResult:
    """鍒嗚В缁撴灉"""
    total_energy: float
    residual_ratio: float  # 娈嬪樊姣旂巼
    layers: List[PyramidLayer]
    suggested_abstraction: str  # POLICY | SUB_SKILL | PREDICATE
    novelty_score: float  # 鏂伴鎬ц瘎鍒?

class ResidualPyramid:
    """娈嬪樊閲戝瓧濉斿垎瑙ｅ櫒"""
    
    ABSTRACTION_LEVELS = ['POLICY', 'SUB_SKILL', 'PREDICATE']
    
    def __init__(self, max_layers: int = 5, use_pca: bool = True):
        """
        鍒濆鍖栭噾瀛楀鍒嗚В鍣?        
        Args:
            max_layers: 鏈€澶у眰鏁?            use_pca: 鏄惁浣跨敤 PCA 闄嶇淮
        """
        self.max_layers = max_layers
        self.use_pca = use_pca
        
    def decompose(self, embedding: List[float]) -> DecompositionResult:
        """
        鍒嗚В宓屽叆鍚戦噺
        
        Args:
            embedding: 杈撳叆宓屽叆鍚戦噺
            
        Returns:
            DecompositionResult: 鍒嗚В缁撴灉
        """
        # 杞崲涓?numpy 鏁扮粍
        x = np.array(embedding, dtype=np.float64)
        
        # 璁＄畻鎬昏兘閲?        total_energy = np.sum(x ** 2)
        
        if total_energy < 1e-10:
            return DecompositionResult(
                total_energy=0.0,
                residual_ratio=1.0,
                layers=[],
                suggested_abstraction='PREDICATE',
                novelty_score=1.0
            )
        
        # 鏋勫缓閲戝瓧濉?        layers = self._build_pyramid(x, total_energy)
        
        # 璁＄畻娈嬪樊
        residual = self._compute_residual(x, layers)
        residual_ratio = np.sum(residual ** 2) / total_energy
        
        # 纭畾寤鸿鐨勬娊璞″眰绾?        coverage = 1.0 - residual_ratio
        suggested_abstraction = self._suggest_abstraction(coverage)
        
        # 璁＄畻鏂伴鎬ц瘎鍒?        novelty_score = self._compute_novelty(residual_ratio, len(layers))
        
        return DecompositionResult(
            total_energy=total_energy,
            residual_ratio=residual_ratio,
            layers=layers,
            suggested_abstraction=suggested_abstraction,
            novelty_score=novelty_score
        )
    
    def _build_pyramid(self, x: np.ndarray, total_energy: float) -> List[PyramidLayer]:
        """鏋勫缓閲戝瓧濉斿眰绾?""
        layers = []
        remaining = x.copy()
        
        for level in range(self.max_layers):
            # 褰撳墠灞傝兘閲忛槇鍊?            threshold = 0.8 ** level
            
            if np.sum(remaining ** 2) < threshold * total_energy * 0.1:
                break
            
            # SVD 鍒嗚В锛堢畝鍖栦负鍗曞悜閲忥級
            if self.use_pca and len(remaining) > 1:
                # PCA: 鍙栦富鎴愬垎
                components = self._extract_principal_component(remaining)
            else:
                components = remaining.copy()
            
            # 褰掍竴鍖?            norm = np.linalg.norm(components)
            if norm > 1e-10:
                components = components / norm
            
            # 璁＄畻璇ュ眰鑳介噺
            energy = np.sum(components ** 2)
            coverage = energy / total_energy if total_energy > 0 else 0
            
            layers.append(PyramidLayer(
                level=level,
                energy=energy,
                components=components,
                coverage=coverage
            ))
            
            # 鍑忓幓璇ュ眰璐＄尞
            remaining = remaining - components * np.dot(remaining, components)
        
        return layers
    
    def _extract_principal_component(self, x: np.ndarray) -> np.ndarray:
        """鎻愬彇涓绘垚鍒嗭紙绠€鍖?PCA锛?""
        # 瀵逛簬鍗曞悜閲忥紝涓绘垚鍒嗗氨鏄嚜韬柟鍚?        return x.copy()
    
    def _compute_residual(self, x: np.ndarray, layers: List[PyramidLayer]) -> np.ndarray:
        """璁＄畻娈嬪樊"""
        residual = x.copy()
        for layer in layers:
            residual = residual - layer.components * np.dot(residual, layer.components)
        return residual
    
    def _suggest_abstraction(self, coverage: float) -> str:
        """鏍规嵁瑕嗙洊鐜囧缓璁娊璞″眰绾?""
        if coverage > 0.8:
            return 'POLICY'  # 楂樿鐩栫巼锛岃皟鏁寸瓥鐣?        elif coverage > 0.4:
            return 'SUB_SKILL'  # 涓瓑瑕嗙洊鐜囷紝鐢熸垚瀛愭妧鑳?        else:
            return 'PREDICATE'  # 浣庤鐩栫巼锛屽綊绾虫柊璋撹瘝
    
    def _compute_novelty(self, residual_ratio: float, layers_count: int) -> float:
        """璁＄畻鏂伴鎬ц瘎鍒?""
        # 娈嬪樊瓒婇珮锛屾柊棰栨€ц秺楂?        # 灞傛暟瓒婂皯锛屾柊棰栨€ц秺楂?        novelty = 0.6 * residual_ratio + 0.4 * (1.0 - layers_count / self.max_layers)
        return min(1.0, max(0.0, novelty))


# 娴嬭瘯
if __name__ == '__main__':
    # 鍒涘缓娴嬭瘯宓屽叆
    test_embedding = np.random.randn(128).tolist()
    
    pyramid = ResidualPyramid(max_layers=5)
    result = pyramid.decompose(test_embedding)
    
    print(f"鎬昏兘閲忥細{result.total_energy:.4f}")
    print(f"娈嬪樊姣旂巼锛歿result.residual_ratio:.4f}")
    print(f"寤鸿鎶借薄锛歿result.suggested_abstraction}")
    print(f"鏂伴鎬ц瘎鍒嗭細{result.novelty_score:.4f}")
    print(f"灞傛暟锛歿len(result.layers)}")
