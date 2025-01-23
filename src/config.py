from pathlib import Path
import torch

class Config:
    # Model Sabitleri
    SD_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
    VIDEO_MODEL = "stabilityai/stable-video-diffusion-img2vid-xt"
    MUSIC_MODEL = "facebook/musicgen-medium"
    
    # Dosya Yolları
    OUTPUT_DIR = Path("outputs")
    LOG_DIR = Path("logs")
    
    # Create directories
    OUTPUT_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)
    
    # Video Parametreleri
    VIDEO_FPS = 24
    VIDEO_DURATION = 5  # saniye

    # Performans ayarları
    TORCH_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    TORCH_DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32
    
    # Güvenlik
    MAX_TEXT_LENGTH = 500  # Maksimum metin uzunluğu

config = Config()