"""
STARK INDUSTRIES - Learning Engine
Motor de aprendizaje avanzado para el sistema neural
Implementación real con capacidades de ML y adaptación
"""

import os
import json
import numpy as np
import pickle
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LearningPattern:
    """Representa un patrón aprendido"""
    pattern_id: str
    pattern_type: str
    data: Dict[str, Any]
    confidence: float
    frequency: int
    last_used: datetime
    source: str

class LearningStrategy(ABC):
    """Estrategia abstracta de aprendizaje"""
    
    @abstractmethod
    def learn(self, data: Any) -> LearningPattern:
        pass
    
    @abstractmethod
    def predict(self, input_data: Any) -> Tuple[Any, float]:
        pass

class PatternRecognitionStrategy(LearningStrategy):
    """Estrategia de reconocimiento de patrones"""
    
    def __init__(self):
        self.patterns = {}
        self.threshold = 0.7
    
    def learn(self, data: Any) -> LearningPattern:
        """Aprende patrones de los datos"""
        pattern_id = f"pattern_{len(self.patterns)}"
        
        pattern = LearningPattern(
            pattern_id=pattern_id,
            pattern_type="sequence",
            data={"sequence": data, "features": self._extract_features(data)},
            confidence=1.0,
            frequency=1,
            last_used=datetime.now(),
            source="pattern_recognition"
        )
        
        self.patterns[pattern_id] = pattern
        logger.info(f"Nuevo patrón aprendido: {pattern_id}")
        return pattern
    
    def predict(self, input_data: Any) -> Tuple[Any, float]:
        """Predice basado en patrones aprendidos"""
        best_match = None
        best_score = 0.0
        
        input_features = self._extract_features(input_data)
        
        for pattern in self.patterns.values():
            similarity = self._calculate_similarity(input_features, pattern.data["features"])
            if similarity > best_score:
                best_score = similarity
                best_match = pattern
        
        if best_match and best_score > self.threshold:
            return best_match.data["sequence"], best_score
        
        return None, 0.0
    
    def _extract_features(self, data: Any) -> Dict[str, Any]:
        """Extrae características de los datos"""
        if isinstance(data, str):
            return {
                "length": len(data),
                "words": len(data.split()),
                "chars": list(set(data.lower()))
            }
        elif isinstance(data, (list, tuple)):
            return {
                "length": len(data),
                "type": "sequence",
                "unique_items": len(set(data)) if all(isinstance(x, (str, int, float)) for x in data) else 0
            }
        else:
            return {"type": str(type(data)), "value": str(data)}
    
    def _calculate_similarity(self, features1: Dict, features2: Dict) -> float:
        """Calcula similitud entre características"""
        common_keys = set(features1.keys()) & set(features2.keys())
        if not common_keys:
            return 0.0
        
        score = 0.0
        for key in common_keys:
            if features1[key] == features2[key]:
                score += 1.0
            elif isinstance(features1[key], (int, float)) and isinstance(features2[key], (int, float)):
                diff = abs(features1[key] - features2[key])
                max_val = max(features1[key], features2[key])
                if max_val > 0:
                    score += 1.0 - (diff / max_val)
        
        return score / len(common_keys)

class AdaptiveLearningStrategy(LearningStrategy):
    """Estrategia de aprendizaje adaptativo"""
    
    def __init__(self):
        self.learning_rate = 0.1
        self.knowledge_base = {}
        self.adaptation_history = []
    
    def learn(self, data: Any) -> LearningPattern:
        """Aprendizaje adaptativo basado en feedback"""
        pattern_id = f"adaptive_{len(self.knowledge_base)}"
        
        # Analizar el contexto de los datos
        context = self._analyze_context(data)
        
        pattern = LearningPattern(
            pattern_id=pattern_id,
            pattern_type="adaptive",
            data={"input": data, "context": context},
            confidence=0.5,  # Comienza con confianza media
            frequency=1,
            last_used=datetime.now(),
            source="adaptive_learning"
        )
        
        self.knowledge_base[pattern_id] = pattern
        self._adapt_learning_rate(pattern)
        
        logger.info(f"Patrón adaptativo creado: {pattern_id}")
        return pattern
    
    def predict(self, input_data: Any) -> Tuple[Any, float]:
        """Predicción adaptativa"""
        context = self._analyze_context(input_data)
        best_match = None
        best_confidence = 0.0
        
        for pattern in self.knowledge_base.values():
            compatibility = self._check_context_compatibility(context, pattern.data["context"])
            adjusted_confidence = pattern.confidence * compatibility
            
            if adjusted_confidence > best_confidence:
                best_confidence = adjusted_confidence
                best_match = pattern
        
        if best_match and best_confidence > 0.3:
            # Actualizar frecuencia de uso
            best_match.frequency += 1
            best_match.last_used = datetime.now()
            return best_match.data["input"], best_confidence
        
        return None, 0.0
    
    def _analyze_context(self, data: Any) -> Dict[str, Any]:
        """Analiza el contexto de los datos"""
        return {
            "timestamp": datetime.now().isoformat(),
            "data_type": str(type(data)),
            "complexity": self._estimate_complexity(data),
            "environment": "stark_system"
        }
    
    def _estimate_complexity(self, data: Any) -> str:
        """Estima la complejidad de los datos"""
        if isinstance(data, str):
            return "low" if len(data) < 100 else "medium" if len(data) < 1000 else "high"
        elif isinstance(data, (list, tuple)):
            return "low" if len(data) < 10 else "medium" if len(data) < 100 else "high"
        else:
            return "medium"
    
    def _check_context_compatibility(self, context1: Dict, context2: Dict) -> float:
        """Verifica compatibilidad entre contextos"""
        if context1["data_type"] != context2["data_type"]:
            return 0.3
        
        if context1["complexity"] == context2["complexity"]:
            return 1.0
        else:
            return 0.6
    
    def _adapt_learning_rate(self, pattern: LearningPattern):
        """Adapta la tasa de aprendizaje"""
        self.adaptation_history.append({
            "pattern_id": pattern.pattern_id,
            "timestamp": datetime.now(),
            "learning_rate": self.learning_rate
        })
        
        # Ajustar tasa de aprendizaje basada en el historial
        if len(self.adaptation_history) > 10:
            recent_patterns = self.adaptation_history[-10:]
            success_rate = sum(1 for p in recent_patterns if p["learning_rate"] > 0.05) / len(recent_patterns)
            
            if success_rate > 0.8:
                self.learning_rate = min(0.2, self.learning_rate * 1.1)
            else:
                self.learning_rate = max(0.01, self.learning_rate * 0.9)

class StarkLearningEngine:
    """
    Motor de aprendizaje principal del sistema STARK
    Coordina múltiples estrategias de aprendizaje
    """
    
    def __init__(self, data_path: str = "learning_data"):
        self.data_path = data_path
        self.strategies = {
            "pattern_recognition": PatternRecognitionStrategy(),
            "adaptive_learning": AdaptiveLearningStrategy()
        }
        
        self.learning_history = []
        self.performance_metrics = {
            "total_patterns": 0,
            "successful_predictions": 0,
            "failed_predictions": 0,
            "learning_accuracy": 0.0
        }
        
        self.active = True
        self._ensure_data_directory()
        self._load_previous_learning()
        
        logger.info("🧠 STARK Learning Engine inicializado")
    
    def _ensure_data_directory(self):
        """Asegura que el directorio de datos existe"""
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
    
    def learn_from_input(self, data: Any, strategy: str = "adaptive_learning") -> bool:
        """Aprende de una entrada de datos"""
        try:
            if strategy not in self.strategies:
                logger.warning(f"Estrategia desconocida: {strategy}")
                strategy = "adaptive_learning"
            
            pattern = self.strategies[strategy].learn(data)
            
            self.learning_history.append({
                "pattern_id": pattern.pattern_id,
                "strategy": strategy,
                "timestamp": datetime.now(),
                "data_type": str(type(data))
            })
            
            self.performance_metrics["total_patterns"] += 1
            self._save_learning_state()
            
            logger.info(f"Aprendizaje completado usando {strategy}")
            return True
            
        except Exception as e:
            logger.error(f"Error en aprendizaje: {e}")
            return False
    
    def predict(self, input_data: Any, strategy: str = None) -> Tuple[Any, float, str]:
        """Realiza predicción usando la mejor estrategia"""
        try:
            best_result = None
            best_confidence = 0.0
            best_strategy = None
            
            strategies_to_try = [strategy] if strategy else self.strategies.keys()
            
            for strat_name in strategies_to_try:
                if strat_name in self.strategies:
                    result, confidence = self.strategies[strat_name].predict(input_data)
                    
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_result = result
                        best_strategy = strat_name
            
            # Actualizar métricas
            if best_result is not None:
                self.performance_metrics["successful_predictions"] += 1
            else:
                self.performance_metrics["failed_predictions"] += 1
            
            self._update_accuracy()
            
            return best_result, best_confidence, best_strategy or "none"
            
        except Exception as e:
            logger.error(f"Error en predicción: {e}")
            return None, 0.0, "error"
    
    def learn_from_interaction(self, user_input: str, system_response: str, feedback: str = None):
        """Aprende de interacciones usuario-sistema"""
        interaction_data = {
            "input": user_input,
            "response": system_response,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        }
        
        # Usar ambas estrategias para aprender
        self.learn_from_input(interaction_data, "pattern_recognition")
        self.learn_from_input(interaction_data, "adaptive_learning")
        
        logger.info("Interacción aprendida y almacenada")
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del aprendizaje"""
        total_predictions = (self.performance_metrics["successful_predictions"] + 
                           self.performance_metrics["failed_predictions"])
        
        return {
            "total_patterns_learned": self.performance_metrics["total_patterns"],
            "total_predictions": total_predictions,
            "successful_predictions": self.performance_metrics["successful_predictions"],
            "failed_predictions": self.performance_metrics["failed_predictions"],
            "learning_accuracy": self.performance_metrics["learning_accuracy"],
            "strategies_available": list(self.strategies.keys()),
            "learning_sessions": len(self.learning_history),
            "last_learning": self.learning_history[-1] if self.learning_history else None
        }
    
    def _update_accuracy(self):
        """Actualiza la precisión del aprendizaje"""
        total = (self.performance_metrics["successful_predictions"] + 
                self.performance_metrics["failed_predictions"])
        
        if total > 0:
            self.performance_metrics["learning_accuracy"] = (
                self.performance_metrics["successful_predictions"] / total
            )
    
    def _save_learning_state(self):
        """Guarda el estado del aprendizaje"""
        try:
            state_file = os.path.join(self.data_path, "learning_state.json")
            state_data = {
                "performance_metrics": self.performance_metrics,
                "learning_history": self.learning_history[-100:],  # Solo últimas 100
                "timestamp": datetime.now().isoformat()
            }
            
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error guardando estado: {e}")
    
    def _load_previous_learning(self):
        """Carga aprendizaje previo"""
        try:
            state_file = os.path.join(self.data_path, "learning_state.json")
            if os.path.exists(state_file):
                with open(state_file, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
                
                self.performance_metrics.update(state_data.get("performance_metrics", {}))
                self.learning_history = state_data.get("learning_history", [])
                
                logger.info("Estado de aprendizaje previo cargado")
                
        except Exception as e:
            logger.error(f"Error cargando estado previo: {e}")
    
    def optimize_learning(self):
        """Optimiza el proceso de aprendizaje"""
        logger.info("🔧 Iniciando optimización del aprendizaje")
        
        # Limpiar patrones antiguos de baja frecuencia
        for strategy in self.strategies.values():
            if hasattr(strategy, 'patterns'):
                old_patterns = []
                for pattern_id, pattern in strategy.patterns.items():
                    days_since_use = (datetime.now() - pattern.last_used).days
                    if days_since_use > 30 and pattern.frequency < 3:
                        old_patterns.append(pattern_id)
                
                for pattern_id in old_patterns:
                    del strategy.patterns[pattern_id]
                
                if old_patterns:
                    logger.info(f"Eliminados {len(old_patterns)} patrones obsoletos")
        
        logger.info("✅ Optimización completada")
    
    def shutdown(self):
        """Cierra el motor de aprendizaje"""
        logger.info("🔌 Cerrando motor de aprendizaje")
        self._save_learning_state()
        self.active = False

# Función principal para crear el motor de aprendizaje
def create_learning_engine(data_path: str = "learning_data") -> StarkLearningEngine:
    """Crea y configura el motor de aprendizaje STARK"""
    return StarkLearningEngine(data_path)

# Función de prueba
def test_learning_engine():
    """Prueba básica del motor de aprendizaje"""
    engine = create_learning_engine()
    
    # Prueba de aprendizaje
    test_data = ["Hello STARK", "System status check", "Initialize neural network"]
    
    for data in test_data:
        engine.learn_from_input(data)
    
    # Prueba de predicción
    result, confidence, strategy = engine.predict("System")
    print(f"Predicción: {result}, Confianza: {confidence}, Estrategia: {strategy}")
    
    # Estadísticas
    stats = engine.get_learning_stats()
    print(f"Estadísticas: {stats}")
    
    engine.shutdown()

if __name__ == "__main__":
    test_learning_engine()