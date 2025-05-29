"""
STARK INDUSTRIES - Autoprogrammer Reviewer (Submódulo Especializado)
Revisión inteligente de código con análisis profundo y sugerencias
"""

import os
import ast
import re
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class IssueType(Enum):
    SYNTAX = "syntax"
    LOGIC = "logic"
    PERFORMANCE = "performance"
    SECURITY = "security"
    STYLE = "style"
    DOCUMENTATION = "documentation"

class Severity(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    INFO = 5

@dataclass
class CodeIssue:
    file_path: str
    line_number: int
    issue_type: IssueType
    severity: Severity
    description: str
    suggestion: str
    code_snippet: str

class CodeReviewer:
    """Revisor inteligente de código con análisis múltiple"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        
        # Patrones de revisión categorizados
        self.review_patterns = {
            'security': [
                {
                    'pattern': r'eval\s*\(',
                    'severity': Severity.CRITICAL,
                    'description': 'Uso peligroso de eval()',
                    'suggestion': 'Usar ast.literal_eval() o validación específica'
                },
                {
                    'pattern': r'exec\s*\(',
                    'severity': Severity.CRITICAL,
                    'description': 'Uso peligroso de exec()',
                    'suggestion': 'Evitar exec() y usar alternativas seguras'
                },
                {
                    'pattern': r'input\s*\([^)]*\)\s*.*eval',
                    'severity': Severity.CRITICAL,
                    'description': 'Input directo a eval - vulnerabilidad de seguridad',
                    'suggestion': 'Validar entrada antes de procesar'
                }
            ],
            'performance': [
                {
                    'pattern': r'for\s+\w+\s+in\s+range\(len\(',
                    'severity': Severity.MEDIUM,
                    'description': 'Loop ineficiente con range(len())',
                    'suggestion': 'Usar enumerate() o iteración directa'
                },
                {
                    'pattern': r'\w+\s*\+=\s*["\'].*["\']',
                    'severity': Severity.MEDIUM,
                    'description': 'Concatenación ineficiente de strings',
                    'suggestion': 'Usar join() o f-strings'
                },
                {
                    'pattern': r'time\.sleep\s*\(',
                    'severity': Severity.LOW,
                    'description': 'Sleep síncrono en contexto potencialmente asíncrono',
                    'suggestion': 'Considerar asyncio.sleep() si es código asíncrono'
                }
            ],
            'style': [
                {
                    'pattern': r'except\s*:',
                    'severity': Severity.HIGH,
                    'description': 'Bare except clause',
                    'suggestion': 'Especificar tipo de excepción'
                },
                {
                    'pattern': r'from\s+\w+\s+import\s+\*',
                    'severity': Severity.MEDIUM,
                    'description': 'Wildcard import',
                    'suggestion': 'Importar solo los nombres necesarios'
                },
                {
                    'pattern': r'def\s+[a-z]+[A-Z]',
                    'severity': Severity.LOW,
                    'description': 'Nombre de función no sigue PEP 8',
                    'suggestion': 'Usar snake_case para nombres de función'
                }
            ],
            'logic': [
                {
                    'pattern': r'if\s+.*==\s*True:',
                    'severity': Severity.LOW,
                    'description': 'Comparación innecesaria con True',
                    'suggestion': 'Usar directamente la condición booleana'
                },
                {
                    'pattern': r'if\s+.*==\s*False:',
                    'severity': Severity.LOW,
                    'description': 'Comparación innecesaria con False',
                    'suggestion': 'Usar not en la condición'
                },
                {
                    'pattern': r'len\([^)]+\)\s*==\s*0',
                    'severity': Severity.LOW,
                    'description': 'Verificación de longitud innecesaria',
                    'suggestion': 'Usar "not container" directamente'
                }
            ]
        }
        
        # Análisis de complejidad
        self.complexity_thresholds = {
            'function_lines': 50,
            'cyclomatic_complexity': 10,
            'nesting_depth': 4,
            'parameters': 5
        }
    
    async def review_code(self, file_path: str) -> str:
        """Realiza revisión completa de un archivo de código"""
        full_path = os.path.join(self.workspace_path, file_path)
        
        if not os.path.exists(full_path):
            return f"❌ Archivo no encontrado: {file_path}"
        
        try:
            # Leer contenido del archivo
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Realizar análisis múltiple
            issues = []
            
            # Análisis sintáctico
            syntax_issues = await self.analyze_syntax(content, file_path)
            issues.extend(syntax_issues)
            
            # Análisis por patrones
            pattern_issues = await self.analyze_patterns(content, file_path)
            issues.extend(pattern_issues)
            
            # Análisis de complejidad
            complexity_issues = await self.analyze_complexity(content, file_path)
            issues.extend(complexity_issues)
            
            # Análisis de documentación
            doc_issues = await self.analyze_documentation(content, file_path)
            issues.extend(doc_issues)
            
            # Análisis de importaciones
            import_issues = await self.analyze_imports(content, file_path)
            issues.extend(import_issues)
            
            # Generar reporte
            report = await self.generate_review_report(issues, file_path, content)
            
            # Guardar reporte si hay issues
            if issues:
                await self.save_review_report(report, file_path)
            
            return report
            
        except Exception as e:
            return f"❌ Error revisando {file_path}: {str(e)}"
    
    async def analyze_syntax(self, content: str, file_path: str) -> List[CodeIssue]:
        """Analiza sintaxis y estructura del código"""
        issues = []
        
        try:
            tree = ast.parse(content)
            
            # Verificar estructura AST para problemas comunes
            for node in ast.walk(tree):
                # Funciones muy largas
                if isinstance(node, ast.FunctionDef):
                    func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                    if func_lines > self.complexity_thresholds['function_lines']:
                        issues.append(CodeIssue(
                            file_path=file_path,
                            line_number=node.lineno,
                            issue_type=IssueType.LOGIC,
                            severity=Severity.MEDIUM,
                            description=f"Función '{node.name}' es muy larga ({func_lines} líneas)",
                            suggestion="Considerar dividir en funciones más pequeñas",
                            code_snippet=f"def {node.name}(...)"
                        ))
                    
                    # Demasiados parámetros
                    param_count = len(node.args.args)
                    if param_count > self.complexity_thresholds['parameters']:
                        issues.append(CodeIssue(
                            file_path=file_path,
                            line_number=node.lineno,
                            issue_type=IssueType.STYLE,
                            severity=Severity.LOW,
                            description=f"Función '{node.name}' tiene muchos parámetros ({param_count})",
                            suggestion="Considerar usar objeto de configuración o **kwargs",
                            code_snippet=f"def {node.name}(...)"
                        ))
                
                # Clases sin documentación
                elif isinstance(node, ast.ClassDef):
                    if not ast.get_docstring(node):
                        issues.append(CodeIssue(
                            file_path=file_path,
                            line_number=node.lineno,
                            issue_type=IssueType.DOCUMENTATION,
                            severity=Severity.LOW,
                            description=f"Clase '{node.name}' sin documentación",
                            suggestion="Agregar docstring explicando el propósito de la clase",
                            code_snippet=f"class {node.name}:"
                        ))
                
        except SyntaxError as e:
            issues.append(CodeIssue(
                file_path=file_path,
                line_number=e.lineno or 0,
                issue_type=IssueType.SYNTAX,
                severity=Severity.CRITICAL,
                description=f"Error de sintaxis: {e.msg}",
                suggestion="Corregir la sintaxis del código",
                code_snippet=e.text or ""
            ))
        
        return issues
    
    async def analyze_patterns(self, content: str, file_path: str) -> List[CodeIssue]:
        """Analiza patrones problemáticos en el código"""
        issues = []
        lines = content.split('\n')
        
        for category, patterns in self.review_patterns.items():
            for pattern_config in patterns:
                pattern = pattern_config['pattern']
                
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern, line):
                        issues.append(CodeIssue(
                            file_path=file_path,
                            line_number=line_num,
                            issue_type=IssueType(category),
                            severity=pattern_config['severity'],
                            description=pattern_config['description'],
                            suggestion=pattern_config['suggestion'],
                            code_snippet=line.strip()
                        ))
        
        return issues
    
    async def analyze_complexity(self, content: str, file_path: str) -> List[CodeIssue]:
        """Analiza complejidad del código"""
        issues = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Calcular complejidad ciclomática simplificada
                    complexity = self.calculate_cyclomatic_complexity(node)
                    
                    if complexity > self.complexity_thresholds['cyclomatic_complexity']:
                        issues.append(CodeIssue(
                            file_path=file_path,
                            line_number=node.lineno,
                            issue_type=IssueType.LOGIC,
                            severity=Severity.HIGH,
                            description=f"Alta complejidad ciclomática ({complexity}) en '{node.name}'",
                            suggestion="Refactorizar función para reducir complejidad",
                            code_snippet=f"def {node.name}(...)"
                        ))
                    
                    # Verificar anidamiento profundo
                    max_depth = self.calculate_nesting_depth(node)
                    if max_depth > self.complexity_thresholds['nesting_depth']:
                        issues.append(CodeIssue(
                            file_path=file_path,
                            line_number=node.lineno,
                            issue_type=IssueType.LOGIC,
                            severity=Severity.MEDIUM,
                            description=f"Anidamiento excesivo ({max_depth} niveles) en '{node.name}'",
                            suggestion="Extraer lógica a funciones separadas",
                            code_snippet=f"def {node.name}(...)"
                        ))
        
        except Exception as e:
            print(f"Error analizando complejidad: {e}")
        
        return issues
    
    async def analyze_documentation(self, content: str, file_path: str) -> List[CodeIssue]:
        """Analiza calidad de documentación"""
        issues = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Verificar presencia de docstring
                    docstring = ast.get_docstring(node)
                    
                    if not docstring:
                        # Solo reportar para funciones públicas (no empiezan con _)
                        if not node.name.startswith('_'):
                            issues.append(CodeIssue(
                                file_path=file_path,
                                line_number=node.lineno,
                                issue_type=IssueType.DOCUMENTATION,
                                severity=Severity.LOW,
                                description=f"Función '{node.name}' sin documentación",
                                suggestion="Agregar docstring explicando parámetros y valor de retorno",
                                code_snippet=f"def {node.name}(...)"
                            ))
                    else:
                        # Verificar calidad del docstring
                        if len(docstring.strip()) < 10:
                            issues.append(CodeIssue(
                                file_path=file_path,
                                line_number=node.lineno,
                                issue_type=IssueType.DOCUMENTATION,
                                severity=Severity.LOW,
                                description=f"Documentación muy breve en '{node.name}'",
                                suggestion="Expandir documentación con más detalles",
                                code_snippet=f'"""{docstring}"""'
                            ))
        
        except Exception as e:
            print(f"Error analizando documentación: {e}")
        
        return issues
    
    async def analyze_imports(self, content: str, file_path: str) -> List[CodeIssue]:
        """Analiza importaciones del archivo"""
        issues = []
        lines = content.split('\n')
        
        import_lines = []
        used_names = set()
        
        # Recopilar importaciones y nombres utilizados
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('import ') or stripped.startswith('from '):
                import_lines.append((line_num, stripped))
            
            # Buscar uso de nombres (simplificado)
            words = re.findall(r'\b\w+\b', line)
            used_names.update(words)
        
        # Verificar importaciones no utilizadas
        for line_num, import_line in import_lines:
            if 'import *' in import_line:
                continue  # Ya se maneja en patrones
            
            # Extraer nombres importados
            imported_names = self.extract_imported_names(import_line)
            
            for name in imported_names:
                if name not in used_names:
                    issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=line_num,
                        issue_type=IssueType.STYLE,
                        severity=Severity.LOW,
                        description=f"Import '{name}' no utilizado",
                        suggestion=f"Remover import no utilizado: {name}",
                        code_snippet=import_line
                    ))
        
        return issues
    
    async def generate_review_report(self, issues: List[CodeIssue], file_path: str, content: str) -> str:
        """Genera reporte completo de revisión"""
        if not issues:
            return f"✅ {file_path}: Código revisado sin problemas detectados"
        
        # Agrupar issues por severidad
        critical_issues = [i for i in issues if i.severity == Severity.CRITICAL]
        high_issues = [i for i in issues if i.severity == Severity.HIGH]
        medium_issues = [i for i in issues if i.severity == Severity.MEDIUM]
        low_issues = [i for i in issues if i.severity == Severity.LOW]
        info_issues = [i for i in issues if i.severity == Severity.INFO]
        
        # Calcular estadísticas del código
        lines_of_code = len([line for line in content.split('\n') if line.strip() and not line.strip().startswith('#')])
        total_lines = len(content.split('\n'))
        
        report = f"""
🔍 STARK CODE REVIEW REPORT
{'='*50}
📁 Archivo: {file_path}
📊 Estadísticas: {lines_of_code} líneas de código / {total_lines} líneas totales
🚨 Issues encontrados: {len(issues)}
📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

RESUMEN POR SEVERIDAD:
"""
        
        if critical_issues:
            report += f"🔴 CRÍTICO: {len(critical_issues)} issues\n"
        if high_issues:
            report += f"🟠 ALTO: {len(high_issues)} issues\n"
        if medium_issues:
            report += f"🟡 MEDIO: {len(medium_issues)} issues\n"
        if low_issues:
            report += f"🔵 BAJO: {len(low_issues)} issues\n"
        if info_issues:
            report += f"⚪ INFO: {len(info_issues)} issues\n"
        
        report += "\nDETALLE DE ISSUES:\n" + "="*50 + "\n"
        
        # Mostrar issues ordenados por severidad
        all_issues_sorted = sorted(issues, key=lambda x: (x.severity.value, x.line_number))
        
        for i, issue in enumerate(all_issues_sorted, 1):
            severity_icon = {
                Severity.CRITICAL: "🔴",
                Severity.HIGH: "🟠", 
                Severity.MEDIUM: "🟡",
                Severity.LOW: "🔵",
                Severity.INFO: "⚪"
            }[issue.severity]
            
            report += f"""
{i}. {severity_icon} {issue.severity.name} - Línea {issue.line_number}
   Tipo: {issue.issue_type.value.capitalize()}
   Problema: {issue.description}
   Sugerencia: {issue.suggestion}
   Código: {issue.code_snippet}
   {'-'*30}
"""
        
        # Agregar recomendaciones generales
        report += self.generate_general_recommendations(issues)
        
        # Calcular puntuación de calidad
        quality_score = self.calculate_quality_score(issues, lines_of_code)
        report += f"\n📈 PUNTUACIÓN DE CALIDAD: {quality_score}/100\n"
        
        return report
    
    async def save_review_report(self, report: str, file_path: str):
        """Guarda reporte de revisión"""
        report_dir = os.path.join(self.workspace_path, "reviews")
        os.makedirs(report_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = os.path.basename(file_path).replace('.py', '')
        report_path = os.path.join(report_dir, f"review_{file_name}_{timestamp}.md")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
    
    # Métodos auxiliares
    def calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """Calcula complejidad ciclomática simplificada"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
        
        return complexity
    
    def calculate_nesting_depth(self, node: ast.FunctionDef) -> int:
        """Calcula profundidad máxima de anidamiento"""
        def get_depth(node, current_depth=0):
            max_depth = current_depth
            
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                    child_depth = get_depth(child, current_depth + 1)
                    max_depth = max(max_depth, child_depth)
                else:
                    child_depth = get_depth(child, current_depth)
                    max_depth = max(max_depth, child_depth)
            
            return max_depth
        
        return get_depth(node)
    
    def extract_imported_names(self, import_line: str) -> List[str]:
        """Extrae nombres de una línea de import"""
        names = []
        
        if import_line.startswith('import '):
            # import module1, module2
            modules = import_line[7:].split(',')
            for module in modules:
                name = module.strip().split(' as ')[0]
                names.append(name.split('.')[0])
        
        elif import_line.startswith('from '):
            # from module import name1, name2
            parts = import_line.split(' import ')
            if len(parts) == 2:
                imported = parts[1].split(',')
                for item in imported:
                    name = item.strip().split(' as ')[0]
                    names.append(name)
        
        return names
    
    def generate_general_recommendations(self, issues: List[CodeIssue]) -> str:
        """Genera recomendaciones generales basadas en los issues encontrados"""
        recommendations = "\n🎯 RECOMENDACIONES GENERALES:\n" + "="*30 + "\n"
        
        # Analizar patrones en los issues
        issue_types = {}
        for issue in issues:
            issue_type = issue.issue_type
            if issue_type not in issue_types:
                issue_types[issue_type] = 0
            issue_types[issue_type] += 1
        
        if IssueType.SECURITY in issue_types:
            recommendations += "🔒 SEGURIDAD: Revisar y corregir vulnerabilidades de seguridad inmediatamente.\n"
        
        if IssueType.PERFORMANCE in issue_types:
            recommendations += "⚡ RENDIMIENTO: Optimizar código para mejor performance.\n"
        
        if IssueType.DOCUMENTATION in issue_types:
            recommendations += "📝 DOCUMENTACIÓN: Mejorar documentación para mayor claridad.\n"
        
        if IssueType.STYLE in issue_types:
            recommendations += "🎨 ESTILO: Seguir convenciones PEP 8 para mejor legibilidad.\n"
        
        if len(issues) > 10:
            recommendations += "🔧 REFACTORING: Considerar refactorización mayor del código.\n"
        
        return recommendations
    
    def calculate_quality_score(self, issues: List[CodeIssue], lines_of_code: int) -> int:
        """Calcula puntuación de calidad del código"""
        if lines_of_code == 0:
            return 0
        
        # Penalizaciones por tipo de issue
        penalties = {
            Severity.CRITICAL: 20,
            Severity.HIGH: 10,
            Severity.MEDIUM: 5,
            Severity.LOW: 2,
            Severity.INFO: 1
        }
        
        total_penalty = 0
        for issue in issues:
            total_penalty += penalties[issue.severity]
        
        # Normalizar por líneas de código
        penalty_per_line = total_penalty / lines_of_code
        
        # Calcular puntuación (máximo 100)
        score = max(0, 100 - int(penalty_per_line * 100))
        
        return score
