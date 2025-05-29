"""
STARK INDUSTRIES - System Inspector V2.0
Herramienta avanzada de análisis e inspección del sistema
Proporciona información completa y actualizada en tiempo real
"""
import os
import json
import ast
import sys
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import importlib.util

class StarkSystemInspector:
    """
    Inspector avanzado del sistema STARK
    Analiza estado real, detecta componentes, verifica implementaciones
    """
    
    def __init__(self, workspace_path: str = None):
        if workspace_path is None:
            workspace_path = os.getcwd()
        self.workspace_path = workspace_path
        self.modules_structure = {
            "neural": ["_MAIN.py", "jarvis_core.py", "friday_core.py", "copilot_core.py", 
                      "neural_network.py", "learning_engine.py", "memory_manager.py"],
            "perception": ["_MAIN.py", "vision_system.py", "audio_processor.py", 
                          "sensor_integration.py", "pattern_recognition.py", "environment_monitor.py"],
            "communication": ["_MAIN.py", "voice_synthesis.py", "natural_language.py", 
                             "protocol_manager.py", "interface_handler.py", "network_comm.py"],
            "agents": ["_MAIN.py", "agent_coordinator.py", "task_manager.py", 
                      "decision_engine.py", "behavior_patterns.py", "autoprogrammer_agent.py"],
            "system": ["_MAIN.py", "memory_manager.py", "config_manager.py", 
                      "logger.py", "health_monitor.py", "state_analyzer.py"],
            "intelligence": ["_MAIN.py", "decision_maker.py", "analytics_engine.py", 
                            "learning_system.py", "strategy_planner.py", "optimization_ai.py"]
        }
    
    def get_complete_system_analysis(self) -> Dict[str, Any]:
        """Análisis completo y actualizado del sistema"""
        print("🔍 STARK SYSTEM INSPECTOR - Análisis completo iniciado")
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "workspace": self.workspace_path,
            "modules": {},
            "files_analysis": {},
            "implementation_status": {},
            "mock_components": {},
            "real_components": {},
            "system_health": {},
            "autoprogrammer_status": {},
            "recommendations": []
        }
        
        # Análisis por módulo
        for module_name, files in self.modules_structure.items():
            analysis["modules"][module_name] = self._analyze_module(module_name, files)
        
        # Análisis de archivos críticos
        critical_files = [
            "LAUNCHER_MAIN.py",
            "STARK_SYSTEM_STATE.json", 
            "STARK_PROGRESS.md",
            "STARK_ACTION_PLAN.md"
        ]
        
        for file_name in critical_files:
            file_path = os.path.join(self.workspace_path, file_name)
            analysis["files_analysis"][file_name] = self._analyze_file(file_path)
        
        # Estado de implementación global
        analysis["implementation_status"] = self._calculate_implementation_status(analysis["modules"])
        
        # Componentes mock vs real
        mock_real_analysis = self._analyze_mock_vs_real(analysis["modules"])
        analysis["mock_components"] = mock_real_analysis["mock"]
        analysis["real_components"] = mock_real_analysis["real"]
        
        # Salud del sistema
        analysis["system_health"] = self._assess_system_health(analysis)
        
        # Estado del autoprogrammer
        analysis["autoprogrammer_status"] = self._analyze_autoprogrammer()
        
        # Recomendaciones
        analysis["recommendations"] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _analyze_module(self, module_name: str, expected_files: List[str]) -> Dict[str, Any]:
        """Analiza un módulo específico"""
        module_path = os.path.join(self.workspace_path, module_name)
        
        module_analysis = {
            "path": module_path,
            "exists": os.path.exists(module_path),
            "files": {},
            "completion_rate": 0,
            "mock_count": 0,
            "real_count": 0,
            "status": "UNKNOWN"
        }
        
        if not module_analysis["exists"]:
            module_analysis["status"] = "MISSING"
            return module_analysis
        
        existing_files = 0
        for file_name in expected_files:
            file_path = os.path.join(module_path, file_name)
            file_analysis = self._analyze_file(file_path)
            module_analysis["files"][file_name] = file_analysis
            
            if file_analysis["exists"]:
                existing_files += 1
                if file_analysis["implementation_type"] == "mock":
                    module_analysis["mock_count"] += 1
                elif file_analysis["implementation_type"] == "real":
                    module_analysis["real_count"] += 1
        
        # Calcular tasa de completitud
        module_analysis["completion_rate"] = (existing_files / len(expected_files)) * 100
        
        # Determinar estado del módulo
        if existing_files == 0:
            module_analysis["status"] = "EMPTY"
        elif existing_files == len(expected_files):
            if module_analysis["real_count"] > module_analysis["mock_count"]:
                module_analysis["status"] = "MOSTLY_REAL"
            elif module_analysis["mock_count"] > module_analysis["real_count"]:
                module_analysis["status"] = "MOSTLY_MOCK"
            else:
                module_analysis["status"] = "MIXED"
        else:
            module_analysis["status"] = "PARTIAL"
        
        return module_analysis
    
    def _analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analiza un archivo específico"""
        file_analysis = {
            "path": file_path,
            "exists": os.path.exists(file_path),
            "size": 0,
            "lines": 0,
            "implementation_type": "unknown",
            "has_classes": False,
            "has_functions": False,
            "imports": [],
            "last_modified": None,
            "syntax_valid": False,
            "content_summary": ""
        }
        
        if not file_analysis["exists"]:
            return file_analysis
        
        try:
            # Información básica del archivo
            stat_info = os.stat(file_path)
            file_analysis["size"] = stat_info.st_size
            file_analysis["last_modified"] = datetime.fromtimestamp(stat_info.st_mtime).isoformat()
            
            # Leer contenido
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_analysis["lines"] = len(content.splitlines())
            
            # Análisis de código Python
            if file_path.endswith('.py'):
                file_analysis.update(self._analyze_python_file(content))
            elif file_path.endswith('.json'):
                file_analysis.update(self._analyze_json_file(content))
            elif file_path.endswith('.md'):
                file_analysis.update(self._analyze_markdown_file(content))
            
        except Exception as e:
            file_analysis["error"] = str(e)
        
        return file_analysis
    
    def _analyze_python_file(self, content: str) -> Dict[str, Any]:
        """Analiza contenido de archivo Python"""
        analysis = {
            "syntax_valid": False,
            "has_classes": False,
            "has_functions": False,
            "imports": [],
            "implementation_type": "unknown",
            "content_summary": ""
        }
        
        try:
            # Verificar sintaxis
            tree = ast.parse(content)
            analysis["syntax_valid"] = True
            
            # Analizar estructura
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    analysis["has_classes"] = True
                elif isinstance(node, ast.FunctionDef):
                    analysis["has_functions"] = True
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis["imports"].append(alias.name)
                    else:
                        analysis["imports"].append(node.module or "")
            
            # Detectar tipo de implementación
            analysis["implementation_type"] = self._detect_implementation_type(content)
            
            # Resumen de contenido
            if analysis["has_classes"] and analysis["has_functions"]:
                analysis["content_summary"] = "Complete implementation with classes and functions"
            elif analysis["has_classes"]:
                analysis["content_summary"] = "Class-based implementation"
            elif analysis["has_functions"]:
                analysis["content_summary"] = "Function-based implementation"
            else:
                analysis["content_summary"] = "Basic script or configuration"
                
        except SyntaxError as e:
            analysis["syntax_error"] = str(e)
        except Exception as e:
            analysis["parse_error"] = str(e)
        
        return analysis
    
    def _detect_implementation_type(self, content: str) -> str:
        """Detecta si la implementación es mock o real"""
        # Indicadores de mock
        mock_indicators = [
            "pass  # TODO",
            "pass # TODO", 
            "# Mock implementation",
            "raise NotImplementedError",
            "return None  # Mock",
            "print(\"Mock",
            "# Placeholder",
            "# MOCK:",
            "TODO: Implement"
        ]
        
        # Indicadores de implementación real - CORREGIDO: escapar el punto correctamente
        real_indicators = [
            "import torch",
            "import tensorflow",
            "import numpy",
            "import cv2",
            "class.*:",
            "def.*:",
            "return .*[^None]",
            r"self\.",  # Escapado correctamente
            "try:",
            "except:",
            "for.*in",
            "while.*:",
            "if.*:"
        ]
        
        content_lower = content.lower()
        
        # Contar indicadores mock
        mock_count = sum(1 for indicator in mock_indicators if indicator.lower() in content_lower)
        
        # Contar indicadores reales
        real_count = 0
        for indicator in real_indicators:
            if indicator == r"self\.":
                # Verificación especial para self.
                if "self." in content:
                    real_count += 1
            elif indicator in content:
                real_count += 1
        
        # Determinar tipo basado en contenido
        if mock_count > 2:
            return "mock"
        elif real_count > 3 and len(content) > 500:
            return "real"
        elif "pass" in content and len(content) < 200:
            return "mock"
        else:
            return "partial"
    
    def _analyze_json_file(self, content: str) -> Dict[str, Any]:
        """Analiza contenido de archivo JSON"""
        analysis = {"content_summary": "JSON configuration file"}
        
        try:
            data = json.loads(content)
            analysis["json_valid"] = True
            analysis["json_keys"] = list(data.keys()) if isinstance(data, dict) else []
            analysis["implementation_type"] = "config"
        except json.JSONDecodeError as e:
            analysis["json_valid"] = False
            analysis["json_error"] = str(e)
        
        return analysis
    
    def _analyze_markdown_file(self, content: str) -> Dict[str, Any]:
        """Analiza contenido de archivo Markdown"""
        return {
            "content_summary": "Documentation file",
            "implementation_type": "documentation",
            "has_headers": "# " in content,
            "has_lists": "- " in content or "* " in content
        }
    
    def _calculate_implementation_status(self, modules: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula el estado general de implementación"""
        total_files = 0
        existing_files = 0
        real_files = 0
        mock_files = 0
        
        for module_name, module_data in modules.items():
            module_total = len(module_data["files"])
            total_files += module_total
            
            for file_name, file_data in module_data["files"].items():
                if file_data["exists"]:
                    existing_files += 1
                    if file_data["implementation_type"] == "real":
                        real_files += 1
                    elif file_data["implementation_type"] == "mock":
                        mock_files += 1
        
        return {
            "total_files": total_files,
            "existing_files": existing_files,
            "real_files": real_files,
            "mock_files": mock_files,
            "completion_rate": (existing_files / total_files * 100) if total_files > 0 else 0,
            "real_rate": (real_files / existing_files * 100) if existing_files > 0 else 0,
            "mock_rate": (mock_files / existing_files * 100) if existing_files > 0 else 0
        }
    
    def _analyze_mock_vs_real(self, modules: Dict[str, Any]) -> Dict[str, List[str]]:
        """Analiza componentes mock vs real"""
        mock_components = []
        real_components = []
        
        for module_name, module_data in modules.items():
            for file_name, file_data in module_data["files"].items():
                if file_data["exists"]:
                    file_path = f"{module_name}/{file_name}"
                    if file_data["implementation_type"] == "mock":
                        mock_components.append(file_path)
                    elif file_data["implementation_type"] == "real":
                        real_components.append(file_path)
        
        return {
            "mock": mock_components,
            "real": real_components
        }
    
    def _assess_system_health(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Evalúa la salud general del sistema"""
        impl_status = analysis["implementation_status"]
        
        health_score = 0
        health_factors = []
        
        # Factor 1: Tasa de completitud
        completion_rate = impl_status["completion_rate"]
        if completion_rate >= 90:
            health_score += 30
            health_factors.append("Excellent completion rate")
        elif completion_rate >= 70:
            health_score += 20
            health_factors.append("Good completion rate")
        else:
            health_factors.append("Low completion rate")
        
        # Factor 2: Tasa de implementación real
        real_rate = impl_status["real_rate"]
        if real_rate >= 70:
            health_score += 30
            health_factors.append("High real implementation rate")
        elif real_rate >= 40:
            health_score += 15
            health_factors.append("Moderate real implementation rate")
        else:
            health_factors.append("High mock component ratio")
        
        # Factor 3: Archivos críticos
        critical_files_ok = True
        for file_name, file_data in analysis["files_analysis"].items():
            if not file_data["exists"]:
                critical_files_ok = False
                break
        
        if critical_files_ok:
            health_score += 25
            health_factors.append("All critical files present")
        else:
            health_factors.append("Missing critical files")
        
        # Factor 4: Sintaxis válida
        syntax_errors = 0
        total_python_files = 0
        
        for module_data in analysis["modules"].values():
            for file_data in module_data["files"].values():
                if file_data["path"].endswith('.py') and file_data["exists"]:
                    total_python_files += 1
                    if not file_data.get("syntax_valid", False):
                        syntax_errors += 1
        
        if syntax_errors == 0 and total_python_files > 0:
            health_score += 15
            health_factors.append("No syntax errors")
        elif syntax_errors <= 2:
            health_score += 10
            health_factors.append("Few syntax errors")
        else:
            health_factors.append("Multiple syntax errors")
        
        # Determinar estado de salud
        if health_score >= 85:
            health_status = "EXCELLENT"
        elif health_score >= 70:
            health_status = "GOOD"
        elif health_score >= 50:
            health_status = "FAIR"
        else:
            health_status = "POOR"
        
        return {
            "score": health_score,
            "status": health_status,
            "factors": health_factors,
            "completion_rate": completion_rate,
            "real_rate": real_rate,
            "total_files": impl_status["total_files"],
            "existing_files": impl_status["existing_files"]
        }
    
    def _analyze_autoprogrammer(self) -> Dict[str, Any]:
        """Analiza el estado del sistema de autoprogramación"""
        autoprogrammer_files = [
            "agents/autoprogrammer_agent.py",
            "agents/autoprogrammer_coordinator.py"
        ]
        
        status = {
            "available": False,
            "files_status": {},
            "can_execute": False,
            "last_execution": None
        }
        
        files_ok = 0
        for file_path in autoprogrammer_files:
            full_path = os.path.join(self.workspace_path, file_path)
            file_analysis = self._analyze_file(full_path)
            status["files_status"][file_path] = file_analysis
            
            if file_analysis["exists"] and file_analysis.get("syntax_valid", False):
                files_ok += 1
        
        status["available"] = files_ok == len(autoprogrammer_files)
        status["can_execute"] = status["available"]
        
        return status
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []
        
        impl_status = analysis["implementation_status"]
        health = analysis["system_health"]
        
        # Recomendaciones basadas en mock ratio
        if impl_status["mock_rate"] > 60:
            recommendations.append("HIGH PRIORITY: Execute mass mock-to-real conversion using autoprogrammer")
        
        # Recomendaciones basadas en completitud
        if impl_status["completion_rate"] < 90:
            recommendations.append("MEDIUM PRIORITY: Complete missing module files")
        
        # Recomendaciones específicas por módulo
        for module_name, module_data in analysis["modules"].items():
            if module_data["status"] == "MOSTLY_MOCK":
                recommendations.append(f"Convert {module_name} module from mock to real implementation")
            elif module_data["status"] == "PARTIAL":
                recommendations.append(f"Complete missing files in {module_name} module")
        
        # Recomendaciones de autoprogramación
        if analysis["autoprogrammer_status"]["available"]:
            recommendations.append("READY: Autoprogrammer system is available for mass conversion")
        else:
            recommendations.append("CRITICAL: Fix autoprogrammer system for automated conversions")
        
        return recommendations
    
    def generate_detailed_report(self) -> str:
        """Genera un reporte detallado del sistema"""
        analysis = self.get_complete_system_analysis()
        
        report = f"""
🔍 STARK SYSTEM INSPECTOR - DETAILED REPORT
============================================
📅 Analysis Date: {analysis['timestamp']}
📁 Workspace: {analysis['workspace']}

🏥 SYSTEM HEALTH: {analysis['system_health']['status']} ({analysis['system_health']['score']}/100)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 IMPLEMENTATION STATUS:
• Total Files: {analysis['implementation_status']['total_files']}
• Existing Files: {analysis['implementation_status']['existing_files']}
• Completion Rate: {analysis['implementation_status']['completion_rate']:.1f}%
• Real Implementation Rate: {analysis['implementation_status']['real_rate']:.1f}%
• Mock Component Rate: {analysis['implementation_status']['mock_rate']:.1f}%

🗂️ MODULE ANALYSIS:
"""
        
        for module_name, module_data in analysis["modules"].items():
            report += f"""
📁 {module_name.upper()}:
   Status: {module_data['status']}
   Completion: {module_data['completion_rate']:.1f}%
   Real/Mock: {module_data['real_count']}/{module_data['mock_count']}
"""
        
        report += f"""
🤖 AUTOPROGRAMMER STATUS:
• Available: {'✅' if analysis['autoprogrammer_status']['available'] else '❌'}
• Can Execute: {'✅' if analysis['autoprogrammer_status']['can_execute'] else '❌'}

🎯 PRIORITY RECOMMENDATIONS:
"""
        
        for i, rec in enumerate(analysis["recommendations"], 1):
            report += f"{i}. {rec}\n"
        
        report += f"""
📋 MOCK COMPONENTS DETECTED ({len(analysis['mock_components'])}):
"""
        for mock in analysis["mock_components"]:
            report += f"   • {mock}\n"
        
        return report
    
    def update_system_state_file(self):
        """Actualiza el archivo STARK_SYSTEM_STATE.json con información real"""
        analysis = self.get_complete_system_analysis()
        
        # Crear estado actualizado basado en análisis real
        updated_state = {
            "meta": {
                "version": "2.0.0",
                "last_update": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "session_id": f"STARK_INSPECTOR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "status": "FULLY_OPERATIONAL" if analysis['system_health']['status'] in ['EXCELLENT', 'GOOD'] else "OPERATIONAL",
                "confidence_level": analysis['system_health']['score'] / 100,
                "system_health": analysis['system_health']['status']
            },
            "modules": {},
            "implementation_status": analysis["implementation_status"],
            "system_health": analysis["system_health"],
            "autoprogrammer_status": analysis["autoprogrammer_status"],
            "real_analysis": {
                "timestamp": analysis["timestamp"],
                "inspector_version": "2.0.0",
                "mock_components": analysis["mock_components"],
                "real_components": analysis["real_components"],
                "recommendations": analysis["recommendations"]
            },
            "last_updated": analysis["timestamp"]
        }
        
        # Convertir análisis de módulos al formato esperado
        for module_name, module_data in analysis["modules"].items():
            updated_state["modules"][module_name] = {
                "status": "ACTIVE" if module_data["exists"] else "INACTIVE",
                "completion_rate": module_data["completion_rate"],
                "real_count": module_data["real_count"],
                "mock_count": module_data["mock_count"],
                "components": {},
                "implementation_analysis": module_data
            }
            
            # Añadir estado de componentes
            for file_name, file_data in module_data["files"].items():
                if file_data["exists"]:
                    if file_data["implementation_type"] == "real":
                        status = "IMPLEMENTED"
                    elif file_data["implementation_type"] == "mock":
                        status = "MOCK"
                    else:
                        status = "PARTIAL"
                else:
                    status = "MISSING"
                
                updated_state["modules"][module_name]["components"][file_name] = status
        
        # Guardar estado actualizado
        state_file = os.path.join(self.workspace_path, "STARK_SYSTEM_STATE.json")
        try:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(updated_state, f, indent=2, ensure_ascii=False)
            print(f"✅ Estado del sistema actualizado: {state_file}")
        except Exception as e:
            print(f"❌ Error actualizando estado del sistema: {e}")


def inspect_stark_system(workspace_path: str = None, detailed_report: bool = True) -> Dict[str, Any]:
    """Función principal de inspección del sistema STARK"""
    inspector = StarkSystemInspector(workspace_path)
    
    if detailed_report:
        print(inspector.generate_detailed_report())
    
    # Actualizar archivo de estado
    inspector.update_system_state_file()
    
    return inspector.get_complete_system_analysis()

if __name__ == "__main__":
    print("🔍 STARK SYSTEM INSPECTOR V2.0 - Iniciando análisis...")
    analysis = inspect_stark_system()
    print(f"\n📊 Análisis completado. Mock ratio: {analysis['implementation_status']['mock_rate']:.1f}%")