import gradio as gr
from pathlib import Path
from dream.generators.image import ImageGenerator
from dream.generators.video import VideoGenerator
from dream.generators.audio import AudioGenerator
from config import config
import subprocess
import logging

logger = logging.getLogger(__name__)

class DreamVisualizer:
    _instance = None
    
    def __new__(cls, elevenlabs_api_key: str = None):
        if cls._instance is None:
            cls._instance = super(DreamVisualizer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.image_gen = ImageGenerator()
        self.video_gen = VideoGenerator()
        self.audio_gen = AudioGenerator()
        config.OUTPUT_DIR.mkdir(exist_ok=True)
        self._initialized = True
        
    def visualize(self, dream_text: str, language: str) -> tuple:
        """Manages the entire dream visualization workflow."""
        if len(dream_text) > config.MAX_TEXT_LENGTH:
            raise gr.Error(f"Text exceeds maximum length of {config.MAX_TEXT_LENGTH} characters")
            
        try:
            # 1. Generate image
            image_path = config.OUTPUT_DIR / f"dream_image_{hash(dream_text)}.png"
            self.image_gen.generate(dream_text, image_path)
            
            # 2. Generate video
            video_path = config.OUTPUT_DIR / f"dream_video_{hash(dream_text)}.mp4"
            self.video_gen.generate(image_path, video_path)
            
            # 3. Generate audio and music
            narration_path = config.OUTPUT_DIR / f"narration_{hash(dream_text)}.mp3"
            lang_code = self.audio_gen.get_language_code(language)
            self.audio_gen.generate_narration(dream_text, narration_path, lang_code)
            
            music_path = config.OUTPUT_DIR / f"music_{hash(dream_text)}.wav"
            self.audio_gen.generate_music(f"Psychedelic ambient music for: {dream_text}", music_path)
            
            # 4. Mix audio tracks
            final_audio_path = config.OUTPUT_DIR / f"final_audio_{hash(dream_text)}.mp3"
            self._mix_audio(narration_path, music_path, final_audio_path)
            
            # Cleanup temporary files
            self._cleanup_temp_files([narration_path, music_path])
            
            return str(video_path), str(final_audio_path)
        
        except Exception as e:
            logger.error(f"Visualization failed: {str(e)}")
            raise gr.Error(f"Generation failed: {str(e)}")
            
    def _mix_audio(self, narration_path: Path, music_path: Path, output_path: Path):
        """Combines narration and background music."""
        try:
            subprocess.run([
                "ffmpeg", "-y",
                "-i", str(narration_path),
                "-i", str(music_path),
                "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=longest:weights=1.5 0.5",
                "-c:a", "libmp3lame",
                str(output_path)
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Audio mixing failed: {e.stderr.decode()}")
            raise
            
    def _cleanup_temp_files(self, files: list[Path]):
        """Removes temporary files after processing."""
        for file in files:
            try:
                if file.exists():
                    file.unlink()
            except Exception as e:
                logger.warning(f"Failed to delete {file}: {str(e)}")

# Gradio Arayüzü
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🌈 **AI Dream Visualizer**")
    with gr.Row():
        dream_input = gr.Textbox(
            label="Describe Your Dream",
            placeholder="I was flying through a neon forest...",
            lines=3
        )
    with gr.Row():
        language_dropdown = gr.Dropdown(
            choices=AudioGenerator().get_available_languages(),
            value="English",
            label="Narration Language"
        )
    with gr.Row():
        submit_btn = gr.Button("Generate", variant="primary")
    with gr.Row():
        video_output = gr.Video(label="Dream Animation", autoplay=True)
        audio_output = gr.Audio(label="Narration & Music", autoplay=True)
    
    # Örnek Girdiler
    examples = [
        ["A surreal landscape with floating islands and giant jellyfish", "English"],
        ["Una ciudad cyberpunk donde siempre llueve neón", "Spanish"],
        ["Neon yağmurun hiç durmadığı bir siberpunk şehir", "Turkish"]
    ]
    
    def process_dream(dream_text: str, language: str):
        visualizer = DreamVisualizer()
        return visualizer.visualize(dream_text, language)
    
    submit_btn.click(
        fn=process_dream,
        inputs=[dream_input, language_dropdown],
        outputs=[video_output, audio_output],
        examples=examples
    )

if __name__ == "__main__":
    app.launch(share=True)