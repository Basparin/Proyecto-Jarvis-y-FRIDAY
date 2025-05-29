#!/usr/bin/env python3
"""
STARK INDUSTRIES - LAUNCHER MAIN
Sistema de control unificado para JARVIS, FRIDAY y COPILOT
Dashboard de control con categorías modulares
"""

import os
import sys
import importlib.util
from pathlib import Path
import asyncio
from typing import Dict, List, Optional

class StarkLauncher:
    """Dashboard de control principal del sistema STARK"""
    
    def __init__(self):
        self.root_path = Path(__file__).parent
        self.categories = {
            'neural': 'Neural Processing & Learning',
            'perception': 'Sensory Input & Recognition', 
            'communication': 'Natural Language & Interfaces',
            'agents': 'AI Personalities & Coordination',
            'system': 'Core Infrastructure & Memory',
            'intelligence': 'Decision Making & Analytics'
        }
        self.active_modules = {}
        self.ai_coordinator = None  # Persistente entre llamadas
        
    def display_dashboard(self):
        """Muestra el dashboard principal de control"""
        print("\n" + "="*60)
        print("🔷 STARK INDUSTRIES - SISTEMA UNIFICADO 🔷")
        print("="*60)
        print("JARVIS | FRIDAY | COPILOT - Operacional")
        print("-"*60)
        
        for i, (key, desc) in enumerate(self.categories.items(), 1):
            status = "🟢 ACTIVO" if key in self.active_modules else "🔴 INACTIVO"
            print(f"{i}. {desc:<35} {status}")
        
        print("-"*60)
        print("7. Ejecutar Todos los Módulos")
        print("8. Estado del Sistema")
        print("9. Configuración Avanzada")        
        print("10. 🧬 Auto-Mejora Inteligente")  # NUEVO
        print("11. ⚡ Optimización Continua")   # NUEVO
        print("12. 🔄 Evolución del Sistema")   # NUEVO
        print("13. 🤝 Coordinación AI Tripartita")  # NUEVO
        print("14. 🎯 Eliminar Componentes Mock")   # NUEVO
        print("15. 🧠 Memoria Permanente AI")      # NUEVO
        print("0. Salir")
        print("="*60)
        
    def load_category_main(self, category: str) -> Optional[object]:
        """Carga el módulo _MAIN.py de una categoría"""
        main_path = self.root_path / category / "_MAIN.py"
        
        if not main_path.exists():
            print(f"⚠️  Módulo {category}/_MAIN.py no encontrado")
            return None
            
        try:
            spec = importlib.util.spec_from_file_location(f"{category}_main", main_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            self.active_modules[category] = module
            print(f"✅ {category.upper()} cargado exitosamente")
            return module
            
        except Exception as e:
            print(f"❌ Error cargando {category}: {e}")
            return None
    
    def execute_category(self, category: str):
        """Ejecuta una categoría específica"""
        if category not in self.categories:
            print("❌ Categoría no válida")
            return
            
        print(f"\n🚀 Iniciando {category.upper()}...")
        module = self.load_category_main(category)
        
        if module and hasattr(module, 'main'):
            try:
                module.main()
            except Exception as e:
                print(f"❌ Error ejecutando {category}: {e}")
    
    def execute_all_modules(self):
        """Ejecuta todos los módulos del sistema"""
        print("\n🚀 INICIALIZANDO SISTEMA STARK COMPLETO...")
        
        for category in self.categories.keys():
            self.execute_category(category)
            
        print("\n✅ Sistema STARK completamente operacional")
        
    def show_system_status(self):
        """Muestra el estado detallado del sistema"""
        print("\n" + "="*50)
        print("📊 ESTADO DEL SISTEMA STARK")
        print("="*50)
        
        for category, desc in self.categories.items():
            main_file = self.root_path / category / "_MAIN.py"
            exists = "✅" if main_file.exists() else "❌"
            loaded = "🟢" if category in self.active_modules else "🔴"
            
            print(f"{category.upper():<15} {exists} {loaded} {desc}")
            
        print(f"\nMódulos activos: {len(self.active_modules)}/{len(self.categories)}")
        print("="*50)
    
    def show_advanced_config(self):
        """Muestra configuración avanzada del sistema"""
        print("\n⚙️ CONFIGURACIÓN AVANZADA STARK")
        print("="*40)
        print("1. Configurar umbrales de optimización")
        print("2. Ajustar intervalos de auto-mejora")
        print("3. Configurar métricas de rendimiento")
        print("4. Establecer políticas de evolución")
        print("5. Volver al menú principal")
        
        config_choice = input("\nSelecciona opción: ")
        if config_choice == '1':            print("📊 Configurando umbrales de optimización...")
        elif config_choice == '2':
            print("⏰ Configurando intervalos de auto-mejora...")
        # Más opciones según necesidad
    async def start_intelligent_improvement(self):
        """Inicia proceso de auto-mejora inteligente"""
        print("\n🧬 STARK INTELLIGENT IMPROVEMENT")
        print("="*40)
        
        try:
            # Importar coordinador
            sys.path.append(str(self.root_path / 'agents'))
            from autoprogrammer_coordinator import StarkAutoprogrammerCoordinator
            
            coordinator = StarkAutoprogrammerCoordinator(workspace_path=str(self.root_path))
            
            print("� 1. Ejecutar auto-mejora inmediata")
            print("📊 2. Ver historial de mejoras")
            print("🔄 3. Cancelar")
            
            choice = input("\nSelecciona opción: ")
            
            if choice == '1':
                print("�🚀 Iniciando análisis y auto-mejora...")
                improvement_result = await coordinator.self_improve_system()
                
                print("\n✅ AUTO-MEJORA COMPLETADA")
                print(f"Mejoras aplicadas: {improvement_result.get('improvements_applied', 0)}")
                print(f"Ganancia de rendimiento: {improvement_result.get('performance_gain', 0):.1f}%")
                print(f"Nuevas capacidades: {improvement_result.get('new_capabilities', 0)}")
                
            elif choice == '2':
                print("📊 Generando historial de mejoras...")
                history_report = await coordinator.get_improvement_history_report()
                print(history_report)
                
            else:
                print("❌ Auto-mejora cancelada")
            
        except Exception as e:
            print(f"❌ Error en auto-mejora: {e}")
    async def start_continuous_optimization(self):
        """Inicia optimización continua del sistema"""
        print("\n⚡ STARK CONTINUOUS OPTIMIZATION")
        print("="*40)
        
        try:
            # Importar optimizador
            sys.path.append(str(self.root_path / 'agents'))
            from intelligent_optimizer import StarkIntelligentOptimizer
            
            optimizer = StarkIntelligentOptimizer()
            
            print("🔍 1. Iniciar optimización continua")
            print("📊 2. Ver historial de optimizaciones")
            print("🔄 3. Cancelar")
            
            choice = input("\nSelecciona opción: ")
            
            if choice == '1':
                print("🎯 ¿Iniciar optimización continua en background?")
                bg_choice = input("(s/N): ").lower()
                
                if bg_choice in ['s', 'si', 'sí', 'y', 'yes']:
                    print("🚀 Iniciando optimización inteligente...")
                    # Ejecutar en background
                    task = asyncio.create_task(optimizer.start_intelligent_optimization())
                    print("✅ Optimización continua activada en background")
                    
                    # Mostrar reporte inicial
                    await asyncio.sleep(2)  # Esperar un poco para que inicie
                    print("\n📊 REPORTE INICIAL:")
                    report = await optimizer.get_optimization_report()
                    print(report)
                else:
                    print("❌ Optimización continua cancelada")
                    
            elif choice == '2':
                print("📊 Generando historial de optimizaciones...")
                report = await optimizer.get_optimization_report()
                print(report)
                
            else:
                print("❌ Optimización cancelada")
                
        except Exception as e:
            print(f"❌ Error en optimización: {e}")
    
    async def start_system_evolution(self):
        """Inicia evolución del sistema"""
        print("\n🔄 STARK SYSTEM EVOLUTION")
        print("="*40)
        try:
            # Importar motor de evolución
            sys.path.append(str(self.root_path / 'agents'))
            from self_evolution_engine import StarkSelfEvolutionEngine
            
            evolution_engine = StarkSelfEvolutionEngine(workspace_path=str(self.root_path))
            
            print("🧬 Selecciona tipo de evolución:")
            print("1. Evolución manual inmediata")
            print("2. Evolución continua (24h ciclos)")
            print("3. Ver reporte de evolución")
            print("4. Cancelar")
            
            evo_choice = input("\nSelecciona opción: ")
            
            if evo_choice == '1':
                print("🔥 Ejecutando evolución manual...")
                evolution_result = await evolution_engine.manual_evolution_trigger()
                
                print("\n✅ EVOLUCIÓN COMPLETADA")
                print(f"Duración: {evolution_result.get('duration_seconds', 0):.1f}s")
                print(f"Mejoras aplicadas: {evolution_result.get('improvements_applied', 0)}")
                print(f"Ganancia rendimiento: {evolution_result.get('performance_gain', 0):.1f}%")
                
            elif evo_choice == '2':
                print("🔄 Iniciando evolución continua...")
                task = asyncio.create_task(evolution_engine.start_continuous_evolution(interval_hours=24))
                print("✅ Evolución continua activada (ciclos de 24h)")
                
            elif evo_choice == '3':
                print(evolution_engine.get_evolution_report())                
            else:
                print("❌ Evolución cancelada")
                
        except Exception as e:
            print(f"❌ Error en evolución: {e}")
    async def start_ai_coordination(self):
        """Inicia sistema de coordinación AI tripartito"""
        print("\n🤝 STARK AI COORDINATION SYSTEM")
        print("="*45)
        
        try:
            # Inicializar coordinador persistente si no existe
            if self.ai_coordinator is None:
                sys.path.append(str(self.root_path / 'neural'))
                from ai_coordination_system import AICoordinationSystem
                self.ai_coordinator = AICoordinationSystem(str(self.root_path))
            
            coord_system = self.ai_coordinator
            
            print("🧠 1. Inicializar entidades AI autónomas")
            print("🤝 2. Establecer coordinación tripartita")
            print("🎯 3. Test de colaboración AI")
            print("📊 4. Estado de coordinación")
            print("🔄 5. Cancelar")
            
            choice = input("\nSelecciona opción: ")
            
            if choice == '1':
                print("🧠 Inicializando entidades AI como individuos autónomos...")
                init_results = coord_system.initialize_ai_entities()
                
                print("\n✅ ENTIDADES AI INICIALIZADAS:")
                for ai_name, result in init_results.items():
                    if isinstance(result, dict) and 'status' in result:
                        print(f"  {ai_name}: {result['status']}")
                        print(f"    Personalidad: {result.get('personality', 'N/A')}")
                        print(f"    Capacidades: {', '.join(result.get('capabilities', []))}")
                    
            elif choice == '2':
                print("🤝 Estableciendo coordinación tripartita...")
                coord_results = coord_system.establish_tripartite_coordination()
                
                print(f"\n✅ COORDINACIÓN: {coord_results.get('coordination_level', 'Unknown')}")
                print(f"AIs activos: {', '.join(coord_results.get('active_ais', []))}")
                print(f"Protocolos: {coord_results.get('communication_protocols', 'Inactive')}")
                
            elif choice == '3':
                print("🎯 Ejecutando test de colaboración AI...")
                collab_result = coord_system.coordinate_ai_collaboration(
                    "Test tripartite collaboration: analyze workspace and optimize performance"
                )
                
                print(f"\n✅ COLABORACIÓN COMPLETADA:")
                print(f"Éxito: {collab_result.get('coordination_success', False)}")
                print(f"AIs participantes: {len(collab_result.get('execution_results', {}).get('ai_contributions', {}))}")
                
            elif choice == '4':
                print("📊 Obteniendo estado de coordinación...")
                status = coord_system.get_coordination_status()
                
                print(f"\n📊 ESTADO DE COORDINACIÓN:")
                print(f"Sistema activo: {status.get('coordination_active', False)}")
                print(f"AIs operacionales: {', '.join(status.get('active_ai_entities', []))}")
                print(f"Colaboraciones totales: {status.get('total_collaborations', 0)}")
                print(f"Preparación sistema: {status.get('system_readiness', 'Unknown')}")
                
            else:
                print("❌ Coordinación AI cancelada")
                
        except Exception as e:
            print(f"❌ Error en coordinación AI: {e}")
    
    async def eliminate_mock_components(self):
        """Elimina componentes mock del sistema"""
        print("\n🎯 STARK MOCK COMPONENT ELIMINATION")
        print("="*45)
        
        try:
            # Importar sistema de coordinación
            sys.path.append(str(self.root_path / 'neural'))
            from ai_coordination_system import AICoordinationSystem
            
            coord_system = AICoordinationSystem(str(self.root_path))
            
            print("🔍 1. Detectar componentes mock")
            print("🎯 2. Eliminar componentes mock (coordinado)")
            print("📊 3. Reporte de progreso mock→real")
            print("🔄 4. Cancelar")
            
            choice = input("\nSelecciona opción: ")
            
            if choice == '1':
                print("🔍 Detectando componentes mock...")
                
                # Usar COPILOT para detección
                if coord_system.ai_entities.get('COPILOT'):
                    mock_detection = coord_system.ai_entities['COPILOT'].autonomous_workspace_optimization()
                    mock_results = mock_detection.get('mock_component_detection', {})
                    
                    print(f"\n📊 COMPONENTES MOCK DETECTADOS:")
                    print(f"Total detectados: {mock_results.get('total_mocks_detected', 0)}")
                    
                    for mock in mock_results.get('mock_components', [])[:5]:  # Mostrar primeros 5
                        print(f"  📄 {mock.get('file', 'Unknown')}")
                        print(f"    Indicador: {mock.get('indicator', 'Unknown')}")
                else:
                    print("⚠️ COPILOT no disponible para detección")
                    
            elif choice == '2':
                print("🎯 Iniciando eliminación coordinada de mocks...")
                elimination_result = coord_system.eliminate_mock_components()
                
                print(f"\n✅ ELIMINACIÓN COMPLETADA:")
                print(f"Coordinación exitosa: {elimination_result.get('coordination_success', False)}")
                print("Componentes mock convertidos a implementaciones reales")
                
            elif choice == '3':
                print("📊 Generando reporte de progreso...")
                
                # Calcular porcentaje actual de mocks
                total_files = 0
                mock_files = 0
                
                for file_path in self.root_path.rglob("*.py"):
                    total_files += 1
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read().lower()
                            if any(indicator in content for indicator in ['mock', 'placeholder', 'todo', 'fixme']):
                                mock_files += 1
                    except:
                        continue
                
                mock_percentage = (mock_files / total_files * 100) if total_files > 0 else 0
                
                print(f"\n📊 REPORTE DE PROGRESO MOCK→REAL:")
                print(f"Archivos totales: {total_files}")
                print(f"Archivos con componentes mock: {mock_files}")
                print(f"Porcentaje de mocks: {mock_percentage:.1f}%")
                print(f"Objetivo: 0.0% (Implementaciones reales completas)")
                
            else:
                print("❌ Eliminación de mocks cancelada")
                
        except Exception as e:
            print(f"❌ Error eliminando mocks: {e}")
    
    async def initialize_permanent_memory(self):
        """Inicializa sistema de memoria permanente AI"""
        print("\n🧠 STARK PERMANENT AI MEMORY SYSTEM")
        print("="*45)
        
        try:
            print("💾 1. Inicializar memoria permanente JARVIS")
            print("🛡️ 2. Inicializar memoria permanente FRIDAY")
            print("⚡ 3. Inicializar memoria permanente COPILOT")
            print("🤝 4. Inicializar memoria compartida tripartita")
            print("📊 5. Estado de memoria permanente")
            print("🔄 6. Cancelar")
            
            choice = input("\nSelecciona opción: ")
            
            if choice == '1':
                print("💾 Inicializando memoria permanente JARVIS...")
                sys.path.append(str(self.root_path / 'neural'))
                from jarvis_core import JarvisCore
                
                jarvis = JarvisCore(str(self.root_path))
                memory_status = jarvis.get_status()
                
                print(f"✅ JARVIS memoria permanente: {memory_status.get('memory_system', 'Unknown')}")
                print(f"Contextos almacenados: {memory_status.get('memory_contexts', 0)}")
                
            elif choice == '2':
                print("🛡️ Inicializando memoria permanente FRIDAY...")
                sys.path.append(str(self.root_path / 'neural'))
                from friday_core import FridayCore
                
                friday = FridayCore(str(self.root_path))
                memory_status = friday.get_status()
                
                print(f"✅ FRIDAY memoria permanente: {memory_status.get('memory_system', 'Unknown')}")
                print(f"Análisis almacenados: {memory_status.get('analysis_history', 0)}")
                
            elif choice == '3':
                print("⚡ Inicializando memoria permanente COPILOT...")
                sys.path.append(str(self.root_path / 'neural'))
                from copilot_core import CopilotCore
                
                copilot = CopilotCore(str(self.root_path))
                memory_status = copilot.get_status()
                
                print(f"✅ COPILOT memoria permanente: {memory_status.get('context_memory_size', 0)} contextos")
                print(f"Optimizaciones realizadas: {memory_status.get('optimizations_performed', 0)}")
                
            elif choice == '4':
                print("🤝 Inicializando memoria compartida tripartita...")
                sys.path.append(str(self.root_path / 'neural'))
                from ai_coordination_system import AICoordinationSystem
                
                coord_system = AICoordinationSystem(str(self.root_path))
                shared_db = coord_system._initialize_shared_memory()
                
                print(f"✅ Memoria compartida inicializada: {shared_db}")
                print("Base de datos de coordinación AI operacional")
                
            elif choice == '5':
                print("📊 Verificando estado de memoria permanente...")
                
                memory_files = []
                for db_file in self.root_path.rglob("*.db"):
                    memory_files.append(str(db_file))
                
                print(f"\n📊 ESTADO MEMORIA PERMANENTE:")
                print(f"Bases de datos detectadas: {len(memory_files)}")
                for db in memory_files:
                    print(f"  💾 {Path(db).name}")
                
                print(f"\nSistema de memoria: {'✅ OPERACIONAL' if memory_files else '❌ NO INICIALIZADO'}")
                
            else:
                print("❌ Inicialización de memoria cancelada")
                
        except Exception as e:
            print(f"❌ Error en memoria permanente: {e}")
    
    async def run(self):
        """Bucle principal del sistema"""
        while True:
            self.display_dashboard()
            
            try:
                choice = input("\n🔷 Selecciona una opción: ").strip()
                if choice == '0':
                    print("\n🔷 Apagando sistema STARK...")
                    break
                elif choice in ['1', '2', '3', '4', '5', '6']:
                    category_list = list(self.categories.keys())
                    category_index = int(choice) - 1
                    if 0 <= category_index < len(category_list):
                        self.execute_category(category_list[category_index])
                    else:
                        print(f"❌ Índice de categoría fuera de rango: {choice}")
                elif choice == '7':
                    self.execute_all_modules()
                elif choice == '8':
                    self.show_system_status()
                elif choice == '9':
                    self.show_advanced_config()
                elif choice == '10':
                    await self.start_intelligent_improvement()
                elif choice == '11':
                    await self.start_continuous_optimization()
                elif choice == '12':
                    await self.start_system_evolution()
                elif choice == '13':
                    await self.start_ai_coordination()
                elif choice == '14':
                    await self.eliminate_mock_components()
                elif choice == '15':
                    await self.initialize_permanent_memory()
                else:
                    print(f"❌ Opción '{choice}' no válida. Selecciona 0-15.")
                    
                input("\nPresiona Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\n🔷 Sistema STARK desconectado")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Punto de entrada principal"""
    try:
        launcher = StarkLauncher()
        asyncio.run(launcher.run())
    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    main()
