#!/usr/bin/env python3
"""
MCP 鏈嶅姟鍣?
鎻愪緵 HTTP 鎺ュ彛渚?TypeScript 璋冪敤
"""

import sys
import json
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from typing import Dict, Any
from pathlib import Path

# 娣诲姞鏍稿績妯″潡璺緞
CORE_DIR = Path(__file__).parent
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from skill_engine import SelfEvolvingSkillEngine


class MCPHandler(BaseHTTPRequestHandler):
    """MCP 璇锋眰澶勭悊鍣?""
    
    engine: SelfEvolvingSkillEngine = None
    
    def log_message(self, format, *args):
        """鑷畾涔夋棩蹇?""
        print(f"[MCP] {args[0]}")
    
    def do_POST(self):
        """澶勭悊 POST 璇锋眰"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            request = json.loads(body)
            tool = request.get('tool')
            arguments = request.get('arguments', {})
            
            print(f"[MCP] 璋冪敤宸ュ叿锛歿tool}")
            
            result = self.call_tool(tool, arguments)
            
            response = {
                'success': True,
                'result': result
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            print(f"[MCP] 閿欒锛歿e}")
            self.send_error(500, str(e))
    
    def call_tool(self, tool: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """璋冪敤宸ュ叿"""
        if tool == 'skill_create':
            return self.tool_create(args)
        elif tool == 'skill_execute':
            return self.tool_execute(args)
        elif tool == 'skill_analyze':
            return self.tool_analyze(args)
        elif tool == 'skill_list':
            return self.tool_list(args)
        elif tool == 'skill_stats':
            return self.tool_stats(args)
        elif tool == 'skill_save':
            return self.tool_save(args)
        elif tool == 'skill_load':
            return self.tool_load(args)
        else:
            raise ValueError(f"鏈煡宸ュ叿锛歿tool}")
    
    def tool_create(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """鍒涘缓鎶€鑳?""
        name = args.get('name', 'Unnamed')
        description = args.get('description', '')
        
        skill = self.engine.create_skill(name, description)
        
        return {
            'skill_id': skill.id,
            'name': skill.name,
            'description': skill.description,
            'created_at': skill.created_at
        }
    
    def tool_execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """鎵ц鎶€鑳?""
        skill_id = args.get('skill_id')
        context = args.get('context', {})
        embedding = args.get('embedding')
        success = args.get('success', True)
        value = args.get('value_realization', 1.0)
        
        result = self.engine.execute(
            skill_id=skill_id,
            context=context,
            embedding=embedding,
            success=success,
            value=value
        )
        
        return {
            'success': result.success,
            'executed': result.executed,
            'reflection_triggered': result.reflection_triggered,
            'mutation_accepted': result.mutation_accepted,
            'trigger_reason': result.trigger_result.reason if result.trigger_result else None
        }
    
    def tool_analyze(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """鍒嗘瀽宓屽叆"""
        embedding = args.get('embedding', [])
        
        result = self.engine.analyze(embedding)
        
        return {
            'total_energy': result.total_energy,
            'residual_ratio': result.residual_ratio,
            'layers_count': len(result.layers),
            'suggested_abstraction': result.suggested_abstraction,
            'novelty_score': result.novelty_score,
            'would_trigger_reflection': result.residual_ratio >= 0.10
        }
    
    def tool_list(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """鍒楀嚭鎶€鑳?""
        skills = self.engine.list_skills()
        
        return {
            'skills': [
                {
                    'id': s.id,
                    'name': s.name,
                    'description': s.description,
                    'execution_count': s.execution_count,
                    'success_rate': s.success_count / max(1, s.execution_count)
                }
                for s in skills
            ],
            'total': len(skills)
        }
    
    def tool_stats(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """鑾峰彇缁熻"""
        return self.engine.get_stats()
    
    def tool_save(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """淇濆瓨鎶€鑳?""
        skill_id = args.get('skill_id')
        success = self.engine.save(skill_id)
        
        return {'saved': success}
    
    def tool_load(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """鍔犺浇鎶€鑳?""
        skill_id = args.get('skill_id')
        skill = self.engine.load(skill_id)
        
        if skill:
            return {
                'id': skill.id,
                'name': skill.name,
                'description': skill.description,
                'execution_count': skill.execution_count
            }
        else:
            return {'error': 'Skill not found'}


def main():
    parser = argparse.ArgumentParser(description='Self-Evolving Skill MCP Server')
    parser.add_argument('--port', type=int, default=8080, help='鏈嶅姟绔彛')
    parser.add_argument('--storage', type=str, default=None, help='瀛樺偍鐩綍')
    args = parser.parse_args()
    
    # 鍒濆鍖栧紩鎿?    print(f"[MCP Server] 鍒濆鍖栧紩鎿?..")
    MCPHandler.engine = SelfEvolvingSkillEngine(storage_dir=args.storage)
    
    # 鍚姩鏈嶅姟鍣?    server = HTTPServer(('localhost', args.port), MCPHandler)
    print(f"[MCP Server] 鍚姩浜?http://localhost:{args.port}")
    print(f"[MCP Server] 鎸?Ctrl+C 鍋滄")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[MCP Server] 鍋滄鏈嶅姟")
        server.shutdown()


if __name__ == '__main__':
    main()
