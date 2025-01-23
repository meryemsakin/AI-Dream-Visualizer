from diffusers import StableDiffusionXLPipeline
import torch
from pathlib import Path
from ..utils.logger import logger
from config import config

class ImageGenerator:
    def __init__(self):
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            config.SD_MODEL,
            torch_dtype=config.TORCH_DTYPE,
            use_safetensors=True
        ).to(config.TORCH_DEVICE)
        logger.info(f"Stable Diffusion XL model loaded on {config.TORCH_DEVICE}")

    def generate(self, prompt: str, output_path: Path) -> Path:
        """Generates image from text prompt."""
        try:
            # Input validation
            if not prompt or len(prompt.strip()) == 0:
                raise ValueError("Empty prompt provided")
                
            # Generate image with safety checks
            with torch.inference_mode():
                image = self.pipe(
                    prompt=prompt,
                    num_inference_steps=30,
                    guidance_scale=7.5
                ).images[0]
                
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save image with proper format
            image.save(output_path, format='PNG', quality=95)
            
            logger.info(f"Image generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            raise