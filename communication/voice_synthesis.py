"""
STARK INDUSTRIES - Voice Synthesis System
Sistema avanzado de síntesis de voz para comunicación
Implementación real con múltiples motores TTS y voces personalizadas
"""

import pyttsx3
import threading
import time
import os
import json
import wave
import tempfile
from typing import Dict, List, Any, Optional, Callable, Union
from datetime import datetime
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging
from enum import Enum

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceGender(Enum):
    """Géneros de voz disponibles"""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"

class VoiceLanguage(Enum):
    """Idiomas soportados"""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"

@dataclass
class VoiceProfile:
    """Perfil de voz personalizado"""
    name: str
    gender: VoiceGender
    language: VoiceLanguage
    rate: int  # Velocidad (palabras por minuto)
    volume: float  # Volumen (0.0 - 1.0)
    pitch: int  # Tono (-50 a 50)
    engine_voice_id: str
    personality_traits: List[str]

@dataclass
class SpeechRequest:
    """Solicitud de síntesis de voz"""
    text: str
    voice_profile: str
    priority: int
    timestamp: datetime
    callback: Optional[Callable] = None
    save_to_file: Optional[str] = None

class TTSEngine(ABC):
    """Motor abstracto de síntesis de voz"""
    
    @abstractmethod
    def initialize(self) -> bool:
        pass
    
    @abstractmethod
    def speak(self, text: str, voice_id: str) -> bool:
        pass
    
    @abstractmethod
    def save_to_file(self, text: str, voice_id: str, filename: str) -> bool:
        pass
    
    @abstractmethod
    def get_available_voices(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def set_rate(self, rate: int):
        pass
    
    @abstractmethod
    def set_volume(self, volume: float):
        pass

class Pyttsx3Engine(TTSEngine):
    """Motor TTS basado en pyttsx3"""
    
    def __init__(self):
        self.engine = None
        self.available_voices = []
        self.current_voice = None
        self.lock = threading.Lock()
        
        logger.info("🗣️ Inicializando motor pyttsx3")
    
    def initialize(self) -> bool:
        """Inicializa el motor pyttsx3"""
        try:
            self.engine = pyttsx3.init()
            
            # Configuración por defecto
            self.engine.setProperty('rate', 200)
            self.engine.setProperty('volume', 0.8)
            
            # Obtener voces disponibles
            voices = self.engine.getProperty('voices')
            self.available_voices = []
            
            for i, voice in enumerate(voices):
                voice_info = {
                    "id": voice.id,
                    "name": voice.name,
                    "gender": self._detect_gender(voice.name),
                    "language": self._detect_language(voice.name, voice.id),
                    "index": i
                }
                self.available_voices.append(voice_info)
            
            logger.info(f"Motor pyttsx3 inicializado con {len(self.available_voices)} voces")
            return True
            
        except Exception as e:
            logger.error(f"Error inicializando pyttsx3: {e}")
            return False
    
    def _detect_gender(self, voice_name: str) -> VoiceGender:
        """Detecta el género de una voz por su nombre"""
        name_lower = voice_name.lower()
        
        if any(word in name_lower for word in ['female', 'woman', 'girl', 'zira', 'cortana', 'eva']):
            return VoiceGender.FEMALE
        elif any(word in name_lower for word in ['male', 'man', 'boy', 'david', 'mark', 'alex']):
            return VoiceGender.MALE
        else:
            return VoiceGender.NEUTRAL
    
    def _detect_language(self, voice_name: str, voice_id: str) -> VoiceLanguage:
        """Detecta el idioma de una voz"""
        text = (voice_name + " " + voice_id).lower()
        
        if any(lang in text for lang in ['spanish', 'es-', 'esp', 'sabina', 'helena']):
            return VoiceLanguage.SPANISH
        elif any(lang in text for lang in ['french', 'fr-', 'fra', 'hortense']):
            return VoiceLanguage.FRENCH
        elif any(lang in text for lang in ['german', 'de-', 'deu', 'katja', 'stefan']):
            return VoiceLanguage.GERMAN
        else:
            return VoiceLanguage.ENGLISH
    
    def speak(self, text: str, voice_id: str = None) -> bool:
        """Sintetiza y reproduce voz"""
        try:
            with self.lock:
                if voice_id:
                    self.engine.setProperty('voice', voice_id)
                
                self.engine.say(text)
                self.engine.runAndWait()
                
            return True
            
        except Exception as e:
            logger.error(f"Error en síntesis de voz: {e}")
            return False
    
    def save_to_file(self, text: str, voice_id: str, filename: str) -> bool:
        """Guarda la síntesis de voz en un archivo"""
        try:
            with self.lock:
                if voice_id:
                    self.engine.setProperty('voice', voice_id)
                
                # pyttsx3 no tiene save_to_file nativo, usamos workaround
                temp_file = tempfile.mktemp(suffix='.wav')
                
                # Configurar para guardar
                original_output = self.engine.getProperty('voice')
                self.engine.save_to_file(text, temp_file)
                self.engine.runAndWait()
                
                # Copiar archivo temporal al destino
                if os.path.exists(temp_file):
                    import shutil
                    shutil.move(temp_file, filename)
                    return True
                
            return False
            
        except Exception as e:
            logger.error(f"Error guardando archivo de voz: {e}")
            return False
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Obtiene las voces disponibles"""
        return self.available_voices.copy()
    
    def set_rate(self, rate: int):
        """Establece la velocidad de habla"""
        try:
            with self.lock:
                self.engine.setProperty('rate', rate)
        except Exception as e:
            logger.error(f"Error estableciendo velocidad: {e}")
    
    def set_volume(self, volume: float):
        """Establece el volumen"""
        try:
            with self.lock:
                self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
        except Exception as e:
            logger.error(f"Error estableciendo volumen: {e}")

class WindowsTTSEngine(TTSEngine):
    """Motor TTS nativo de Windows (SAPI)"""
    
    def __init__(self):
        self.sapi = None
        self.available_voices = []
        
        try:
            import win32com.client
            self.win32_available = True
        except ImportError:
            self.win32_available = False
            logger.warning("win32com no disponible, motor Windows TTS deshabilitado")
    
    def initialize(self) -> bool:
        """Inicializa el motor Windows TTS"""
        if not self.win32_available:
            return False
        
        try:
            import win32com.client
            self.sapi = win32com.client.Dispatch("SAPI.SpVoice")
            
            # Obtener voces disponibles
            voices = self.sapi.GetVoices()
            self.available_voices = []
            
            for i in range(voices.Count):
                voice = voices.Item(i)
                voice_info = {
                    "id": i,
                    "name": voice.GetDescription(),
                    "gender": self._detect_gender_sapi(voice.GetDescription()),
                    "language": self._detect_language_sapi(voice.GetDescription())
                }
                self.available_voices.append(voice_info)
            
            logger.info(f"Motor Windows TTS inicializado con {len(self.available_voices)} voces")
            return True
            
        except Exception as e:
            logger.error(f"Error inicializando Windows TTS: {e}")
            return False
    
    def _detect_gender_sapi(self, description: str) -> VoiceGender:
        """Detecta género para voces SAPI"""
        desc_lower = description.lower()
        if 'female' in desc_lower or 'zira' in desc_lower:
            return VoiceGender.FEMALE
        elif 'male' in desc_lower or 'david' in desc_lower:
            return VoiceGender.MALE
        return VoiceGender.NEUTRAL
    
    def _detect_language_sapi(self, description: str) -> VoiceLanguage:
        """Detecta idioma para voces SAPI"""
        desc_lower = description.lower()
        if 'spanish' in desc_lower:
            return VoiceLanguage.SPANISH
        elif 'french' in desc_lower:
            return VoiceLanguage.FRENCH
        elif 'german' in desc_lower:
            return VoiceLanguage.GERMAN
        return VoiceLanguage.ENGLISH
    
    def speak(self, text: str, voice_id: str = None) -> bool:
        """Sintetiza con SAPI"""
        if not self.sapi:
            return False
        
        try:
            if voice_id is not None:
                voices = self.sapi.GetVoices()
                if int(voice_id) < voices.Count:
                    self.sapi.Voice = voices.Item(int(voice_id))
            
            self.sapi.Speak(text)
            return True
            
        except Exception as e:
            logger.error(f"Error en SAPI speak: {e}")
            return False
    
    def save_to_file(self, text: str, voice_id: str, filename: str) -> bool:
        """Guarda con SAPI"""
        if not self.sapi:
            return False
        
        try:
            import win32com.client
            
            if voice_id is not None:
                voices = self.sapi.GetVoices()
                if int(voice_id) < voices.Count:
                    self.sapi.Voice = voices.Item(int(voice_id))
            
            # Crear file stream
            file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
            file_stream.Open(filename, 3)  # 3 = write mode
            
            original_output = self.sapi.AudioOutputStream
            self.sapi.AudioOutputStream = file_stream
            
            self.sapi.Speak(text)
            
            self.sapi.AudioOutputStream = original_output
            file_stream.Close()
            
            return True
            
        except Exception as e:
            logger.error(f"Error guardando con SAPI: {e}")
            return False
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Voces disponibles en SAPI"""
        return self.available_voices.copy()
    
    def set_rate(self, rate: int):
        """Establece velocidad SAPI"""
        if self.sapi:
            # SAPI usa rango -10 a 10, convertir desde rate
            sapi_rate = max(-10, min(10, (rate - 200) // 20))
            self.sapi.Rate = sapi_rate
    
    def set_volume(self, volume: float):
        """Establece volumen SAPI"""
        if self.sapi:
            self.sapi.Volume = int(volume * 100)

class StarkVoiceSynthesis:
    """
    Sistema principal de síntesis de voz de STARK Industries
    Coordina múltiples motores TTS y perfiles de voz
    """
    
    def __init__(self, data_path: str = "voice_data"):
        self.data_path = data_path
        self.engines = {}
        self.voice_profiles = {}
        self.speech_queue = []
        self.is_speaking = False
        self.processing_thread = None
        self.active = False
        
        # Configuración
        self.default_engine = "pyttsx3"
        self.queue_lock = threading.Lock()
        
        # Estadísticas
        self.stats = {
            "total_requests": 0,
            "successful_synthesis": 0,
            "failed_synthesis": 0,
            "average_processing_time": 0.0,
            "last_update": datetime.now()
        }
        
        # Callbacks
        self.speech_callbacks: List[Callable] = []
        
        self._ensure_data_directory()
        self._initialize_engines()
        self._load_voice_profiles()
        self._create_default_profiles()
        
        logger.info("🎤 STARK Voice Synthesis System inicializado")
    
    def _ensure_data_directory(self):
        """Asegura que el directorio de datos existe"""
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
    
    def _initialize_engines(self):
        """Inicializa todos los motores TTS disponibles"""
        # Motor pyttsx3 (siempre disponible)
        pyttsx3_engine = Pyttsx3Engine()
        if pyttsx3_engine.initialize():
            self.engines["pyttsx3"] = pyttsx3_engine
        
        # Motor Windows TTS (si está disponible)
        windows_engine = WindowsTTSEngine()
        if windows_engine.initialize():
            self.engines["windows"] = windows_engine
        
        logger.info(f"Motores TTS inicializados: {list(self.engines.keys())}")
    
    def _load_voice_profiles(self):
        """Carga perfiles de voz guardados"""
        try:
            profiles_file = os.path.join(self.data_path, "voice_profiles.json")
            if os.path.exists(profiles_file):
                with open(profiles_file, 'r', encoding='utf-8') as f:
                    profiles_data = json.load(f)
                
                for name, data in profiles_data.items():
                    profile = VoiceProfile(
                        name=data["name"],
                        gender=VoiceGender(data["gender"]),
                        language=VoiceLanguage(data["language"]),
                        rate=data["rate"],
                        volume=data["volume"],
                        pitch=data["pitch"],
                        engine_voice_id=data["engine_voice_id"],
                        personality_traits=data["personality_traits"]
                    )
                    self.voice_profiles[name] = profile
                
                logger.info(f"Cargados {len(self.voice_profiles)} perfiles de voz")
                
        except Exception as e:
            logger.error(f"Error cargando perfiles de voz: {e}")
    
    def _create_default_profiles(self):
        """Crea perfiles de voz por defecto para los AIs"""
        if not self.engines:
            return
        
        default_engine = list(self.engines.keys())[0]
        available_voices = self.engines[default_engine].get_available_voices()
        
        if not available_voices:
            return
        
        # Buscar voces por género para los perfiles
        male_voice = None
        female_voice = None
        neutral_voice = available_voices[0]["id"]  # Fallback
        
        for voice in available_voices:
            if voice["gender"] == VoiceGender.MALE and not male_voice:
                male_voice = voice["id"]
            elif voice["gender"] == VoiceGender.FEMALE and not female_voice:
                female_voice = voice["id"]
        
        # Perfil JARVIS - Voz sofisticada masculina
        if "jarvis" not in self.voice_profiles:
            self.voice_profiles["jarvis"] = VoiceProfile(
                name="jarvis",
                gender=VoiceGender.MALE,
                language=VoiceLanguage.ENGLISH,
                rate=190,  # Velocidad moderada
                volume=0.8,
                pitch=0,
                engine_voice_id=male_voice or neutral_voice,
                personality_traits=["sophisticated", "calm", "authoritative"]
            )
        
        # Perfil FRIDAY - Voz directa femenina
        if "friday" not in self.voice_profiles:
            self.voice_profiles["friday"] = VoiceProfile(
                name="friday",
                gender=VoiceGender.FEMALE,
                language=VoiceLanguage.ENGLISH,
                rate=210,  # Velocidad rápida
                volume=0.9,
                pitch=10,
                engine_voice_id=female_voice or neutral_voice,
                personality_traits=["direct", "efficient", "tactical"]
            )
        
        # Perfil COPILOT - Voz analítica neutra
        if "copilot" not in self.voice_profiles:
            self.voice_profiles["copilot"] = VoiceProfile(
                name="copilot",
                gender=VoiceGender.NEUTRAL,
                language=VoiceLanguage.ENGLISH,
                rate=200,  # Velocidad estándar
                volume=0.7,
                pitch=-5,
                engine_voice_id=neutral_voice,
                personality_traits=["analytical", "precise", "helpful"]
            )
        
        self._save_voice_profiles()
        logger.info("Perfiles de voz por defecto creados")
    
    def _save_voice_profiles(self):
        """Guarda los perfiles de voz"""
        try:
            profiles_data = {}
            for name, profile in self.voice_profiles.items():
                profiles_data[name] = {
                    "name": profile.name,
                    "gender": profile.gender.value,
                    "language": profile.language.value,
                    "rate": profile.rate,
                    "volume": profile.volume,
                    "pitch": profile.pitch,
                    "engine_voice_id": profile.engine_voice_id,
                    "personality_traits": profile.personality_traits
                }
            
            profiles_file = os.path.join(self.data_path, "voice_profiles.json")
            with open(profiles_file, 'w', encoding='utf-8') as f:
                json.dump(profiles_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error guardando perfiles: {e}")
    
    def start_service(self):
        """Inicia el servicio de síntesis de voz"""
        if self.active:
            return
        
        self.active = True
        self.processing_thread = threading.Thread(target=self._processing_loop)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
        logger.info("🚀 Servicio de síntesis de voz iniciado")
    
    def stop_service(self):
        """Detiene el servicio"""
        self.active = False
        
        if self.processing_thread:
            self.processing_thread.join(timeout=2.0)
        
        logger.info("⏹️ Servicio de síntesis detenido")
    
    def speak(self, text: str, voice_profile: str = "copilot", priority: int = 1, 
             callback: Callable = None, save_to_file: str = None) -> bool:
        """Solicita síntesis de voz"""
        try:
            request = SpeechRequest(
                text=text,
                voice_profile=voice_profile,
                priority=priority,
                timestamp=datetime.now(),
                callback=callback,
                save_to_file=save_to_file
            )
            
            with self.queue_lock:
                self.speech_queue.append(request)
                # Ordenar por prioridad (mayor prioridad primero)
                self.speech_queue.sort(key=lambda x: x.priority, reverse=True)
            
            self.stats["total_requests"] += 1
            return True
            
        except Exception as e:
            logger.error(f"Error en solicitud de voz: {e}")
            return False
    
    def speak_immediately(self, text: str, voice_profile: str = "copilot") -> bool:
        """Síntesis inmediata (bloquea hasta completar)"""
        try:
            if voice_profile not in self.voice_profiles:
                voice_profile = "copilot"
            
            profile = self.voice_profiles[voice_profile]
            engine = self.engines.get(self.default_engine)
            
            if not engine:
                return False
            
            # Configurar motor
            engine.set_rate(profile.rate)
            engine.set_volume(profile.volume)
            
            # Sintetizar
            start_time = time.time()
            success = engine.speak(text, profile.engine_voice_id)
            processing_time = time.time() - start_time
            
            # Actualizar estadísticas
            if success:
                self.stats["successful_synthesis"] += 1
                self._update_processing_time(processing_time)
            else:
                self.stats["failed_synthesis"] += 1
            
            return success
            
        except Exception as e:
            logger.error(f"Error en síntesis inmediata: {e}")
            return False
    
    def _processing_loop(self):
        """Bucle principal de procesamiento de cola"""
        while self.active:
            try:
                request = None
                
                # Obtener próxima solicitud
                with self.queue_lock:
                    if self.speech_queue:
                        request = self.speech_queue.pop(0)
                
                if request:
                    self._process_speech_request(request)
                else:
                    time.sleep(0.1)  # Esperar si no hay solicitudes
                    
            except Exception as e:
                logger.error(f"Error en bucle de procesamiento: {e}")
                time.sleep(0.5)
    
    def _process_speech_request(self, request: SpeechRequest):
        """Procesa una solicitud de síntesis"""
        try:
            self.is_speaking = True
            start_time = time.time()
            
            # Obtener perfil de voz
            profile = self.voice_profiles.get(request.voice_profile, 
                                            self.voice_profiles.get("copilot"))
            
            if not profile:
                logger.error(f"Perfil de voz no encontrado: {request.voice_profile}")
                return
            
            # Obtener motor
            engine = self.engines.get(self.default_engine)
            if not engine:
                logger.error("No hay motores TTS disponibles")
                return
            
            # Configurar motor
            engine.set_rate(profile.rate)
            engine.set_volume(profile.volume)
            
            # Ejecutar síntesis
            success = False
            
            if request.save_to_file:
                success = engine.save_to_file(
                    request.text, 
                    profile.engine_voice_id, 
                    request.save_to_file
                )
            else:
                success = engine.speak(request.text, profile.engine_voice_id)
            
            # Actualizar estadísticas
            processing_time = time.time() - start_time
            
            if success:
                self.stats["successful_synthesis"] += 1
                self._update_processing_time(processing_time)
            else:
                self.stats["failed_synthesis"] += 1
            
            # Ejecutar callback
            if request.callback:
                try:
                    request.callback(success, request.text, processing_time)
                except Exception as e:
                    logger.error(f"Error en callback: {e}")
            
            # Ejecutar callbacks globales
            for callback in self.speech_callbacks:
                try:
                    callback(request, success)
                except Exception as e:
                    logger.error(f"Error en callback global: {e}")
                    
        except Exception as e:
            logger.error(f"Error procesando solicitud: {e}")
        finally:
            self.is_speaking = False
    
    def _update_processing_time(self, processing_time: float):
        """Actualiza tiempo promedio de procesamiento"""
        if self.stats["average_processing_time"] == 0.0:
            self.stats["average_processing_time"] = processing_time
        else:
            alpha = 0.1  # Factor de suavizado
            self.stats["average_processing_time"] = (
                alpha * processing_time + 
                (1 - alpha) * self.stats["average_processing_time"]
            )
    
    def get_voice_profiles(self) -> Dict[str, VoiceProfile]:
        """Obtiene todos los perfiles de voz"""
        return self.voice_profiles.copy()
    
    def create_voice_profile(self, name: str, gender: VoiceGender, 
                           language: VoiceLanguage, rate: int = 200, 
                           volume: float = 0.8, pitch: int = 0,
                           engine_voice_id: str = None,
                           personality_traits: List[str] = None) -> bool:
        """Crea un nuevo perfil de voz"""
        try:
            if engine_voice_id is None:
                # Usar primera voz disponible
                if self.engines:
                    engine = list(self.engines.values())[0]
                    voices = engine.get_available_voices()
                    if voices:
                        engine_voice_id = voices[0]["id"]
            
            profile = VoiceProfile(
                name=name,
                gender=gender,
                language=language,
                rate=rate,
                volume=volume,
                pitch=pitch,
                engine_voice_id=engine_voice_id or "",
                personality_traits=personality_traits or []
            )
            
            self.voice_profiles[name] = profile
            self._save_voice_profiles()
            
            logger.info(f"Perfil de voz creado: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Error creando perfil: {e}")
            return False
    
    def add_speech_callback(self, callback: Callable):
        """Agrega callback para eventos de síntesis"""
        self.speech_callbacks.append(callback)
    
    def get_system_info(self) -> Dict[str, Any]:
        """Información del sistema de síntesis"""
        return {
            "active": self.active,
            "engines_available": list(self.engines.keys()),
            "default_engine": self.default_engine,
            "voice_profiles": list(self.voice_profiles.keys()),
            "queue_length": len(self.speech_queue),
            "is_speaking": self.is_speaking,
            "statistics": self.stats.copy()
        }
    
    def get_available_voices(self) -> Dict[str, List[Dict[str, Any]]]:
        """Obtiene todas las voces disponibles por motor"""
        voices_by_engine = {}
        
        for engine_name, engine in self.engines.items():
            voices_by_engine[engine_name] = engine.get_available_voices()
        
        return voices_by_engine
    
    def clear_queue(self):
        """Limpia la cola de síntesis"""
        with self.queue_lock:
            self.speech_queue.clear()
        logger.info("Cola de síntesis limpiada")

# Función principal para crear el sistema de síntesis
def create_voice_synthesis(data_path: str = "voice_data") -> StarkVoiceSynthesis:
    """Crea y configura el sistema de síntesis de voz STARK"""
    return StarkVoiceSynthesis(data_path)

# Función de prueba
def test_voice_synthesis():
    """Prueba básica del sistema de síntesis"""
    tts = create_voice_synthesis()
    tts.start_service()
    
    # Pruebas con diferentes voces
    tts.speak("Hello, I am JARVIS, your sophisticated AI assistant.", "jarvis")
    time.sleep(3)
    
    tts.speak("This is FRIDAY. Systems are operational and ready for tactical operations.", "friday")
    time.sleep(3)
    
    tts.speak("GitHub Copilot here. All analysis complete and optimizations applied.", "copilot")
    time.sleep(3)
    
    print("Información del sistema:", tts.get_system_info())
    
    tts.stop_service()

if __name__ == "__main__":
    test_voice_synthesis()
