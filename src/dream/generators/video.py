from diffusers import StableVideoDiffusionPipeline
import torch
from pathlib import Path
import cv2
import numpy as np
from ..utils.logger import logger
from config import config

class VideoGenerator:
    def __init__(self):
        self.pipe = StableVideoDiffusionPipeline.from_pretrained(
            config.VIDEO_MODEL,
            torch_dtype=config.TORCH_DTYPE,
        ).to(config.TORCH_DEVICE)
        logger.info(f"Stable Video Diffusion model loaded on {config.TORCH_DEVICE}")

    def generate(self, image_path: Path, output_path: Path) -> Path:
        """Generates video from input image."""
        try:
            # Input validation
            if not image_path.exists():
                raise FileNotFoundError(f"Input image not found: {image_path}")
                
            image = cv2.imread(str(image_path))
            if image is None:
                raise ValueError("Failed to load input image")
                
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Generate frames with progress tracking
            frames = self.pipe(
                image,
                num_frames=config.VIDEO_FPS * config.VIDEO_DURATION,
                decode_chunk_size=8,
                num_inference_steps=30
            ).frames
            
            # Save video with proper encoding
            self._save_video(frames, output_path)
            
            logger.info(f"Video generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Video generation failed: {str(e)}")
            raise
            
    def _save_video(self, frames: list, output_path: Path):
        """Saves frames as video with proper encoding."""
        height, width, _ = frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        with cv2.VideoWriter(str(output_path), fourcc, config.VIDEO_FPS, (width, height)) as video:
            for frame in frames:
                video.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))