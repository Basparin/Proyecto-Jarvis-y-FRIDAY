"""
STARK INDUSTRIES - Decision Maker
Motor avanzado de toma de decisiones con inteligencia adaptativa
Núcleo de razonamiento estratégico para sistema STARK
"""
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import asyncio
from enum import Enum

class DecisionPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class DecisionMaker:
    """
    Motor de decisiones inteligente para sistema STARK
    Toma decisiones complejas basadas en múltiples factores
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.decision_history = []
        self.learning_factors = {}
        self.decision_rules = self._initialize_decision_rules()
        self.status = "INITIALIZED"
        self._initialize()
    
    def _initialize(self):
        """Inicializa el motor de decisiones"""
        print("🧠 Inicializando motor de decisiones STARK...")
        self.status = "ACTIVE"
        print("✅ Motor de decisiones activo y listo")
    
    def _initialize_decision_rules(self) -> Dict[str, Any]:
        """Inicializa reglas de decisión base"""
        return {
            "safety_first": {"weight": 0.9, "priority": DecisionPriority.CRITICAL},
            "efficiency": {"weight": 0.8, "priority": DecisionPriority.HIGH},
            "user_preference": {"weight": 0.7, "priority": DecisionPriority.HIGH},
            "resource_optimization": {"weight": 0.6, "priority": DecisionPriority.MEDIUM},
            "learning_opportunity": {"weight": 0.5, "priority": DecisionPriority.MEDIUM}
        }
    
    async def make_decision(self, context: Dict[str, Any], options: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Toma una decisión basada en contexto y opciones disponibles"""
        try:
            decision_id = f"DEC_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:15]}"
            
            print(f"🤔 Analizando decisión {decision_id}...")
            
            # Evaluar cada opción
            evaluated_options = []
            for option in options:
                score = await self._evaluate_option(option, context)
                evaluated_options.append({
                    "option": option,
                    "score": score,
                    "factors": self._get_evaluation_factors(option, context)
                })
            
            # Seleccionar mejor opción
            best_option = max(evaluated_options, key=lambda x: x["score"])
            
            # Crear decisión
            decision = {
                "id": decision_id,
                "timestamp": datetime.now().isoformat(),
                "context": context,
                "selected_option": best_option["option"],
                "confidence": best_option["score"],
                "reasoning": self._generate_reasoning(best_option, evaluated_options),
                "alternatives": [opt for opt in evaluated_options if opt != best_option]
            }
            
            # Registrar decisión
            self.decision_history.append(decision)
            
            print(f"✅ Decisión tomada: {decision['reasoning']['summary']}")
            return decision
            
        except Exception as e:
            print(f"❌ Error en toma de decisión: {e}")
            return {"error": str(e), "fallback": True}
    
    async def _evaluate_option(self, option: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Evalúa una opción específica"""
        total_score = 0.0
        total_weight = 0.0
        
        for rule_name, rule_config in self.decision_rules.items():
            rule_score = await self._apply_decision_rule(rule_name, option, context)
            weight = rule_config["weight"]
            
            total_score += rule_score * weight
            total_weight += weight
        
        # Normalizar score
        normalized_score = total_score / total_weight if total_weight > 0 else 0
        
        # Aplicar factores de aprendizaje
        learning_bonus = self._calculate_learning_bonus(option, context)
        
        return min(1.0, normalized_score + learning_bonus)
    
    async def _apply_decision_rule(self, rule_name: str, option: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Aplica una regla de decisión específica"""
        if rule_name == "safety_first":
            return self._evaluate_safety(option, context)
        elif rule_name == "efficiency":
            return self._evaluate_efficiency(option, context)
        elif rule_name == "user_preference":
            return self._evaluate_user_preference(option, context)
        elif rule_name == "resource_optimization":
            return self._evaluate_resource_usage(option, context)
        elif rule_name == "learning_opportunity":
            return self._evaluate_learning_potential(option, context)
        else:
            return 0.5  # Neutral score for unknown rules
    
    def _evaluate_safety(self, option: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Evalúa factor de seguridad"""
        safety_indicators = option.get("safety_level", 0.8)
        risk_factors = option.get("risk_factors", [])
        
        safety_score = safety_indicators - (len(risk_factors) * 0.1)
        return max(0.0, min(1.0, safety_score))
    
    def _evaluate_efficiency(self, option: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Evalúa eficiencia de la opción"""
        time_cost = option.get("time_cost", 1.0)
        resource_cost = option.get("resource_cost", 1.0)
        expected_benefit = option.get("expected_benefit", 1.0)
        
        efficiency = expected_benefit / (time_cost + resource_cost)
        return min(1.0, efficiency / 2.0)  # Normalizar
    
    def _evaluate_user_preference(self, option: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Evalúa preferencias del usuario"""
        user_prefs = context.get("user_preferences", {})
        option_alignment = option.get("user_alignment", 0.7)
        
        # Calcular alineación con preferencias históricas
        historical_preference = self._get_historical_preference(option.get("type", "unknown"))
        
        return (option_alignment + historical_preference) / 2.0
    
    def _evaluate_resource_usage(self, option: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Evalúa uso de recursos"""
        cpu_usage = option.get("cpu_cost", 0.5)
        memory_usage = option.get("memory_cost", 0.5)
        available_resources = context.get("available_resources", {"cpu": 0.8, "memory": 0.8})
        
        cpu_score = 1.0 - (cpu_usage / available_resources.get("cpu", 1.0))
        memory_score = 1.0 - (memory_usage / available_resources.get("memory", 1.0))
        
        return (cpu_score + memory_score) / 2.0
    
    def _evaluate_learning_potential(self, option: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Evalúa potencial de aprendizaje"""
        novelty = option.get("novelty", 0.5)
        learning_value = option.get("learning_value", 0.5)
        
        return (novelty + learning_value) / 2.0
    
    def _calculate_learning_bonus(self, option: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Calcula bonus por aprendizaje previo"""
        option_type = option.get("type", "unknown")
        
        if option_type in self.learning_factors:
            success_rate = self.learning_factors[option_type]["success_rate"]
            return (success_rate - 0.5) * 0.1  # Bonus/penalty pequeño
        
        return 0.0
    
    def _get_historical_preference(self, option_type: str) -> float:
        """Obtiene preferencia histórica para tipo de opción"""
        if not self.decision_history:
            return 0.7  # Default neutral-positive
        
        # Analizar decisiones históricas
        type_decisions = [d for d in self.decision_history if d.get("selected_option", {}).get("type") == option_type]
        
        if not type_decisions:
            return 0.7
        
        # Calcular éxito promedio
        success_scores = [d.get("confidence", 0.5) for d in type_decisions]
        return sum(success_scores) / len(success_scores)
    
    def _get_evaluation_factors(self, option: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, float]:
        """Obtiene factores de evaluación detallados"""
        return {
            "safety": self._evaluate_safety(option, context),
            "efficiency": self._evaluate_efficiency(option, context),
            "user_preference": self._evaluate_user_preference(option, context),
            "resource_optimization": self._evaluate_resource_usage(option, context),
            "learning_potential": self._evaluate_learning_potential(option, context)
        }
    
    def _generate_reasoning(self, best_option: Dict[str, Any], all_options: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Genera explicación del razonamiento"""
        factors = best_option["factors"]
        dominant_factor = max(factors.items(), key=lambda x: x[1])
        
        return {
            "summary": f"Selected based on {dominant_factor[0]} (score: {dominant_factor[1]:.2f})",
            "confidence": best_option["score"],
            "dominant_factor": dominant_factor[0],
            "factor_scores": factors,
            "alternatives_considered": len(all_options)
        }
    
    async def learn_from_outcome(self, decision_id: str, outcome: Dict[str, Any]):
        """Aprende del resultado de una decisión"""
        # Encontrar decisión
        decision = next((d for d in self.decision_history if d["id"] == decision_id), None)
        
        if not decision:
            print(f"⚠️ Decisión {decision_id} no encontrada")
            return
        
        option_type = decision["selected_option"].get("type", "unknown")
        success = outcome.get("success", False)
        
        # Actualizar factores de aprendizaje
        if option_type not in self.learning_factors:
            self.learning_factors[option_type] = {"success_count": 0, "total_count": 0, "success_rate": 0.5}
        
        self.learning_factors[option_type]["total_count"] += 1
        if success:
            self.learning_factors[option_type]["success_count"] += 1
        
        # Recalcular tasa de éxito
        factor = self.learning_factors[option_type]
        factor["success_rate"] = factor["success_count"] / factor["total_count"]
        
        print(f"📚 Aprendizaje actualizado para {option_type}: {factor['success_rate']:.2f}")
    
    def get_decision_analytics(self) -> Dict[str, Any]:
        """Obtiene analíticas de decisiones"""
        if not self.decision_history:
            return {"total_decisions": 0, "analytics": "No decisions recorded"}
        
        total_decisions = len(self.decision_history)
        avg_confidence = sum(d.get("confidence", 0) for d in self.decision_history) / total_decisions
        
        # Análisis por tipo
        type_analysis = {}
        for decision in self.decision_history:
            option_type = decision.get("selected_option", {}).get("type", "unknown")
            if option_type not in type_analysis:
                type_analysis[option_type] = {"count": 0, "avg_confidence": 0}
            type_analysis[option_type]["count"] += 1
        
        return {
            "total_decisions": total_decisions,
            "average_confidence": avg_confidence,
            "learning_factors": self.learning_factors,
            "type_distribution": type_analysis,
            "status": self.status
        }

def create_decision_maker() -> DecisionMaker:
    """Crea motor de decisiones optimizado para STARK"""
    return DecisionMaker()

if __name__ == "__main__":
    print("🧠 STARK Decision Maker - Prueba independiente")
    dm = create_decision_maker()
    
    # Prueba de decisión
    test_context = {"user_preferences": {"speed": 0.8}, "available_resources": {"cpu": 0.7, "memory": 0.9}}
    test_options = [
        {"type": "fast", "time_cost": 0.3, "resource_cost": 0.8, "expected_benefit": 1.0},
        {"type": "balanced", "time_cost": 0.6, "resource_cost": 0.5, "expected_benefit": 0.9}
    ]
    
    decision_result = asyncio.run(dm.make_decision(test_context, test_options))
    print(f"✅ Decisión de prueba completada")
    print(dm.get_decision_analytics())
