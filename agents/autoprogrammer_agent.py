"""
JARVIS FRIDAY - Autoprogrammer Agent V2.0
Agente especializado en autoprogramación y conversión mock→real
Experto en implementación eficiente y optimización automática
Integrado con arquitectura modular avanzada
"""
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import os
import sys

# Asegurar que el workspace está en el path
workspace_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if workspace_path not in sys.path:
    sys.path.insert(0, workspace_path)

try:
    from agents.autoprogrammer_coordinator import AutoprogrammerCoordinator
except ImportError as e:
    print(f"⚠️ Error importando coordinador: {e}")
    AutoprogrammerCoordinator = None

class StarkAutoprogrammerAgent:
    """
    Agente principal de autoprogramación para sistema JARVIS-FRIDAY V2.0
    Coordina conversiones masivas mock→real con arquitectura modular
    """
    
    def __init__(self, workspace_path: str = None):
        if workspace_path is None:
            workspace_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.workspace_path = workspace_path
        self.version = "2.0.1"
        self.sub_agents = {}
        self.conversion_queue = []
        self.completed_tasks = []
        self.efficiency_metrics = {}
        
        print(f"🤖 JARVIS-FRIDAY AUTOPROGRAMMER AGENT V{self.version} - Inicializado")
        print("⚡ Arquitectura modular con sub-agentes especializados")
        print(f"📍 Workspace: {self.workspace_path}")
        
        self._initialize_sub_agents()
    
    def _initialize_sub_agents(self):
        """Inicializa sub-agentes especializados"""
        try:
            if AutoprogrammerCoordinator:
                self.sub_agents = {
                    "coordinator": AutoprogrammerCoordinator(self.workspace_path),
                    "analyzer": None,  # Se inicializará cuando sea necesario
                    "converter": None,
                    "optimizer": None
                }
                print("✅ Coordinador inicializado correctamente")
            else:
                print("⚠️ Coordinador no disponible, usando modo básico")
                self.sub_agents = {}
        except Exception as e:
            print(f"⚠️ Error inicializando sub-agentes: {e}")
            self.sub_agents = {}
    
    def _analyze_system_advanced(self):
        """Análisis avanzado del sistema con coordinador"""
        if "coordinator" in self.sub_agents and self.sub_agents["coordinator"]:
            try:
                return self.sub_agents["coordinator"].scan_mock_components()
            except Exception as e:
                print(f"⚠️ Error en análisis avanzado: {e}")
                return self._analyze_system_basic()
        return self._analyze_system_basic()
    
    def _analyze_system_basic(self):
        """Análisis básico del sistema sin coordinador"""
        # Estructura de módulos esperada
        modules_structure = {
            "neural": ["neural_network.py", "learning_engine.py", "memory_manager.py"],
            "perception": ["audio_processor.py", "sensor_integration.py", "pattern_recognition.py", "environment_monitor.py"],
            "communication": ["voice_synthesis.py", "natural_language.py", "protocol_manager.py", "interface_handler.py", "network_comm.py"],
            "agents": ["agent_coordinator.py", "decision_engine.py", "behavior_patterns.py"],
            "system": ["config_manager.py", "logger.py", "health_monitor.py"],
            "intelligence": ["decision_maker.py", "analytics_engine.py", "learning_system.py", "strategy_planner.py", "optimization_ai.py"]
        }
        
        mock_components = {"critical": [], "high": [], "medium": [], "low": []}
        
        for module_name, files in modules_structure.items():
            module_path = os.path.join(self.workspace_path, module_name)
            
            if not os.path.exists(module_path):
                continue
                
            for file_name in files:
                file_path = os.path.join(module_path, file_name)
                if os.path.exists(file_path):
                    if self._is_mock_implementation(file_path):
                        priority = self._determine_priority(module_name, file_name)
                        mock_components[priority].append({
                            "file": f"{module_name}/{file_name}",
                            "path": file_path,
                            "type": module_name,
                            "priority": priority.upper()
                        })
        
        return mock_components
    
    def _is_mock_implementation(self, file_path: str) -> bool:
        """Verifica si un archivo contiene implementación mock"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Indicadores de implementación mock
            mock_indicators = [
                "pass  # TODO",
                "# Mock implementation", 
                "raise NotImplementedError",
                "return None  # Mock",
                "# Placeholder",
                "TODO: Implement"
            ]
            
            # Si es muy pequeño y solo tiene pass, probablemente es mock
            if len(content.strip()) < 100 and "pass" in content:
                return True
                
            return any(indicator in content for indicator in mock_indicators)
        except:
            return True
    
    def _determine_priority(self, module_name: str, file_name: str) -> str:
        """Determina la prioridad de conversión"""
        critical_files = ["neural_network.py", "decision_maker.py", "voice_synthesis.py"]
        high_files = ["learning_engine.py", "natural_language.py", "analytics_engine.py"]
        
        if file_name in critical_files:
            return "critical"
        elif file_name in high_files:
            return "high"
        elif module_name in ["neural", "intelligence"]:
            return "medium"
        else:
            return "low"
    
    def _analyze_system(self):
        """Análisis principal del sistema"""
        print("\n📊 ANÁLISIS AVANZADO DEL SISTEMA...")
        
        if "coordinator" in self.sub_agents and self.sub_agents["coordinator"]:
            print("✅ Usando análisis avanzado con coordinador")
            return self._analyze_system_advanced()
        else:
            print("⚠️ Coordinador no disponible, usando análisis básico")
            return self._analyze_system_basic()
    
    def _identify_mock_components(self):
        """Identifica componentes mock en el sistema"""
        return self._analyze_system()
    
    def _calculate_priority(self, file_path: str, component_type: str) -> int:
        """Calcula prioridad numérica para ordenamiento"""
        priority_map = {"critical": 1, "high": 2, "medium": 3, "low": 4}
        priority = self._determine_priority(component_type, os.path.basename(file_path))
        return priority_map.get(priority, 4)
    
    def _update_system_state(self, conversion_results: Dict[str, Any]):
        """Actualiza el estado del sistema después de conversiones"""
        try:
            state_file = os.path.join(self.workspace_path, "STARK_SYSTEM_STATE.json")
            if os.path.exists(state_file):
                import json
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                # Actualizar timestamp
                state["last_updated"] = datetime.now().isoformat()
                
                # Añadir historial de conversión
                if "conversion_history" not in state:
                    state["conversion_history"] = []
                
                state["conversion_history"].append({
                    "timestamp": datetime.now().isoformat(),
                    "agent_version": self.version,
                    "completed": conversion_results.get("completed", []),
                    "failed": conversion_results.get("failed", [])
                })
                
                with open(state_file, 'w', encoding='utf-8') as f:
                    json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error actualizando estado: {e}")
    
    async def execute_mass_conversion(self):
        """Ejecuta conversión masiva de componentes mock"""
        if "coordinator" in self.sub_agents and self.sub_agents["coordinator"]:
            try:
                print("🎯 Ejecutando conversión masiva con coordinador...")
                result = await self.sub_agents["coordinator"].execute_mass_conversion()
                self._update_system_state(result)
                return result
            except Exception as e:
                print(f"❌ Error en conversión masiva: {e}")
                return {"error": str(e)}
        else:
            print("❌ Coordinador no disponible para conversión masiva")
            return {"error": "Coordinator not available"}
    
    def get_quick_status(self) -> Dict[str, Any]:
        """Obtiene estado rápido del agente"""
        mock_components = self._identify_mock_components()
        
        total_mocks = sum(len(components) for components in mock_components.values())
        
        return {
            "version": self.version,
            "workspace": self.workspace_path,
            "mock_components_detected": total_mocks,
            "priority_breakdown": {
                "critical": len(mock_components.get("critical", [])),
                "high": len(mock_components.get("high", [])),
                "medium": len(mock_components.get("medium", [])),
                "low": len(mock_components.get("low", []))
            },
            "sub_agents": list(self.sub_agents.keys()),
            "completed_tasks": len(self.completed_tasks),
            "efficiency": self._calculate_efficiency()
        }
    
    def _calculate_efficiency(self) -> float:
        """Calcula eficiencia del agente"""
        if not self.completed_tasks:
            return 0.0
        
        successful_tasks = sum(1 for task in self.completed_tasks if task.get("success", False))
        return (successful_tasks / len(self.completed_tasks)) * 100
    
    def generate_quick_report(self) -> str:
        """Genera reporte rápido del estado"""
        status = self.get_quick_status()
        
        report = f"""
🤖 JARVIS-FRIDAY AUTOPROGRAMMER V{status['version']} - REPORTE RÁPIDO
==================================================

📊 ESTADO DEL SISTEMA:
• Componentes mock detectados: {status['mock_components_detected']}
• Prioridad ALTA: {status['priority_breakdown']['critical'] + status['priority_breakdown']['high']}
• Prioridad MEDIA: {status['priority_breakdown']['medium']}
• Prioridad BAJA: {status['priority_breakdown']['low']}

🤖 ESTADO DEL AGENTE:
• Versión: {status['version']}
• Tareas completadas: {status['completed_tasks']}
• Eficiencia: {status['efficiency']:.1f}%
• Sub-agentes: {', '.join(status['sub_agents']) if status['sub_agents'] else 'Ninguno'}

⏰ Último análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return report


# Funciones de utilidad para ejecución directa
async def execute_mass_conversion_standalone():
    """Ejecuta conversión masiva de forma independiente"""
    agent = StarkAutoprogrammerAgent()
    
    print("\n📊 ANÁLISIS DEL SISTEMA...")
    mock_components = agent._identify_mock_components()
    total_mocks = sum(len(components) for components in mock_components.values())
    
    if total_mocks == 0:
        print("✅ No se detectaron componentes mock para convertir")
        return
    
    print(f"🔍 Detectados {total_mocks} componentes mock")
    print(agent.generate_quick_report())
    
    # Intentar conversión masiva
    result = await agent.execute_mass_conversion()
    
    if "error" not in result:
        print("✅ Conversión masiva completada exitosamente")
    else:
        print(f"❌ Error en conversión: {result['error']}")

def main():
    """Función principal para ejecución directa"""
    import asyncio
    
    print("🚀 JARVIS-FRIDAY AUTOPROGRAMMER V2.0 - EJECUCIÓN DIRECTA")
    
    try:
        agent = StarkAutoprogrammerAgent()
        
        # Mostrar estado inicial
        print(agent.generate_quick_report())
        
        # Preguntar por conversión masiva
        response = input("\n¿Ejecutar conversión masiva? (s/N): ").lower().strip()
        
        if response in ['s', 'y', 'yes', 'sí']:
            asyncio.run(execute_mass_conversion_standalone())
        else:
            print("🤖 Agente listo para uso manual")
            
    except Exception as e:
        print(f"❌ Error en ejecución principal: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()