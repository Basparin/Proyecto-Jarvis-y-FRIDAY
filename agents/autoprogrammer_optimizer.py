"""
STARK INDUSTRIES - Autoprogrammer Optimizer (Submódulo Especializado)
Optimización inteligente de código para máximo rendimiento
"""

import os
import ast
import re
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import subprocess

class CodeOptimizer:
    """Optimizador inteligente de código Python"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        
        # Patrones de optimización
        self.optimization_patterns = {
            'imports': {
                'wildcard_imports': {
                    'pattern': r'from\s+\w+\s+import\s+\*',
                    'fix': self.fix_wildcard_imports,
                    'description': 'Reemplazar imports con wildcard por imports específicos'
                },
                'unused_imports': {
                    'pattern': None,  # Requires AST analysis
                    'fix': self.remove_unused_imports,
                    'description': 'Eliminar imports no utilizados'
                },
                'import_order': {
                    'pattern': None,  # Requires analysis
                    'fix': self.optimize_import_order,
                    'description': 'Ordenar imports según PEP 8'
                }
            },
            'performance': {
                'list_comprehensions': {
                    'pattern': r'for\s+\w+\s+in\s+.*:\s*\n\s*.*\.append\(',
                    'fix': self.convert_to_list_comprehension,
                    'description': 'Convertir loops a list comprehensions'
                },
                'string_concatenation': {
                    'pattern': r'\w+\s*\+=\s*["\'].*["\']',
                    'fix': self.optimize_string_concatenation,
                    'description': 'Optimizar concatenación de strings'
                },
                'inefficient_loops': {
                    'pattern': r'for\s+\w+\s+in\s+range\(len\(',
                    'fix': self.optimize_range_loops,
                    'description': 'Optimizar loops con range(len())'
                }
            },
            'memory': {
                'generator_expressions': {
                    'pattern': r'sum\(\[.*for.*\]\)',
                    'fix': self.convert_to_generators,
                    'description': 'Convertir a generator expressions'
                },
                'memory_leaks': {
                    'pattern': None,  # Requires analysis
                    'fix': self.fix_memory_leaks,
                    'description': 'Detectar y arreglar posibles memory leaks'
                }
            },
            'async': {
                'blocking_calls': {
                    'pattern': r'time\.sleep\(',
                    'fix': self.convert_to_async_sleep,
                    'description': 'Convertir time.sleep a asyncio.sleep'
                },
                'async_opportunities': {
                    'pattern': None,  # Requires analysis
                    'fix': self.identify_async_opportunities,
                    'description': 'Identificar oportunidades para async/await'
                }
            },
            'error_handling': {
                'bare_except': {
                    'pattern': r'except\s*:',
                    'fix': self.fix_bare_except,
                    'description': 'Reemplazar bare except con excepción específica'
                },
                'missing_finally': {
                    'pattern': None,  # Requires analysis
                    'fix': self.add_missing_finally,
                    'description': 'Agregar finally blocks donde sea necesario'
                }
            }
        }
    
    async def optimize_code(self, file_path: str, optimization_type: str = "all") -> str:
        """Optimiza código en un archivo específico"""
        full_path = os.path.join(self.workspace_path, file_path)
        
        if not os.path.exists(full_path):
            return f"❌ Archivo no encontrado: {file_path}"
        
        try:
            # Leer archivo original
            with open(full_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Crear backup
            backup_path = f"{full_path}.optimized_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Realizar análisis sintáctico
            syntax_analysis = await self.analyze_syntax(original_content)
            if not syntax_analysis['valid']:
                return f"❌ Error de sintaxis en {file_path}: {syntax_analysis['error']}"
            
            # Realizar optimizaciones
            optimized_content = original_content
            optimizations_applied = []
            
            if optimization_type == "all":
                for category in self.optimization_patterns:
                    result = await self.apply_category_optimizations(
                        optimized_content, category, file_path
                    )
                    optimized_content = result['content']
                    optimizations_applied.extend(result['applied'])
            else:
                # Optimización específica
                if optimization_type in self.optimization_patterns:
                    result = await self.apply_category_optimizations(
                        optimized_content, optimization_type, file_path
                    )
                    optimized_content = result['content']
                    optimizations_applied.extend(result['applied'])
            
            # Verificar que las optimizaciones no rompieron el código
            final_syntax = await self.analyze_syntax(optimized_content)
            if not final_syntax['valid']:
                return f"❌ Las optimizaciones causaron errores de sintaxis: {final_syntax['error']}"
            
            # Agregar comentario de optimización
            optimization_header = self.generate_optimization_header(optimizations_applied)
            optimized_content = optimization_header + optimized_content
            
            # Escribir archivo optimizado
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(optimized_content)
            
            # Generar reporte de optimización
            performance_gain = await self.estimate_performance_gain(optimizations_applied)
            
            return f"""✅ Optimización completada: {file_path}
📊 Optimizaciones aplicadas: {len(optimizations_applied)}
⚡ Ganancia estimada: {performance_gain}%
💾 Backup: {os.path.basename(backup_path)}
🔧 Optimizaciones: {', '.join(opt['type'] for opt in optimizations_applied)}"""
            
        except Exception as e:
            return f"❌ Error optimizando {file_path}: {str(e)}"
    
    async def analyze_syntax(self, content: str) -> Dict[str, Any]:
        """Analiza la sintaxis del código"""
        try:
            ast.parse(content)
            return {'valid': True, 'ast': ast.parse(content)}
        except SyntaxError as e:
            return {
                'valid': False,
                'error': f"Línea {e.lineno}: {e.msg}",
                'line': e.lineno,
                'offset': e.offset
            }
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    async def apply_category_optimizations(self, content: str, category: str, file_path: str) -> Dict[str, Any]:
        """Aplica optimizaciones de una categoría específica"""
        optimizations_applied = []
        optimized_content = content
        
        if category not in self.optimization_patterns:
            return {'content': content, 'applied': []}
        
        patterns = self.optimization_patterns[category]
        
        for opt_name, opt_config in patterns.items():
            try:
                if opt_config['pattern']:
                    # Optimización basada en regex
                    result = await self.apply_regex_optimization(
                        optimized_content, opt_config, opt_name, category
                    )
                else:
                    # Optimización basada en análisis
                    result = await opt_config['fix'](optimized_content, file_path)
                
                if result['modified']:
                    optimized_content = result['content']
                    optimizations_applied.append({
                        'type': f"{category}.{opt_name}",
                        'description': opt_config['description'],
                        'changes': result.get('changes', 1)
                    })
            
            except Exception as e:
                print(f"⚠️ Error aplicando optimización {category}.{opt_name}: {e}")
        
        return {'content': optimized_content, 'applied': optimizations_applied}
    
    async def apply_regex_optimization(self, content: str, opt_config: Dict, opt_name: str, category: str) -> Dict[str, Any]:
        """Aplica optimización basada en expresiones regulares"""
        pattern = opt_config['pattern']
        matches = list(re.finditer(pattern, content, re.MULTILINE))
        
        if not matches:
            return {'modified': False, 'content': content}
        
        # Aplicar fix function
        result = await opt_config['fix'](content, matches)
        
        return {
            'modified': result.get('modified', False),
            'content': result.get('content', content),
            'changes': len(matches)
        }
    
    # Funciones de optimización específicas
    async def fix_wildcard_imports(self, content: str, matches: List) -> Dict[str, Any]:
        """Arregla imports con wildcard"""
        optimized_content = content
        
        for match in reversed(matches):  # Procesar en reversa para mantener posiciones
            wildcard_line = match.group(0)
            
            # Extraer módulo
            module_match = re.search(r'from\s+(\w+)', wildcard_line)
            if module_match:
                module_name = module_match.group(1)
                
                # Analizar uso en el código para determinar imports específicos
                used_names = self.find_used_names_from_module(content, module_name)
                
                if used_names:
                    specific_import = f"from {module_name} import {', '.join(used_names)}"
                    optimized_content = optimized_content[:match.start()] + specific_import + optimized_content[match.end():]
        
        return {'modified': True, 'content': optimized_content}
    
    async def remove_unused_imports(self, content: str, file_path: str) -> Dict[str, Any]:
        """Elimina imports no utilizados"""
        try:
            tree = ast.parse(content)
            
            # Encontrar todos los imports
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for alias in node.names:
                            imports.append(f"{node.module}.{alias.name}")
            
            # Encontrar nombres utilizados
            used_names = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    used_names.add(node.id)
                elif isinstance(node, ast.Attribute):
                    # Manejar atributos como module.function
                    if isinstance(node.value, ast.Name):
                        used_names.add(node.value.id)
            
            # Identificar imports no utilizados
            unused_imports = [imp for imp in imports if not any(name in imp for name in used_names)]
            
            if unused_imports:
                # Eliminar imports no utilizados
                lines = content.split('\n')
                filtered_lines = []
                
                for line in lines:
                    is_unused_import = False
                    for unused in unused_imports:
                        if f"import {unused}" in line or f"from {unused}" in line:
                            is_unused_import = True
                            break
                    
                    if not is_unused_import:
                        filtered_lines.append(line)
                
                return {'modified': True, 'content': '\n'.join(filtered_lines)}
            
            return {'modified': False, 'content': content}
            
        except Exception as e:
            print(f"Error analizando imports: {e}")
            return {'modified': False, 'content': content}
    
    async def optimize_import_order(self, content: str, file_path: str) -> Dict[str, Any]:
        """Ordena imports según PEP 8"""
        lines = content.split('\n')
        
        # Separar imports, docstrings y código
        imports = []
        other_lines = []
        in_import_section = True
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('import ') or stripped.startswith('from '):
                if in_import_section:
                    imports.append(line)
                else:
                    other_lines.append(line)
            elif stripped == '' or stripped.startswith('#'):
                if in_import_section:
                    imports.append(line)
                else:
                    other_lines.append(line)
            else:
                in_import_section = False
                other_lines.append(line)
        
        if not imports:
            return {'modified': False, 'content': content}
        
        # Clasificar imports según PEP 8
        stdlib_imports = []
        third_party_imports = []
        local_imports = []
        
        for imp in imports:
            if imp.strip() == '' or imp.strip().startswith('#'):
                continue
                
            if self.is_stdlib_import(imp):
                stdlib_imports.append(imp)
            elif self.is_local_import(imp):
                local_imports.append(imp)
            else:
                third_party_imports.append(imp)
        
        # Ordenar cada grupo
        stdlib_imports.sort()
        third_party_imports.sort()
        local_imports.sort()
        
        # Reconstruir sección de imports
        ordered_imports = []
        if stdlib_imports:
            ordered_imports.extend(stdlib_imports)
            ordered_imports.append('')
        if third_party_imports:
            ordered_imports.extend(third_party_imports)
            ordered_imports.append('')
        if local_imports:
            ordered_imports.extend(local_imports)
            ordered_imports.append('')
        
        # Reconstruir contenido
        if ordered_imports:
            ordered_imports.pop()  # Eliminar última línea vacía
        
        optimized_content = '\n'.join(ordered_imports + other_lines)
        
        return {'modified': True, 'content': optimized_content}
    
    async def convert_to_list_comprehension(self, content: str, matches: List) -> Dict[str, Any]:
        """Convierte loops a list comprehensions"""
        optimized_content = content
        
        # Buscar patrones específicos de loops que se pueden optimizar
        loop_pattern = re.compile(
            r'(\w+)\s*=\s*\[\]\s*\n\s*for\s+(\w+)\s+in\s+(.*?):\s*\n\s*\1\.append\((.*?)\)',
            re.MULTILINE | re.DOTALL
        )
        
        for match in reversed(list(loop_pattern.finditer(content))):
            list_name, var_name, iterable, expression = match.groups()
            
            # Crear list comprehension
            list_comp = f"{list_name} = [{expression} for {var_name} in {iterable}]"
            
            optimized_content = optimized_content[:match.start()] + list_comp + optimized_content[match.end():]
        
        return {'modified': True, 'content': optimized_content}
    
    async def optimize_string_concatenation(self, content: str, matches: List) -> Dict[str, Any]:
        """Optimiza concatenación de strings"""
        # Detectar múltiples concatenaciones de strings
        concat_pattern = re.compile(
            r'(\w+)\s*=\s*["\'].*?["\']\s*\n(?:\s*\1\s*\+=\s*["\'].*?["\']\s*\n)+',
            re.MULTILINE
        )
        
        optimized_content = content
        
        for match in reversed(list(concat_pattern.finditer(content))):
            concat_block = match.group(0)
            
            # Extraer strings
            string_parts = re.findall(r'["\']([^"\']*)["\']', concat_block)
            var_name = re.search(r'(\w+)\s*=', concat_block).group(1)            # Crear versión optimizada con join
            if len(string_parts) > 2:
                string_list = ", ".join([f'"{part}"' for part in string_parts])
                optimized_concat = f'{var_name} = "".join([{string_list}])'
                optimized_content = optimized_content[:match.start()] + optimized_concat + optimized_content[match.end():]
        
        return {'modified': True, 'content': optimized_content}
    
    async def convert_to_async_sleep(self, content: str, matches: List) -> Dict[str, Any]:
        """Convierte time.sleep a asyncio.sleep"""
        optimized_content = content
        needs_asyncio_import = 'import asyncio' not in content and 'from asyncio' not in content
        
        for match in reversed(matches):
            sleep_call = match.group(0)
            
            # Extraer duración
            duration_match = re.search(r'time\.sleep\((.*?)\)', sleep_call)
            if duration_match:
                duration = duration_match.group(1)
                async_sleep = f"await asyncio.sleep({duration})"
                optimized_content = optimized_content[:match.start()] + async_sleep + optimized_content[match.end():]
        
        # Agregar import de asyncio si es necesario
        if needs_asyncio_import and matches:
            import_line = "import asyncio\n"
            optimized_content = import_line + optimized_content
        
        return {'modified': True, 'content': optimized_content}
    
    async def fix_bare_except(self, content: str, matches: List) -> Dict[str, Any]:
        """Arregla bare except clauses"""
        optimized_content = content
        
        for match in reversed(matches):
            bare_except = match.group(0)
            specific_except = "except Exception:"
            optimized_content = optimized_content[:match.start()] + specific_except + optimized_content[match.end():]
        
        return {'modified': True, 'content': optimized_content}
    
    # Métodos auxiliares
    def find_used_names_from_module(self, content: str, module: str) -> List[str]:
        """Encuentra nombres utilizados de un módulo específico"""
        # Implementación simplificada - buscar patrones comunes
        common_names = {
            'os': ['path', 'listdir', 'makedirs', 'environ'],
            'sys': ['argv', 'exit', 'path'],
            'json': ['loads', 'dumps', 'load', 'dump'],
            'time': ['sleep', 'time', 'strftime'],
            'datetime': ['datetime', 'date', 'time']
        }
        
        used = []
        if module in common_names:
            for name in common_names[module]:
                if name in content:
                    used.append(name)
        
        return used[:5]  # Limitar a 5 imports más comunes
    
    def is_stdlib_import(self, import_line: str) -> bool:
        """Determina si un import es de la librería estándar"""
        stdlib_modules = {
            'os', 'sys', 'json', 'time', 'datetime', 'collections', 
            'itertools', 'functools', 'operator', 're', 'math', 
            'random', 'string', 'io', 'pathlib', 'asyncio'
        }
        
        module_match = re.search(r'(?:from\s+|import\s+)(\w+)', import_line)
        if module_match:
            module = module_match.group(1)
            return module in stdlib_modules
        
        return False
    
    def is_local_import(self, import_line: str) -> bool:
        """Determina si un import es local (del proyecto)"""
        return import_line.startswith('from .') or 'from agents' in import_line or 'from neural' in import_line
    
    def generate_optimization_header(self, optimizations: List[Dict]) -> str:
        """Genera header con información de optimizaciones aplicadas"""
        if not optimizations:
            return ""
        
        header = f"""
# STARK AUTOPROGRAMMER - Optimizaciones aplicadas
# Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Optimizaciones: {len(optimizations)}
"""
        
        for opt in optimizations:
            header += f"# - {opt['type']}: {opt['description']}\n"
        
        header += "#" + "="*60 + "\n\n"
        
        return header
    
    async def estimate_performance_gain(self, optimizations: List[Dict]) -> int:
        """Estima ganancia de rendimiento basada en optimizaciones aplicadas"""
        gain_map = {
            'imports.wildcard_imports': 5,
            'imports.unused_imports': 10,
            'performance.list_comprehensions': 15,
            'performance.string_concatenation': 20,
            'memory.generator_expressions': 25,
            'async.blocking_calls': 30
        }
        
        total_gain = 0
        for opt in optimizations:
            gain = gain_map.get(opt['type'], 5)
            total_gain += gain * opt.get('changes', 1)
        
        return min(total_gain, 85)  # Cap at 85% max gain
