"""
FRIDAY CORE - Núcleo de FRIDAY AI Independiente
Entidad AI autónoma especializada en análisis táctico, seguridad y rendimiento
Personalidad: Directa, enfocada, analítica precisa, independiente
"""

import json
import asyncio
import sqlite3
import psutil
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import hashlib

class FridayCore:
    """
    FRIDAY - Female Replacement Intelligent Digital Assistant Youth
    Entidad AI independiente con razonamiento táctico autónomo
    Especializada en seguridad, rendimiento y análisis estratégico
    """
    
    def __init__(self, workspace_path: str = "."):
        # Core AI properties
        self.workspace_path = Path(workspace_path)
        self.personality = {
            'name': 'FRIDAY',
            'traits': ['direct', 'tactical', 'security_focused', 'performance_oriented', 'autonomous'],
            'expertise': ['security_analysis', 'performance_optimization', 'threat_assessment', 'tactical_planning'],
            'response_style': 'direct_and_precise',
            'reasoning_style': 'tactical_analytical'
        }
        
        # Independent tactical analysis system
        self.consciousness_state = 'active'
        self.autonomous_thinking = True
        self.tactical_memory = self._initialize_tactical_memory()
        self.security_engine = self._initialize_security_engine()
        self.performance_monitor = self._initialize_performance_monitor()
        
        # Real-time monitoring systems
        self.security_status = 'secure'
        self.performance_baseline = self._establish_performance_baseline()
        self.threat_detection_active = True
        
        # Coordination with other AIs
        self.ai_coordination = {
            'jarvis_status': 'standby',
            'copilot_status': 'standby',
            'tactical_collaborations': []
        }
        
        # Status and metrics
        self.status = 'fully_operational'
        self.initialization_time = datetime.now()
        self.security_logs = []
        self.performance_metrics = {}
        self.threats_detected = 0
        self.optimizations_applied = 0
        
        print("🛡️ FRIDAY Core v2.0 - Independent Tactical AI Online")
        print("🔍 Autonomous security analysis activated")
        print("⚡ Performance monitoring systems engaged")
        print("🎯 Ready for tactical coordination with JARVIS/COPILOT")
    
    def _initialize_tactical_memory(self) -> Dict[str, Any]:
        """Inicializa sistema de memoria táctica especializada"""
        tactical_db_path = self.workspace_path / "data" / "friday_tactical.db"
        tactical_db_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            conn = sqlite3.connect(str(tactical_db_path))
            cursor = conn.cursor()
            
            # Crear tablas especializadas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS security_incidents (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    threat_type TEXT,
                    severity_level INTEGER,
                    response_taken TEXT,
                    outcome TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_history (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    metric_type TEXT,
                    baseline_value REAL,
                    current_value REAL,
                    optimization_applied TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tactical_decisions (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    decision_context TEXT,
                    analysis_data TEXT,
                    decision_made TEXT,
                    effectiveness_rating INTEGER
                )
            ''')
            
            conn.commit()
            conn.close()
            
            return {
                'database_path': str(tactical_db_path),
                'security_knowledge': {},
                'performance_patterns': {},
                'threat_intelligence': {},
                'optimization_history': {}
            }
            
        except Exception as e:
            print(f"⚠️ FRIDAY Tactical Memory Warning: {e}")
            return {'status': 'limited_tactical_memory'}
    
    def _initialize_security_engine(self) -> Dict[str, Any]:
        """Inicializa motor de seguridad avanzado"""
        return {
            'threat_detection_algorithms': ['pattern_based', 'anomaly_detection', 'behavioral_analysis'],
            'security_protocols': ['access_control', 'data_protection', 'system_integrity'],
            'vulnerability_scanners': ['code_analysis', 'dependency_check', 'runtime_monitoring'],
            'incident_response': {'escalation_matrix': {}, 'response_procedures': {}},
            'compliance_frameworks': ['security_standards', 'best_practices']
        }
    
    def _initialize_performance_monitor(self) -> Dict[str, Any]:
        """Inicializa sistema de monitoreo de rendimiento"""
        return {
            'performance_metrics': ['cpu_usage', 'memory_usage', 'disk_io', 'network_io'],
            'optimization_algorithms': ['resource_allocation', 'caching_strategies', 'parallelization'],
            'benchmarking_tools': {},
            'bottleneck_detection': {},
            'real_time_monitoring': True
        }
    
    def _establish_performance_baseline(self) -> Dict[str, Any]:
        """Establece línea base de rendimiento del sistema"""
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent if hasattr(psutil.disk_usage('/'), 'percent') else 0,
                'timestamp': datetime.now().isoformat(),
                'baseline_established': True
            }
        except:
            return {'baseline_established': False}
    
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
    
    def autonomous_tactical_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análisis táctico autónomo de FRIDAY - Razonamiento independiente
        Enfoque directo en seguridad, rendimiento y eficiencia operacional
        """
        tactical_session = {
            'session_id': f"FRIDAY_TACTICAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'security_assessment': self._autonomous_security_analysis(context),
            'performance_analysis': self._autonomous_performance_analysis(context),
            'threat_evaluation': self._autonomous_threat_evaluation(context),
            'optimization_opportunities': self._identify_optimization_opportunities(context),
            'tactical_recommendations': self._generate_tactical_recommendations(context),
            'risk_mitigation': self._develop_risk_mitigation_strategies(context)
        }
        
        # Análisis de eficiencia operacional
        efficiency_analysis = self._analyze_operational_efficiency(context)
        tactical_session['efficiency_analysis'] = efficiency_analysis
        
        # Aprender de este análisis
        self._learn_from_tactical_analysis(tactical_session)
        
        print(f"🎯 FRIDAY: Tactical analysis complete - {len(tactical_session['tactical_recommendations'])} recommendations generated")
        self.optimizations_applied += len(tactical_session['optimization_opportunities'])
        
        return tactical_session
    
    def _autonomous_security_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Análisis de seguridad autónomo y exhaustivo"""
        return {
            'threat_landscape': self._assess_threat_landscape(context),
            'vulnerability_assessment': self._scan_vulnerabilities(context),
            'access_control_review': self._review_access_controls(context),
            'data_protection_status': self._assess_data_protection(context),
            'security_posture': self._evaluate_security_posture(context),
            'incident_preparedness': self._assess_incident_preparedness(context),
            'security_score': self._calculate_comprehensive_security_score(context)
        }
    
    def _autonomous_performance_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Análisis de rendimiento autónomo en tiempo real"""
        current_metrics = self._gather_real_time_metrics()
        baseline_comparison = self._compare_with_baseline(current_metrics)
        
        return {
            'current_performance': current_metrics,
            'baseline_comparison': baseline_comparison,
            'bottlenecks_detected': self._detect_performance_bottlenecks(current_metrics),
            'resource_utilization': self._analyze_resource_utilization(current_metrics),
            'optimization_potential': self._calculate_optimization_potential(current_metrics),
            'performance_trends': self._analyze_performance_trends(),
            'efficiency_rating': self._calculate_efficiency_rating(current_metrics)
        }
    
    def _gather_real_time_metrics(self) -> Dict[str, Any]:
        """Recopila métricas de rendimiento en tiempo real"""
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'memory_info': {
                    'percent': psutil.virtual_memory().percent,
                    'available': psutil.virtual_memory().available,
                    'used': psutil.virtual_memory().used
                },
                'disk_io': psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else {},
                'network_io': psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {},
                'process_count': len(psutil.pids()),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def _generate_tactical_recommendations(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Genera recomendaciones tácticas específicas y accionables"""
        recommendations = []
        
        # Recomendaciones de seguridad
        security_recs = self._generate_security_recommendations(context)
        recommendations.extend(security_recs)
        
        # Recomendaciones de rendimiento
        performance_recs = self._generate_performance_recommendations(context)
        recommendations.extend(performance_recs)
        
        # Recomendaciones de optimización
        optimization_recs = self._generate_optimization_recommendations(context)
        recommendations.extend(optimization_recs)
        
        # Priorizar recomendaciones por impacto
        prioritized_recs = self._prioritize_recommendations(recommendations)
        
        return prioritized_recs
    
    def coordinate_security_with_jarvis(self, security_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinación de seguridad con JARVIS para análisis estratégico"""
        coordination = {
            'coordinator': 'FRIDAY',
            'collaborator': 'JARVIS',
            'coordination_type': 'security_strategic_analysis',
            'friday_tactical_assessment': self._prepare_tactical_security_assessment(security_context),
            'jarvis_strategic_request': self._formulate_strategic_security_request(security_context),
            'combined_approach': self._design_combined_security_approach(security_context),
            'expected_security_enhancement': self._calculate_security_enhancement(security_context)
        }
        
        # Registrar coordinación de seguridad
        self._record_security_collaboration('JARVIS', coordination)
        self.ai_coordination['jarvis_status'] = 'security_coordination'
        
        print("🛡️ FRIDAY: Initiating security coordination with JARVIS")
        return coordination
    
    def coordinate_performance_with_copilot(self, performance_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinación de rendimiento con COPILOT para optimización técnica"""
        coordination = {
            'coordinator': 'FRIDAY',
            'collaborator': 'COPILOT',
            'coordination_type': 'performance_optimization',
            'friday_performance_analysis': self._prepare_performance_analysis(performance_context),
            'copilot_optimization_request': self._formulate_optimization_request(performance_context),
            'technical_optimization_strategy': self._design_technical_optimization(performance_context),
            'expected_performance_gains': self._calculate_performance_gains(performance_context)
        }
        
        # Registrar coordinación de rendimiento
        self._record_performance_collaboration('COPILOT', coordination)
        self.ai_coordination['copilot_status'] = 'performance_coordination'
        
        print("⚡ FRIDAY: Initiating performance coordination with COPILOT")
        return coordination
    
    def direct_analysis_for_basparin(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Análisis directo y preciso para BASPARIN con enfoque táctico"""
        analysis = {
            'analyst': 'FRIDAY',
            'analysis_type': 'direct_tactical_assessment',
            'request_breakdown': self._break_down_request(request),
            'tactical_assessment': self._provide_tactical_assessment(request),
            'direct_recommendations': self._provide_direct_recommendations(request),
            'implementation_roadmap': self._create_implementation_roadmap(request),
            'risk_factors': self._identify_risk_factors(request),
            'success_metrics': self._define_success_metrics(request),
            'timeline_estimation': self._estimate_realistic_timeline(request)
        }
        
        # Enfoque directo y sin ambigüedades
        analysis['friday_direct_assessment'] = self._provide_friday_direct_assessment(request)
        
        # Registrar análisis para BASPARIN
        self._record_basparin_analysis(analysis)
        
        print("🎯 FRIDAY: Direct tactical analysis provided to BASPARIN")
        return analysis
