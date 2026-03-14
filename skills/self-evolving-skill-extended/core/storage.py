"""
鎸佷箙鍖栧瓨鍌ㄦā鍧?
绠＄悊鎶€鑳藉拰缁忛獙鐨勪繚瀛?鍔犺浇
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Skill:
    """鎶€鑳芥暟鎹粨鏋?""
    id: str
    name: str
    description: str
    created_at: str
    execution_count: int = 0
    success_count: int = 0
    total_value: float = 0.0
    policy: Optional[Dict] = None


@dataclass
class Experience:
    """缁忛獙鏁版嵁缁撴瀯"""
    skill_id: str
    timestamp: str
    success: bool
    value: float
    context: Dict[str, Any]
    embedding: Optional[List[float]] = None
    reflection_triggered: bool = False
    mutation_accepted: bool = False


class SkillStorage:
    """鎶€鑳芥寔涔呭寲瀛樺偍"""
    
    def __init__(self, storage_dir: str):
        """
        鍒濆鍖栧瓨鍌?        
        Args:
            storage_dir: 瀛樺偍鐩綍璺緞
        """
        self.storage_dir = Path(storage_dir)
        self.skills_file = self.storage_dir / 'skills.json'
        self.experiences_file = self.storage_dir / 'experiences.json'
        self.stats_file = self.storage_dir / 'stats.json'
        
        # 纭繚鐩綍瀛樺湪
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # 鍔犺浇鏁版嵁
        self.skills: Dict[str, Skill] = {}
        self.experiences: List[Experience] = []
        self.stats = {
            'total_executions': 0,
            'total_reflections': 0,
            'total_mutations': 0,
            'value_gate_accepted': 0
        }
        
        self._load_all()
    
    def _load_all(self):
        """鍔犺浇鎵€鏈夋暟鎹?""
        self._load_skills()
        self._load_experiences()
        self._load_stats()
    
    def _load_skills(self):
        """鍔犺浇鎶€鑳?""
        if self.skills_file.exists():
            try:
                with open(self.skills_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for skill_data in data.get('skills', []):
                        skill = Skill(**skill_data)
                        self.skills[skill.id] = skill
            except Exception as e:
                print(f"[Storage] 鍔犺浇鎶€鑳藉け璐ワ細{e}")
    
    def _load_experiences(self):
        """鍔犺浇缁忛獙"""
        if self.experiences_file.exists():
            try:
                with open(self.experiences_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.experiences = [Experience(**e) for e in data.get('experiences', [])]
            except Exception as e:
                print(f"[Storage] 鍔犺浇缁忛獙澶辫触锛歿e}")
    
    def _load_stats(self):
        """鍔犺浇缁熻"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    self.stats = json.load(f)
            except Exception as e:
                print(f"[Storage] 鍔犺浇缁熻澶辫触锛歿e}")
    
    def save_skill(self, skill: Skill) -> bool:
        """淇濆瓨鎶€鑳?""
        self.skills[skill.id] = skill
        return self._save_skills()
    
    def add_experience(self, experience: Experience) -> bool:
        """娣诲姞缁忛獙"""
        self.experiences.append(experience)
        
        # 鏇存柊鎶€鑳界粺璁?        if experience.skill_id in self.skills:
            skill = self.skills[experience.skill_id]
            skill.execution_count += 1
            if experience.success:
                skill.success_count += 1
            skill.total_value += experience.value
            
            self._save_skills()
        
        # 鏇存柊鍏ㄥ眬缁熻
        self.stats['total_executions'] += 1
        if experience.success:
            self.stats['value_gate_accepted'] += 1
        if experience.reflection_triggered:
            self.stats['total_reflections'] += 1
        if experience.mutation_accepted:
            self.stats['total_mutations'] += 1
        
        # 纭繚甯冨皵鍊艰浆鎹负鏁存暟
        self.stats['total_executions'] = int(self.stats['total_executions'])
        self.stats['total_reflections'] = int(self.stats['total_reflections'])
        self.stats['total_mutations'] = int(self.stats['total_mutations'])
        self.stats['value_gate_accepted'] = int(self.stats['value_gate_accepted'])
        
        self._save_stats()
        return self._save_experiences()
    
    def _save_skills(self) -> bool:
        """淇濆瓨鎶€鑳藉埌鏂囦欢"""
        try:
            data = {
                'skills': [asdict(s) for s in self.skills.values()],
                'updated_at': datetime.now().isoformat()
            }
            with open(self.skills_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[Storage] 淇濆瓨鎶€鑳藉け璐ワ細{e}")
            return False
    
    def _save_experiences(self) -> bool:
        """淇濆瓨缁忛獙鍒版枃浠?""
        try:
            data = {
                'experiences': [asdict(e) for e in self.experiences],
                'updated_at': datetime.now().isoformat()
            }
            with open(self.experiences_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[Storage] 淇濆瓨缁忛獙澶辫触锛歿e}")
            return False
    
    def _save_stats(self) -> bool:
        """淇濆瓨缁熻鍒版枃浠?""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2)
            return True
        except Exception as e:
            print(f"[Storage] 淇濆瓨缁熻澶辫触锛歿e}")
            return False
    
    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """鑾峰彇鎶€鑳?""
        return self.skills.get(skill_id)
    
    def list_skills(self) -> List[Skill]:
        """鍒楀嚭鎵€鏈夋妧鑳?""
        return list(self.skills.values())
    
    def get_experiences(self, skill_id: Optional[str] = None, limit: int = 100) -> List[Experience]:
        """鑾峰彇缁忛獙"""
        if skill_id:
            experiences = [e for e in self.experiences if e.skill_id == skill_id]
        else:
            experiences = self.experiences
        
        return experiences[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """鑾峰彇缁熻淇℃伅"""
        return {
            **self.stats,
            'skills_count': len(self.skills),
            'experiences_count': len(self.experiences),
            'storage_size_mb': self._get_storage_size_mb()
        }
    
    def _get_storage_size_mb(self) -> float:
        """鑾峰彇瀛樺偍澶у皬 (MB)"""
        total_size = 0
        for file in [self.skills_file, self.experiences_file, self.stats_file]:
            if file.exists():
                total_size += file.stat().st_size
        return total_size / (1024 * 1024)
    
    def clear_all(self):
        """娓呯┖鎵€鏈夋暟鎹?""
        self.skills.clear()
        self.experiences.clear()
        self.stats = {
            'total_executions': 0,
            'total_reflections': 0,
            'total_mutations': 0,
            'value_gate_accepted': 0
        }
        self._save_all()
    
    def _save_all(self):
        """淇濆瓨鎵€鏈夋暟鎹?""
        self._save_skills()
        self._save_experiences()
        self._save_stats()


# 娴嬭瘯
if __name__ == '__main__':
    storage = SkillStorage('./test_storage')
    
    # 鍒涘缓娴嬭瘯鎶€鑳?    skill = Skill(
        id='skill_test_001',
        name='TestSkill',
        description='娴嬭瘯鎶€鑳?,
        created_at=datetime.now().isoformat()
    )
    
    storage.save_skill(skill)
    print(f"淇濆瓨鎶€鑳斤細{skill.name}")
    
    # 娣诲姞缁忛獙
    exp = Experience(
        skill_id='skill_test_001',
        timestamp=datetime.now().isoformat(),
        success=True,
        value=0.8,
        context={'task': 'test'}
    )
    
    storage.add_experience(exp)
    print(f"娣诲姞缁忛獙锛歴uccess={exp.success}, value={exp.value}")
    
    # 鏄剧ず缁熻
    stats = storage.get_stats()
    print(f"\n缁熻锛歿json.dumps(stats, indent=2)}")
