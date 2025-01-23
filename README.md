# 🌈 AI Dream Visualizer

AI Dream Visualizer is a powerful application that transforms your written dreams into immersive multimedia experiences, combining AI-generated images, videos, narration, and music.

## ✨ Features

- 🎨 **Image Generation**: Converts text descriptions into high-quality images using Stable Diffusion XL
- 🎬 **Video Animation**: Transforms static images into fluid animations using Stable Video Diffusion
- 🗣️ **Multilingual Narration**: Supports 16 languages using XTTS (Coqui TTS)
- 🎵 **Background Music**: Generates contextual music using Facebook's MusicGen
- 🎯 **User-Friendly Interface**: Simple and intuitive Gradio web interface
- 🌍 **Multi-Language Support**: Available languages include:
  - English, Spanish, French, German, Italian
  - Portuguese, Polish, Turkish, Russian, Dutch
  - Czech, Arabic, Chinese, Japanese, Korean, Hungarian

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- CUDA-capable GPU (recommended)
- FFmpeg installed on your system
- 8GB+ GPU VRAM
- 16GB+ RAM
- 10GB+ free disk space

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-dream-visualizer.git
cd ai-dream-visualizer
```

2. Create and activate a conda environment:
```bash
conda create -n dreamenv python=3.10
conda activate dreamenv
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Project Structure
```
ai-dream-visualizer/
├── src/
│   ├── app.py                 # Main application file
│   ├── config.py              # Configuration settings
│   └── dream/
│       ├── generators/        # Generation modules
│       │   ├── image.py       # Image generation using SDXL
│       │   ├── video.py       # Video generation using SVD
│       │   └── audio.py       # Audio generation using XTTS & MusicGen
│       └── utils/
│           └── logger.py      # Logging configuration
├── outputs/                   # Generated content directory
├── logs/                     # Application logs
└── requirements.txt          # Project dependencies
```

## 🎮 Features in Detail

### Image Generation
- High-resolution output using Stable Diffusion XL
- GPU-accelerated generation
- Safety checks and error handling
- Automatic prompt optimization

### Video Animation
- Stable Video Diffusion for fluid animations
- 24 FPS smooth animation with 5-second duration
- Optimized frame interpolation
- Stable frame transitions

### Audio Generation
- XTTS for natural-sounding multilingual narration (16 languages)
- MusicGen for contextual background music
- FFmpeg for balanced audio mixing
- Multiple voice options

## 📝 Configuration

Key settings in `config.py`:
```python
# Model Settings
SD_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
VIDEO_MODEL = "stabilityai/stable-video-diffusion-img2vid-xt"
MUSIC_MODEL = "facebook/musicgen-medium"

# Performance Settings
TORCH_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32

# Generation Parameters
VIDEO_FPS = 24
VIDEO_DURATION = 5  # seconds
MAX_TEXT_LENGTH = 500  # characters
```

## 🎯 Usage Example

1. Start the application:
```bash
python src/app.py
```

2. Access the web interface at `http://localhost:7860`

3. Example inputs:
```text
"A surreal landscape with floating islands and giant jellyfish" (English)
"Una ciudad cyberpunk donde siempre llueve neón" (Spanish)
"Neon yağmurun hiç durmadığı bir siberpunk şehir" (Turkish)
```

## ⚡ Performance Optimization
- GPU acceleration with mixed precision
- Singleton pattern for resource management
- Automatic cleanup of temporary files
- Memory-efficient processing
- Optimized model loading

## 🔮 Future Plans

- Voice cloning support
- Additional language support
- Custom music style selection
- Batch processing capability
- Extended video duration options
- Progress bar implementation
- Cache system for repeated generations
- Custom model support
- API endpoint implementation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Stability AI for Stable Diffusion XL and Stable Video Diffusion
- Coqui team for XTTS
- Facebook Research for MusicGen
- Gradio team for the UI framework

## 📞 Support

If you have any questions or run into issues, please open an issue in the GitHub repository.
