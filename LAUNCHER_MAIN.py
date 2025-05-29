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
        if config_choice == '1':
            print("📊 Configurando umbrales de optimización...")
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
            
            coordinator = StarkAutoprogrammerCoordinator()
            
            print("🚀 Iniciando análisis y auto-mejora...")
            improvement_result = await coordinator.self_improve_system()
            
            print("\n✅ AUTO-MEJORA COMPLETADA")
            print(f"Mejoras aplicadas: {improvement_result.get('improvements_applied', 0)}")
            print(f"Ganancia de rendimiento: {improvement_result.get('performance_gain', 0):.1f}%")
            print(f"Nuevas capacidades: {improvement_result.get('new_capabilities', 0)}")
            
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
            
            print("🎯 ¿Iniciar optimización continua en background?")
            choice = input("(s/N): ").lower()
            
            if choice in ['s', 'si', 'sí', 'y', 'yes']:
                print("🚀 Iniciando optimización inteligente...")
                # Ejecutar en background
                task = asyncio.create_task(optimizer.start_intelligent_optimization())
                print("✅ Optimización continua activada en background")
                
                # Mostrar reporte inicial
                await asyncio.sleep(2)  # Esperar un poco para que inicie
                print("\n📊 REPORTE INICIAL:")
                print(optimizer.get_optimization_report())
            else:
                print("❌ Optimización continua cancelada")
                
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
            
            evolution_engine = StarkSelfEvolutionEngine()
            
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
    
    async def run(self):
        """Bucle principal del sistema"""
        while True:
            self.display_dashboard()
            
            try:
                choice = input("\n🔷 Selecciona una opción: ").strip()
                
                if choice == '0':
                    print("\n🔷 Apagando sistema STARK...")
                    break
                elif choice in '123456':
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
                else:
                    print(f"❌ Opción '{choice}' no válida. Selecciona 0-12.")
                    
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
