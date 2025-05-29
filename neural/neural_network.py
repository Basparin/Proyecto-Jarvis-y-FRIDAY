"""
Neural Network Implementation - STARK Industries
Red neuronal funcional para procesamiento AI avanzado
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import Dict, List, Any, Optional, Tuple

class StarkNeuralNetwork(nn.Module):
    """Red neuronal avanzada para sistema STARK"""
    
    def __init__(self, input_size: int = 512, hidden_sizes: List[int] = [256, 128, 64], output_size: int = 10):
        super(StarkNeuralNetwork, self).__init__()
        
        # Arquitectura de red
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.extend([
                nn.Linear(prev_size, hidden_size),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.BatchNorm1d(hidden_size)
            ])
            prev_size = hidden_size
        
        layers.append(nn.Linear(prev_size, output_size))
        self.network = nn.Sequential(*layers)
        
        # Optimizador y función de pérdida
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        self.criterion = nn.CrossEntropyLoss()
        
        # Estado de entrenamiento
        self.training_history = []
        self.is_trained = False
        
        print("🧠 STARK Neural Network - Inicializada")
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass de la red"""
        return self.network(x)
    
    def train_network(self, train_data: torch.Tensor, train_labels: torch.Tensor, epochs: int = 100) -> Dict[str, List[float]]:
        """Entrena la red neuronal"""
        self.train()
        history = {"loss": [], "accuracy": []}
        
        for epoch in range(epochs):
            self.optimizer.zero_grad()
            
            # Forward pass
            outputs = self(train_data)
            loss = self.criterion(outputs, train_labels)
            
            # Backward pass
            loss.backward()
            self.optimizer.step()
            
            # Métricas
            with torch.no_grad():
                predicted = torch.argmax(outputs, dim=1)
                accuracy = (predicted == train_labels).float().mean()
                
                history["loss"].append(loss.item())
                history["accuracy"].append(accuracy.item())
            
            if epoch % 10 == 0:
                print(f"Epoch {epoch}: Loss={loss.item():.4f}, Accuracy={accuracy.item():.4f}")
        
        self.is_trained = True
        self.training_history = history
        print("✅ Neural Network entrenada exitosamente")
        return history
    
    def predict(self, data: torch.Tensor) -> torch.Tensor:
        """Realiza predicciones"""
        self.eval()
        with torch.no_grad():
            outputs = self(data)
            return torch.softmax(outputs, dim=1)
    
    def save_model(self, path: str):
        """Guarda el modelo entrenado"""
        torch.save({
            'model_state_dict': self.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'training_history': self.training_history,
            'is_trained': self.is_trained
        }, path)
        print(f"✅ Modelo guardado en: {path}")
    
    def load_model(self, path: str):
        """Carga un modelo entrenado"""
        checkpoint = torch.load(path)
        self.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.training_history = checkpoint['training_history']
        self.is_trained = checkpoint['is_trained']
        print(f"✅ Modelo cargado desde: {path}")

# Función de utilidad para crear red neuronal
def create_stark_neural_network(config: Dict[str, Any] = None) -> StarkNeuralNetwork:
    """Crea una red neuronal STARK con configuración personalizada"""
    if config is None:
        config = {
            "input_size": 512,
            "hidden_sizes": [256, 128, 64],
            "output_size": 10
        }
    
    return StarkNeuralNetwork(**config)
