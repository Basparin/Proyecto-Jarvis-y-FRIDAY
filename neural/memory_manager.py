"""
Memory Manager Implementation - STARK Industries  
Gestor de memoria persistente para sistema STARK
"""

import sqlite3
import pickle
import json
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os

class StarkMemoryManager:
    """Gestor de memoria persistente para sistema STARK"""
    
    def __init__(self, db_path: str = "stark_memory.db"):
        self.db_path = db_path
        self.cache = {}
        self.cache_max_size = 1000
        self.cache_ttl = timedelta(hours=1)
        self.lock = threading.RLock()
        
        self._initialize_database()
        print("💾 STARK Memory Manager - Inicializado")
    
    def _initialize_database(self):
        """Inicializa la base de datos SQLite"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabla para memoria a largo plazo
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS long_term_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value BLOB NOT NULL,
                    data_type TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    access_count INTEGER DEFAULT 0,
                    importance_score REAL DEFAULT 0.0
                )
            """)
            
            # Tabla para memoria de trabajo
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS working_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value BLOB NOT NULL,
                    data_type TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    UNIQUE(session_id, key)
                )
            """)
            
            # Tabla para patrones aprendidos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learned_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT NOT NULL,
                    pattern_data BLOB NOT NULL,
                    confidence_score REAL NOT NULL,
                    usage_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def store_long_term(self, key: str, value: Any, importance: float = 0.5) -> bool:
        """Almacena información en memoria a largo plazo"""
        try:
            with self.lock:
                serialized_value = pickle.dumps(value)
                data_type = type(value).__name__
                
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT OR REPLACE INTO long_term_memory 
                        (key, value, data_type, importance_score, updated_at)
                        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """, (key, serialized_value, data_type, importance))
                    conn.commit()
                
                # Actualizar cache
                self.cache[key] = {
                    'value': value,
                    'timestamp': datetime.now(),
                    'type': 'long_term'
                }
                
                return True
                
        except Exception as e:
            print(f"❌ Error almacenando en memoria a largo plazo: {e}")
            return False
    
    def retrieve_long_term(self, key: str) -> Optional[Any]:
        """Recupera información de memoria a largo plazo"""
        try:
            with self.lock:
                # Verificar cache primero
                if key in self.cache:
                    cache_entry = self.cache[key]
                    if datetime.now() - cache_entry['timestamp'] < self.cache_ttl:
                        return cache_entry['value']
                
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT value, data_type FROM long_term_memory 
                        WHERE key = ?
                    """, (key,))
                    
                    result = cursor.fetchone()
                    if result:
                        value = pickle.loads(result[0])
                        
                        # Actualizar contador de acceso
                        cursor.execute("""
                            UPDATE long_term_memory 
                            SET access_count = access_count + 1
                            WHERE key = ?
                        """, (key,))
                        conn.commit()
                        
                        # Actualizar cache
                        self.cache[key] = {
                            'value': value,
                            'timestamp': datetime.now(),
                            'type': 'long_term'
                        }
                        
                        return value
                
                return None
                
        except Exception as e:
            print(f"❌ Error recuperando de memoria a largo plazo: {e}")
            return None
    
    def store_working_memory(self, session_id: str, key: str, value: Any, ttl_minutes: int = 60) -> bool:
        """Almacena información en memoria de trabajo"""
        try:
            with self.lock:
                serialized_value = pickle.dumps(value)
                data_type = type(value).__name__
                expires_at = datetime.now() + timedelta(minutes=ttl_minutes)
                
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT OR REPLACE INTO working_memory 
                        (session_id, key, value, data_type, expires_at)
                        VALUES (?, ?, ?, ?, ?)
                    """, (session_id, key, serialized_value, data_type, expires_at))
                    conn.commit()
                
                return True
                
        except Exception as e:
            print(f"❌ Error almacenando en memoria de trabajo: {e}")
            return False
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de uso de memoria"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Estadísticas memoria a largo plazo
                cursor.execute("SELECT COUNT(*), AVG(importance_score) FROM long_term_memory")
                long_term_stats = cursor.fetchone()
                
                # Estadísticas memoria de trabajo
                cursor.execute("SELECT COUNT(*) FROM working_memory WHERE expires_at > CURRENT_TIMESTAMP")
                active_working = cursor.fetchone()[0]
                
                return {
                    "long_term_entries": long_term_stats[0],
                    "average_importance": long_term_stats[1] or 0.0,
                    "active_working_memory": active_working,
                    "cache_size": len(self.cache),
                    "db_size_bytes": os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
                }
                
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}
    
    def cleanup_expired(self):
        """Limpia entradas expiradas de memoria"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM working_memory WHERE expires_at <= CURRENT_TIMESTAMP")
                deleted = cursor.rowcount
                conn.commit()
                
            # Limpiar cache expirado
            current_time = datetime.now()
            expired_keys = [
                key for key, entry in self.cache.items()
                if current_time - entry['timestamp'] > self.cache_ttl
            ]
            
            for key in expired_keys:
                del self.cache[key]
            
            print(f"🧹 Limpieza completada: {deleted} entradas eliminadas")
            
        except Exception as e:
            print(f"❌ Error en limpieza: {e}")

# Función de utilidad para crear gestor de memoria
def create_stark_memory_manager(db_path: str = "stark_memory.db") -> StarkMemoryManager:
    """Crea un gestor de memoria STARK"""
    return StarkMemoryManager(db_path)
