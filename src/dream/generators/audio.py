from TTS.api import TTS
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from pathlib import Path
from ..utils.logger import logger
from config import config

class AudioGenerator:
    def __init__(self):
        # Initialize TTS model
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        self.music_model = MusicGen.get_pretrained(config.MUSIC_MODEL)
        logger.info("Loaded TTS and Music models")

    def generate_narration(self, text: str, output_path: Path, language: str = "en") -> Path:
        """Generates narration using XTTS with multi-language support."""
        try:
            # Available languages: en, es, fr, de, it, pt, pl, tr, ru, nl, cs, ar, zh-cn, ja, ko, hu
            self.tts.tts_to_file(
                text=text,
                file_path=str(output_path),
                language=language,
                speaker_wav=None,  # Can be used for voice cloning
                speed=1.0
            )
            logger.info(f"Narration saved to {output_path} in {language}")
            return output_path
        except Exception as e:
            logger.error(f"Narration failed: {str(e)}")
            raise

    def get_available_languages(self) -> list:
        """Returns list of available languages."""
        return [
            "English", "Spanish", "French", "German", "Italian", 
            "Portuguese", "Polish", "Turkish", "Russian", "Dutch",
            "Czech", "Arabic", "Chinese", "Japanese", "Korean", "Hungarian"
        ]

    def get_language_code(self, language: str) -> str:
        """Converts language name to code."""
        language_map = {
            "English": "en", "Spanish": "es", "French": "fr",
            "German": "de", "Italian": "it", "Portuguese": "pt",
            "Polish": "pl", "Turkish": "tr", "Russian": "ru",
            "Dutch": "nl", "Czech": "cs", "Arabic": "ar",
            "Chinese": "zh-cn", "Japanese": "ja", "Korean": "ko",
            "Hungarian": "hu"
        }
        return language_map.get(language, "en")

    def generate_music(self, prompt: str, output_path: Path) -> Path:
        """Generates background music."""
        try:
            self.music_model.set_generation_params(duration=config.VIDEO_DURATION)
            music = self.music_model.generate([prompt])
            audio_write(str(output_path), music[0].cpu(), self.music_model.sample_rate)
            logger.info(f"Music saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Music generation failed: {str(e)}")
            raise