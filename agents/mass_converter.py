# filepath: agents/mass_converter.py
"""
STARK MASS CONVERTER - Ejecutor de Conversión Masiva
Lanza conversión masiva y eficiente de componentes mock → real
"""
import asyncio
import sys
import os
from datetime import datetime

# Agregar directorio padre al path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autoprogrammer_coordinator import StarkAutoprogrammerCoordinator
from integrator_agent import IntegratorAgent

async def main():
    """Función principal de conversión masiva"""
    print("🚀 STARK INDUSTRIES - MASS MOCK CONVERTER")
    print("=" * 50)
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Inicializar coordinador
        coordinator = StarkAutoprogrammerCoordinator()
          # Análisis inicial
        print("\n📊 ANÁLISIS INICIAL DEL SISTEMA...")
        mock_data = coordinator.detect_mock_components()
        mock_components = mock_data['components']
        
        print(f"Componentes mock detectados: {mock_data['total_found']}")
          # Mostrar componentes por prioridad
        high_priority = [c for c in mock_components if c.get("priority", "MEDIUM") == "HIGH"]
        medium_priority = [c for c in mock_components if c.get("priority", "MEDIUM") == "MEDIUM"]
        low_priority = [c for c in mock_components if c.get("priority", "MEDIUM") == "LOW"]
        
        print(f"• Prioridad ALTA: {len(high_priority)}")
        print(f"• Prioridad MEDIA: {len(medium_priority)}")
        print(f"• Prioridad BAJA: {len(low_priority)}")
        
        # Confirmar conversión
        response = input(f"\n¿Proceder con conversión masiva de {len(mock_components)} componentes? (s/N): ")
        
        if response.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Conversión cancelada por el usuario")
            return
        
        # Ejecutar conversión masiva
        print("\n🎯 INICIANDO CONVERSIÓN MASIVA...")
        results = await coordinator.mass_convert_mocks(max_concurrent=3)
        
        # Mostrar reporte final
        print("\n" + coordinator.generate_conversion_report(results))
        
        # Ejecutar análisis post-conversión
        print("\n📊 ANÁLISIS POST-CONVERSIÓN...")
        os.system('python system/state_analyzer.py')
        
        print(f"\n✅ CONVERSIÓN MASIVA COMPLETADA")
        print(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"\n❌ ERROR EN CONVERSIÓN MASIVA: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
