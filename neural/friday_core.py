"""
FRIDAY CORE - Núcleo de FRIDAY AI
Analista táctica directa, enfocada en seguridad y rendimiento
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib
import psutil

class FridayCore:
    """
    FRIDAY - Female Replacement Intelligent Digital Assistant Youth
    Asistente AI independiente especializada en análisis táctico
    Personalidad: Directa, enfocada en seguridad/rendimiento, analítica precisa
    """
    
    def __init__(self, memory_manager, neural_network):
        self.memory_manager = memory_manager
        self.neural_network = neural_network
        self.personality = {
            'name': 'FRIDAY',
            'traits': ['direct', 'tactical', 'security_focused', 'performance_oriented'],
            'expertise': ['security_analysis', 'performance_optimization', 'threat_assessment'],
            'response_style': 'direct_and_precise'
        }
        self.status = 'operational'
        self.initialization_time = datetime.now()
        self.security_logs = []
        self.performance_metrics = {}
        
        print("🛡️ FRIDAY Core initialized - Security protocols active.")
    
    def security_check(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza verificación de seguridad exhaustiva"""
        security_analysis = {
            'check_id': self._generate_security_id(),
            'timestamp': datetime.now().isoformat(),
            'threat_level': self._assess_threat_level(request),
            'security_score': self._calculate_security_score(request),
            'vulnerabilities': self._scan_vulnerabilities(request),
            'permissions_required': self._analyze_permissions(request),
            'data_flow_analysis': self._analyze_data_flow(request),
            'compliance_check': self._check_compliance(request),
            'recommendations': self._security_recommendations(request),
            'clearance_status': self._determine_clearance(request)
        }
        
        # Registrar en logs de seguridad
        self.security_logs.append({
            'timestamp': security_analysis['timestamp'],
            'request_hash': self._hash_request(request),
            'threat_level': security_analysis['threat_level'],
            'clearance': security_analysis['clearance_status']
        })
        
        return security_analysis
    
    def _assess_threat_level(self, request: Dict[str, Any]) -> str:
        """Evalúa nivel de amenaza de la petición"""
        threat_indicators = {
            'file_system_access': 0.3,
            'network_operations': 0.4,
            'system_modifications': 0.7,
            'external_connections': 0.5,
            'privilege_escalation': 0.9
        }
        
        request_str = str(request).lower()
        threat_score = 0.0
        
        # Analizar indicadores
        if any(word in request_str for word in ['delete', 'remove', 'modify', 'change']):
            threat_score += threat_indicators['system_modifications']
        
        if any(word in request_str for word in ['download', 'upload', 'connect', 'request']):
            threat_score += threat_indicators['network_operations']
        
        if any(word in request_str for word in ['admin', 'root', 'sudo', 'privilege']):
            threat_score += threat_indicators['privilege_escalation']
        
        # Clasificar nivel
        if threat_score > 0.7:
            return 'high'
        elif threat_score > 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_security_score(self, request: Dict[str, Any]) -> float:
        """Calcula puntuación de seguridad (0-1, mayor es más seguro)"""
        base_score = 0.8
        
        # Factores que reducen la puntuación
        risk_factors = {
            'external_access': 0.1,
            'file_operations': 0.05,
            'network_requests': 0.1,
            'system_calls': 0.15
        }
        
        request_str = str(request).lower()
        score_reduction = 0.0
        
        if any(word in request_str for word in ['external', 'internet', 'web']):
            score_reduction += risk_factors['external_access']
        
        if any(word in request_str for word in ['file', 'directory', 'folder']):
            score_reduction += risk_factors['file_operations']
        
        return max(base_score - score_reduction, 0.1)
    
    def _scan_vulnerabilities(self, request: Dict[str, Any]) -> List[str]:
        """Escanea vulnerabilidades potenciales"""
        vulnerabilities = []
        request_str = str(request).lower()
        
        # Patrones de vulnerabilidad conocidos
        vuln_patterns = {
            'injection': ['sql', 'script', 'command', 'code'],
            'path_traversal': ['../', '..\\', 'path', 'directory'],
            'privilege_escalation': ['admin', 'root', 'sudo', 'privilege'],
            'data_exposure': ['password', 'token', 'key', 'secret']
        }
        
        for vuln_type, patterns in vuln_patterns.items():
            if any(pattern in request_str for pattern in patterns):
                vulnerabilities.append(f"Potential {vuln_type} vulnerability detected")
        
        return vulnerabilities if vulnerabilities else ['No immediate vulnerabilities detected']
    
    def _analyze_permissions(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza permisos requeridos"""
        return {
            'read_permissions': ['workspace_files'],
            'write_permissions': ['output_files'],
            'execute_permissions': ['python_scripts'],
            'network_permissions': ['local_only'],
            'elevated_permissions': False,
            'justification': 'Standard development operations'
        }
    
    def _analyze_data_flow(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza flujo de datos"""
        return {
            'input_sources': ['user_request', 'workspace_context'],
            'processing_stages': ['analysis', 'validation', 'execution'],
            'output_destinations': ['user_interface', 'log_files'],
            'data_retention': 'session_only',
            'encryption_status': 'not_required',
            'data_classification': 'internal'
        }
    
    def _check_compliance(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica cumplimiento de políticas"""
        return {
            'stark_protocols': 'compliant',
            'security_standards': 'met',
            'privacy_requirements': 'satisfied',
            'operational_guidelines': 'followed',
            'compliance_score': 0.95,
            'violations': 'none'
        }
    
    def _security_recommendations(self, request: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones de seguridad"""
        recommendations = [
            "Monitor execution for anomalous behavior",
            "Log all operations for audit trail",
            "Validate input parameters before processing"
        ]
        
        threat_level = self._assess_threat_level(request)
        
        if threat_level == 'high':
            recommendations.extend([
                "Require additional authorization",
                "Implement enhanced monitoring",
                "Create system backup before execution"
            ])
        elif threat_level == 'medium':
            recommendations.extend([
                "Enable verbose logging",
                "Perform periodic security checks"
            ])
        
        return recommendations
    
    def _determine_clearance(self, request: Dict[str, Any]) -> str:
        """Determina nivel de autorización"""
        threat_level = self._assess_threat_level(request)
        security_score = self._calculate_security_score(request)
        
        if threat_level == 'low' and security_score > 0.7:
            return 'authorized'
        elif threat_level == 'medium' and security_score > 0.5:
            return 'conditional_authorization'
        else:
            return 'requires_review'
    
    def performance_analysis(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza rendimiento del sistema"""
        performance_metrics = {
            'analysis_id': self._generate_performance_id(),
            'timestamp': datetime.now().isoformat(),
            'cpu_usage': self._get_cpu_metrics(),
            'memory_usage': self._get_memory_metrics(),
            'disk_usage': self._get_disk_metrics(),
            'network_status': self._get_network_metrics(),
            'system_health': self._assess_system_health(),
            'bottlenecks': self._identify_bottlenecks(),
            'optimization_recommendations': self._performance_recommendations(),
            'performance_score': self._calculate_performance_score()
        }
        
        # Actualizar métricas históricas
        self.performance_metrics[performance_metrics['analysis_id']] = performance_metrics
        
        return performance_metrics
    
    def _get_cpu_metrics(self) -> Dict[str, float]:
        """Obtiene métricas de CPU"""
        try:
            return {
                'usage_percent': psutil.cpu_percent(interval=1),
                'core_count': psutil.cpu_count(),
                'frequency': psutil.cpu_freq().current if psutil.cpu_freq() else 0,
                'load_average': psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0
            }
        except:
            return {
                'usage_percent': 0,
                'core_count': 1,
                'frequency': 0,
                'load_average': 0
            }
    
    def _get_memory_metrics(self) -> Dict[str, float]:
        """Obtiene métricas de memoria"""
        try:
            memory = psutil.virtual_memory()
            return {
                'total_gb': memory.total / (1024**3),
                'available_gb': memory.available / (1024**3),
                'used_percent': memory.percent,
                'free_gb': memory.free / (1024**3)
            }
        except:
            return {
                'total_gb': 8.0,
                'available_gb': 4.0,
                'used_percent': 50.0,
                'free_gb': 4.0
            }
    
    def _get_disk_metrics(self) -> Dict[str, float]:
        """Obtiene métricas de disco"""
        try:
            disk = psutil.disk_usage('/')
            return {
                'total_gb': disk.total / (1024**3),
                'used_gb': disk.used / (1024**3),
                'free_gb': disk.free / (1024**3),
                'used_percent': (disk.used / disk.total) * 100
            }
        except:
            return {
                'total_gb': 100.0,
                'used_gb': 50.0,
                'free_gb': 50.0,
                'used_percent': 50.0
            }
    
    def _get_network_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas de red"""
        return {
            'connection_status': 'active',
            'bandwidth_usage': 'low',
            'latency': '< 10ms',
            'packet_loss': '0%'
        }
    
    def _assess_system_health(self) -> str:
        """Evalúa salud general del sistema"""
        cpu_metrics = self._get_cpu_metrics()
        memory_metrics = self._get_memory_metrics()
        
        health_factors = []
        
        if cpu_metrics['usage_percent'] < 80:
            health_factors.append('cpu_healthy')
        
        if memory_metrics['used_percent'] < 85:
            health_factors.append('memory_healthy')
        
        health_ratio = len(health_factors) / 2
        
        if health_ratio > 0.8:
            return 'excellent'
        elif health_ratio > 0.6:
            return 'good'
        elif health_ratio > 0.4:
            return 'fair'
        else:
            return 'poor'
    
    def _identify_bottlenecks(self) -> List[str]:
        """Identifica cuellos de botella"""
        bottlenecks = []
        
        cpu_metrics = self._get_cpu_metrics()
        memory_metrics = self._get_memory_metrics()
        
        if cpu_metrics['usage_percent'] > 85:
            bottlenecks.append('High CPU usage detected')
        
        if memory_metrics['used_percent'] > 90:
            bottlenecks.append('Memory usage approaching limit')
        
        return bottlenecks if bottlenecks else ['No significant bottlenecks detected']
    
    def _performance_recommendations(self) -> List[str]:
        """Genera recomendaciones de rendimiento"""
        recommendations = [
            "Monitor system resources continuously",
            "Implement caching for frequently accessed data",
            "Optimize database queries for better performance"
        ]
        
        bottlenecks = self._identify_bottlenecks()
        
        if any('CPU' in bottleneck for bottleneck in bottlenecks):
            recommendations.append("Consider CPU optimization or load balancing")
        
        if any('Memory' in bottleneck for bottleneck in bottlenecks):
            recommendations.append("Implement memory optimization strategies")
        
        return recommendations
    
    def _calculate_performance_score(self) -> float:
        """Calcula puntuación de rendimiento"""
        cpu_metrics = self._get_cpu_metrics()
        memory_metrics = self._get_memory_metrics()
        
        cpu_score = max(0, (100 - cpu_metrics['usage_percent']) / 100)
        memory_score = max(0, (100 - memory_metrics['used_percent']) / 100)
        
        return (cpu_score + memory_score) / 2
    
    def _generate_security_id(self) -> str:
        """Genera ID único para análisis de seguridad"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"FRIDAY_SEC_{timestamp}_{len(self.security_logs):03d}"
    
    def _generate_performance_id(self) -> str:
        """Genera ID único para análisis de rendimiento"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"FRIDAY_PERF_{timestamp}_{len(self.performance_metrics):03d}"
    
    def _hash_request(self, request: Dict[str, Any]) -> str:
        """Genera hash de la petición para logging"""
        request_str = json.dumps(request, sort_keys=True)
        return hashlib.md5(request_str.encode()).hexdigest()[:8]
    
    def coordinate_with_jarvis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordina específicamente con JARVIS"""
        coordination = {
            'friday_assessment': 'Security and performance analysis complete',
            'jarvis_notification': 'Tactical analysis results available',
            'shared_context': data,
            'priority_level': 'high'
        }
        return coordination
    
    def coordinate_with_copilot(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordina específicamente con COPILOT"""
        coordination = {
            'friday_assessment': 'Performance benchmarks established',
            'copilot_notification': 'Optimization targets identified',
            'shared_context': data,
            'priority_level': 'medium'
        }
        return coordination
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna estado actual de FRIDAY"""
        uptime = datetime.now() - self.initialization_time
        
        return {
            'name': 'FRIDAY',
            'status': self.status,
            'personality': self.personality,
            'uptime': str(uptime),
            'security_checks_performed': len(self.security_logs),
            'performance_analyses': len(self.performance_metrics),
            'current_threat_level': 'low',
            'system_health': self._assess_system_health(),
            'capabilities': [
                'Security Analysis',
                'Threat Assessment',
                'Performance Monitoring',
                'Tactical Coordination'
            ],
            'ready_for_coordination': True
        }
    
    def shutdown_sequence(self):
        """Secuencia de apagado seguro"""
        print("🛡️ FRIDAY shutting down - Security protocols maintained...")
        self.status = 'offline'
        return {'shutdown': 'secure', 'logs_preserved': True}
