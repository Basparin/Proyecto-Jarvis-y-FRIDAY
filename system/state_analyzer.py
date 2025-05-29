
"""
STARK INDUSTRIES - System State Analyzer
Análisis técnico eficiente del estado del sistema para AI
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class StarkStateAnalyzer:
    """Analizador técnico del estado del sistema STARK"""
    
    def __init__(self, workspace_path: str = None):
        if workspace_path is None:
            workspace_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.workspace_path = workspace_path
        self.state_file = os.path.join(workspace_path, "STARK_SYSTEM_STATE.json")
        self.progress_file = os.path.join(workspace_path, "STARK_PROGRESS.md")
    
    def load_system_state(self) -> Dict[str, Any]:
        """Carga el estado actual del sistema"""
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Could not load system state: {e}"}
    
    def get_quick_status(self) -> Dict[str, Any]:
        """Obtiene un resumen rápido del estado del sistema"""
        state = self.load_system_state()
        if "error" in state:
            return state
        
        return {
            "system_operational": state.get("meta", {}).get("status") == "FULLY_OPERATIONAL",
            "total_modules": len(state.get("modules", {})),
            "active_modules": sum(1 for module in state.get("modules", {}).values() 
                                if module.get("status") == "ACTIVE"),
            "ai_personalities_active": len([ai for ai in state.get("ai_personalities", {}).values() 
                                          if ai.get("status") == "OPERATIONAL"]),
            "mock_components_ratio": self._calculate_mock_ratio(state),
            "critical_issues": self._identify_critical_issues(state),
            "next_priorities": state.get("optimization_opportunities", [])[:3]
        }
    
    def get_module_analysis(self) -> Dict[str, Any]:
        """Análisis detallado de módulos"""
        state = self.load_system_state()
        modules = state.get("modules", {})
        
        analysis = {}
        for module_name, module_data in modules.items():
            components = module_data.get("components", {})
            mock_count = sum(1 for status in components.values() 
                           if status in ["MOCK", "PENDING"])
            total_count = len(components)
            
            analysis[module_name] = {
                "status": module_data.get("status"),
                "completion_ratio": (total_count - mock_count) / total_count if total_count > 0 else 0,
                "mock_components": mock_count,
                "total_components": total_count,
                "capabilities": module_data.get("capabilities", []),
                "test_status": "PASSED" if all(status == "PASSED" 
                                             for status in module_data.get("tests", {}).values()) else "ISSUES"
            }
        
        return analysis
    
    def get_ai_coordination_status(self) -> Dict[str, Any]:
        """Estado de coordinación de las personalidades AI"""
        state = self.load_system_state()
        ai_personalities = state.get("ai_personalities", {})
        
        return {
            "jarvis": {
                "active": ai_personalities.get("jarvis", {}).get("status") == "OPERATIONAL",
                "traits": ai_personalities.get("jarvis", {}).get("personality_traits", []),
                "independence": ai_personalities.get("jarvis", {}).get("independence")
            },
            "friday": {
                "active": ai_personalities.get("friday", {}).get("status") == "OPERATIONAL",
                "traits": ai_personalities.get("friday", {}).get("personality_traits", []),
                "independence": ai_personalities.get("friday", {}).get("independence")
            },
            "copilot": {
                "active": ai_personalities.get("copilot", {}).get("status") == "OPERATIONAL",
                "traits": ai_personalities.get("copilot", {}).get("personality_traits", []),
                "independence": ai_personalities.get("copilot", {}).get("independence")
            },
            "coordination_active": all(ai.get("coordination") == "ACTIVE" 
                                     for ai in ai_personalities.values())
        }
    
    def get_development_priorities(self) -> Dict[str, List[str]]:
        """Prioridades de desarrollo actuales"""
        state = self.load_system_state()
        
        return {
            "immediate": [
                "Replace mock neural network with real implementation",
                "Implement persistent memory system",
                "Add real computer vision capabilities"
            ],
            "short_term": [
                "Voice synthesis integration",
                "External API connections", 
                "Advanced learning algorithms"
            ],
            "long_term": [
                "GUI dashboard interfaces",
                "Advanced AI coordination",
                "Production deployment"
            ]
        }
    
    def _calculate_mock_ratio(self, state: Dict[str, Any]) -> float:
        """Calcula el ratio de componentes mock vs reales"""
        modules = state.get("modules", {})
        total_components = 0
        mock_components = 0
        
        for module_data in modules.values():
            components = module_data.get("components", {})
            total_components += len(components)
            mock_components += sum(1 for status in components.values() 
                                 if status in ["MOCK", "PENDING"])
        
        return mock_components / total_components if total_components > 0 else 0
    
    def _identify_critical_issues(self, state: Dict[str, Any]) -> List[str]:
        """Identifica problemas críticos del sistema"""
        issues = []
        
        # Verificar módulos inactivos
        modules = state.get("modules", {})
        for module_name, module_data in modules.items():
            if module_data.get("status") != "ACTIVE":
                issues.append(f"Module {module_name} not active")
        
        # Verificar AI personalities
        ai_personalities = state.get("ai_personalities", {})
        for ai_name, ai_data in ai_personalities.items():
            if ai_data.get("status") != "OPERATIONAL":
                issues.append(f"AI {ai_name} not operational")
        
        # Verificar mock ratio crítico
        mock_ratio = self._calculate_mock_ratio(state)
        if mock_ratio > 0.8:
            issues.append("High mock component ratio - needs real implementations")
        
        return issues
    
    def update_state_timestamp(self):
        """Actualiza el timestamp del estado del sistema"""
        try:
            state = self.load_system_state()
            if "error" not in state:
                state["meta"]["last_update"] = datetime.now().isoformat() + "Z"
                with open(self.state_file, 'w', encoding='utf-8') as f:
                    json.dump(state, f, indent=2, ensure_ascii=False)
                return True
        except Exception:
            pass
        return False
    
    def generate_technical_summary(self) -> str:
        """Genera un resumen técnico para AI analysis"""
        quick_status = self.get_quick_status()
        module_analysis = self.get_module_analysis()
        ai_status = self.get_ai_coordination_status()
        
        summary = f"""
STARK SYSTEM TECHNICAL SUMMARY
==============================

SYSTEM STATUS: {'OPERATIONAL' if quick_status.get('system_operational') else 'ISSUES'}
Active Modules: {quick_status.get('active_modules')}/{quick_status.get('total_modules')}
AI Personalities: {quick_status.get('ai_personalities_active')}/3 active
Mock Component Ratio: {quick_status.get('mock_components_ratio', 0):.1%}

MODULE ANALYSIS:
{self._format_module_analysis(module_analysis)}

AI COORDINATION:
JARVIS: {'✓' if ai_status['jarvis']['active'] else '✗'} - {', '.join(ai_status['jarvis']['traits'])}
FRIDAY: {'✓' if ai_status['friday']['active'] else '✗'} - {', '.join(ai_status['friday']['traits'])}  
COPILOT: {'✓' if ai_status['copilot']['active'] else '✗'} - {', '.join(ai_status['copilot']['traits'])}

CRITICAL ISSUES:
{chr(10).join('- ' + issue for issue in quick_status.get('critical_issues', []))}

NEXT PRIORITIES:
{chr(10).join('- ' + priority for priority in quick_status.get('next_priorities', []))}
"""
        return summary
    
    def _format_module_analysis(self, analysis: Dict[str, Any]) -> str:
        """Formatea el análisis de módulos"""
        formatted = []
        for module_name, data in analysis.items():
            status_icon = "✓" if data['status'] == 'ACTIVE' else "✗"
            completion = f"{data['completion_ratio']:.0%}"
            formatted.append(f"{module_name.upper()}: {status_icon} {completion} complete")
        return "\n".join(formatted)

# Función de utilidad para uso rápido
def analyze_stark_system(workspace_path: str = None) -> Dict[str, Any]:
    """Función de análisis rápido del sistema STARK"""
    analyzer = StarkStateAnalyzer(workspace_path)
    return {
        "quick_status": analyzer.get_quick_status(),
        "module_analysis": analyzer.get_module_analysis(),
        "ai_status": analyzer.get_ai_coordination_status(),
        "priorities": analyzer.get_development_priorities(),
        "technical_summary": analyzer.generate_technical_summary()
    }

if __name__ == "__main__":
    # Test del analizador
    analyzer = StarkStateAnalyzer()
    print(analyzer.generate_technical_summary())
