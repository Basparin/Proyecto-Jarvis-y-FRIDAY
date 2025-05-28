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
                    self.execute_category(category_list[int(choice) - 1])
                elif choice == '7':
                    self.execute_all_modules()
                elif choice == '8':
                    self.show_system_status()
                elif choice == '9':
                    print("\n⚙️  Configuración avanzada en desarrollo...")
                else:
                    print("❌ Opción no válida")
                    
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
