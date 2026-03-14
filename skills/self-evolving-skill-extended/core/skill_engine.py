"""
鑷紨鍖栨妧鑳芥牳蹇冨紩鎿?
鏁村悎鎵€鏈夋ā鍧楋紝鎻愪緵缁熶竴鐨勬妧鑳藉涔犲拰鎵ц鎺ュ彛
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import uuid

# 娣诲姞鏍稿績妯″潡璺緞
CORE_DIR = Path(__file__).parent
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from residual_pyramid import ResidualPyramid, DecompositionResult
from reflection_trigger import ReflectionTrigger, TriggerResult
from experience_replay import ExperienceReplay, ExperiencePattern
from storage import SkillStorage, Skill, Experience


@dataclass
class ExecutionResult:
    """鎵ц缁撴灉"""
    success: bool
    skill_id: str
    executed: bool
    reflection_triggered: bool = False
    mutation_accepted: bool = False
    trigger_result: Optional[TriggerResult] = None
    decomposition: Optional[DecompositionResult] = None


class SelfEvolvingSkillEngine:
    """鑷紨鍖栨妧鑳藉紩鎿?""
    
    def __init__(self, storage_dir: Optional[str] = None):
        """
        鍒濆鍖栧紩鎿?        
        Args:
            storage_dir: 瀛樺偍鐩綍
        """
        # 榛樿瀛樺偍鐩綍
        if storage_dir is None:
            appdata = os.environ.get('APPDATA', os.environ.get('HOME', ''))
            storage_dir = os.path.join(appdata, '.openclaw', 'self-evolving-skill', 'storage')
        
        # 鍒濆鍖栨ā鍧?        self.storage = SkillStorage(storage_dir)
        self.pyramid = ResidualPyramid(max_layers=5, use_pca=True)
        self.trigger = ReflectionTrigger(
            min_energy_ratio=0.10,
            value_gain_threshold=0.20,
            target_trigger_rate=0.15
        )
        self.replay = ExperienceReplay(capacity=1000, similarity_threshold=0.85)
        
        # 鎶€鑳藉簱
        self.skill_library: Dict[str, Skill] = self.storage.skills.copy()
        
        print(f"[SkillEngine] 鍒濆鍖栧畬鎴愶紝瀛樺偍鐩綍锛歿storage_dir}")
        print(f"[SkillEngine] 宸插姞杞?{len(self.skill_library)} 涓妧鑳?)
    
    def create_skill(self, name: str, description: str = "") -> Skill:
        """
        鍒涘缓鏂版妧鑳?        
        Args:
            name: 鎶€鑳藉悕绉?            description: 鎶€鑳芥弿杩?            
        Returns:
            Skill: 鍒涘缓鐨勬妧鑳?        """
        skill_id = f"skill_{int(datetime.now().timestamp() * 1000)}"
        
        skill = Skill(
            id=skill_id,
            name=name,
            description=description,
            created_at=datetime.now().isoformat()
        )
        
        self.skill_library[skill_id] = skill
        self.storage.save_skill(skill)
        
        print(f"[SkillEngine] 鍒涘缓鎶€鑳斤細{skill_id} - {name}")
        return skill
    
    def execute(
        self,
        skill_id: str,
        context: Dict[str, Any],
        embedding: Optional[List[float]] = None,
        success: bool = True,
        value: float = 1.0
    ) -> ExecutionResult:
        """
        鎵ц鎶€鑳藉苟瑙﹀彂瀛︿範
        
        Args:
            skill_id: 鎶€鑳?ID
            context: 鎵ц涓婁笅鏂?            embedding: 宓屽叆鍚戦噺 (鍙€?
            success: 鏄惁鎴愬姛
            value: 浠峰€煎疄鐜板害
            
        Returns:
            ExecutionResult: 鎵ц缁撴灉
        """
        # 妫€鏌ユ妧鑳藉瓨鍦?        if skill_id not in self.skill_library:
            print(f"[SkillEngine] 鎶€鑳戒笉瀛樺湪锛歿skill_id}")
            return ExecutionResult(
                success=False,
                skill_id=skill_id,
                executed=False
            )
        
        skill = self.skill_library[skill_id]
        
        # 鍒嗚В宓屽叆 (濡傛灉鏈?
        decomposition = None
        if embedding:
            decomposition = self.pyramid.decompose(embedding)
        
        # 妫€鏌ユ槸鍚﹁Е鍙戝弽鎬?        trigger_result = None
        if decomposition:
            value_gain = value - skill.total_value / max(1, skill.execution_count)
            
            trigger_result = self.trigger.check(
                residual_ratio=decomposition.residual_ratio,
                value_gain=value_gain,
                suggested_abstraction=decomposition.suggested_abstraction
            )
        
        # 娣诲姞鍒扮粡楠屽洖鏀?        if embedding:
            self.replay.add(
                embedding=embedding,
                context=context,
                success=success,
                value=value
            )
        
        # 淇濆瓨缁忛獙
        experience = Experience(
            skill_id=skill_id,
            timestamp=datetime.now().isoformat(),
            success=success,
            value=value,
            context=context,
            embedding=embedding,
            reflection_triggered=trigger_result.should_trigger if trigger_result else False,
            mutation_accepted=False  # 绠€鍖栵細鏆備笉瀹炵幇鍙樺紓
        )
        
        self.storage.add_experience(experience)
        
        # 鏇存柊鎶€鑳界粺璁?        skill.execution_count += 1
        if success:
            skill.success_count += 1
        skill.total_value += value
        
        self.storage.save_skill(skill)
        
        result = ExecutionResult(
            success=True,
            skill_id=skill_id,
            executed=True,
            reflection_triggered=trigger_result.should_trigger if trigger_result else False,
            mutation_accepted=False,
            trigger_result=trigger_result,
            decomposition=decomposition
        )
        
        if trigger_result and trigger_result.should_trigger:
            print(f"[SkillEngine] 瑙﹀彂鍙嶆€濓細{trigger_result.reason}")
        
        return result
    
    def analyze(self, embedding: List[float]) -> DecompositionResult:
        """
        鍒嗘瀽宓屽叆鍚戦噺
        
        Args:
            embedding: 宓屽叆鍚戦噺
            
        Returns:
            DecompositionResult: 鍒嗚В缁撴灉
        """
        return self.pyramid.decompose(embedding)
    
    def list_skills(self) -> List[Skill]:
        """鍒楀嚭鎵€鏈夋妧鑳?""
        return list(self.skill_library.values())
    
    def get_stats(self) -> Dict[str, Any]:
        """鑾峰彇绯荤粺缁熻"""
        return {
            'skills_count': len(self.skill_library),
            'experiences_count': len(self.storage.experiences),
            'storage_size_mb': self.storage._get_storage_size_mb(),
            'engine': {
                'total_executions': self.storage.stats['total_executions'],
                'total_reflections': self.storage.stats['total_reflections'],
                'total_mutations': self.storage.stats['total_mutations'],
                'value_gate_acceptance': self.storage.stats['value_gate_accepted']
            },
            'trigger': self.trigger.get_stats(),
            'replay': self.replay.get_stats()
        }
    
    def save(self, skill_id: str) -> bool:
        """淇濆瓨鎶€鑳?""
        if skill_id in self.skill_library:
            return self.storage.save_skill(self.skill_library[skill_id])
        return False
    
    def load(self, skill_id: str) -> Optional[Skill]:
        """鍔犺浇鎶€鑳?""
        return self.skill_library.get(skill_id)


# 娴嬭瘯
if __name__ == '__main__':
    engine = SelfEvolvingSkillEngine()
    
    # 鍒涘缓鎶€鑳?    skill = engine.create_skill("TestSkill", "娴嬭瘯鎶€鑳?)
    print(f"鍒涘缓鎶€鑳斤細{skill.id}")
    
    # 鎵ц
    result = engine.execute(
        skill_id=skill.id,
        context={'task': 'test'},
        embedding=[0.1] * 128,
        success=True,
        value=0.8
    )
    
    print(f"鎵ц缁撴灉锛歴uccess={result.success}, reflection={result.reflection_triggered}")
    
    # 缁熻
    stats = engine.get_stats()
    print(f"\n绯荤粺缁熻锛歿stats}")
