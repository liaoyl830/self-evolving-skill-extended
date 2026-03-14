#!/usr/bin/env python3
"""
McPorter Adapter for Self-Evolving Skill

鎻愪緵绗﹀悎 mcporter 璋冪敤鏍煎紡鐨勯€傞厤鍣?鏀寔 sessions_yield 寮傛澶嶇洏
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any

# 娣诲姞鏍稿績妯″潡璺緞
CORE_DIR = os.path.join(os.path.dirname(__file__), 'core')
if CORE_DIR not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

# 鍒濆鍖栧紩鎿?_engine = None

def get_engine():
    global _engine
    if _engine is None:
        from skill_engine import SelfEvolvingSkillEngine
        storage_dir = os.environ.get(
            'MCP_STORAGE_DIR',
            os.path.join(os.environ.get('APPDATA', ''), '.openclaw', 'self-evolving-skill', 'storage')
        )
        _engine = SelfEvolvingSkillEngine(storage_dir=storage_dir)
    return _engine


def get_review_agent():
    """鑾峰彇澶嶇洏浠ｇ悊"""
    from review_background_agent import ReviewBackgroundAgent
    return ReviewBackgroundAgent()


def get_yield_adapter():
    """鑾峰彇 sessions_yield 閫傞厤鍣?""
    from sessions_yield_adapter import SessionsYieldAdapter
    return SessionsYieldAdapter()


def skill_create(args: Dict[str, Any]) -> str:
    """鍒涘缓 Skill"""
    engine = get_engine()
    name = args.get('name', 'Unnamed')
    description = args.get('description', '')
    
    skill = engine.create_skill(name, description)
    
    return json.dumps({
        'success': True,
        'skill_id': skill.id,
        'name': skill.name,
        'description': skill.description
    })


def skill_execute(args: Dict[str, Any]) -> str:
    """鎵ц Skill"""
    engine = get_engine()
    skill_id = args.get('skill_id')
    context = args.get('context', {})
    embedding = args.get('embedding')
    success = args.get('success', True)
    value = args.get('value_realization', 1.0)
    
    result = engine.execute(
        skill_id=skill_id,
        context=context,
        embedding=embedding,
        success=success,
        value=value
    )
    
    return json.dumps({
        'success': result.success,
        'executed': result.executed,
        'reflection_triggered': result.reflection_triggered,
        'mutation_accepted': result.mutation_accepted
    })


def skill_analyze(args: Dict[str, Any]) -> str:
    """鍒嗘瀽宓屽叆"""
    engine = get_engine()
    embedding = args.get('embedding', [])
    
    result = engine.analyze(embedding)
    
    return json.dumps({
        'total_energy': result.total_energy,
        'residual_ratio': result.residual_ratio,
        'layers_count': len(result.layers),
        'suggested_abstraction': result.suggested_abstraction,
        'novelty_score': result.novelty_score
    })


def skill_list(args: Dict[str, Any]) -> str:
    """鍒楀嚭 Skills"""
    engine = get_engine()
    skills = engine.list_skills()
    
    return json.dumps({
        'skills': [
            {
                'id': s.id,
                'name': s.name,
                'description': s.description,
                'execution_count': s.execution_count
            }
            for s in skills
        ],
        'total': len(skills)
    })


def skill_stats(args: Dict[str, Any]) -> str:
    """绯荤粺缁熻"""
    engine = get_engine()
    stats = engine.get_stats()
    
    return json.dumps(stats)


def skill_save(args: Dict[str, Any]) -> str:
    """淇濆瓨 Skill"""
    engine = get_engine()
    skill_id = args.get('skill_id')
    success = engine.save(skill_id)
    
    return json.dumps({'saved': success})


def skill_load(args: Dict[str, Any]) -> str:
    """鍔犺浇 Skill"""
    engine = get_engine()
    skill_id = args.get('skill_id')
    skill = engine.load(skill_id)
    
    if skill:
        return json.dumps({
            'id': skill.id,
            'name': skill.name,
            'description': skill.description,
            'execution_count': skill.execution_count
        })
    else:
        return json.dumps({'error': 'Skill not found'})


def skill_review_async(args: Dict[str, Any]) -> str:
    """
    寮傛澶嶇洏锛堜娇鐢?sessions_yield锛?    
    绔嬪嵆杩斿洖锛屽悗鍙版墽琛?    """
    adapter = get_yield_adapter()
    context = args.get('context', {})
    
    result = adapter.start_background_review(context)
    
    return json.dumps(result)


def skill_review_sync(args: Dict[str, Any]) -> str:
    """
    鍚屾澶嶇洏锛堥檷绾ф柟妗堬級
    """
    agent = get_review_agent()
    context = args.get('context', {})
    
    result = agent.execute_review(context)
    
    # 纭繚鎵€鏈夊€奸兘鏄?JSON 鍙簭鍒楀寲鐨?    def make_serializable(obj):
        if isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_serializable(v) for v in obj]
        elif isinstance(obj, (bool,)):
            return bool(obj)
        elif isinstance(obj, (int,)):
            return int(obj)
        elif isinstance(obj, (float,)):
            return float(obj)
        else:
            return obj
    
    serializable_result = make_serializable(result)
    return json.dumps(serializable_result, ensure_ascii=False)


# 涓诲叆鍙?if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("鐢ㄦ硶锛歱ython mcporter_adapter.py <tool_name> '<args_json>'")
        sys.exit(1)
    
    tool_name = sys.argv[1]
    args_json = sys.argv[2] if len(sys.argv) > 2 else '{}'
    
    try:
        args = json.loads(args_json)
    except json.JSONDecodeError:
        print(json.dumps({'error': 'Invalid JSON'}))
        sys.exit(1)
    
    tools = {
        'skill_create': skill_create,
        'skill_execute': skill_execute,
        'skill_analyze': skill_analyze,
        'skill_list': skill_list,
        'skill_stats': skill_stats,
        'skill_save': skill_save,
        'skill_load': skill_load,
        'skill_review_async': skill_review_async,
        'skill_review_sync': skill_review_sync
    }
    
    if tool_name not in tools:
        print(json.dumps({'error': f'Unknown tool: {tool_name}'}))
        sys.exit(1)
    
    result = tools[tool_name](args)
    print(result)
