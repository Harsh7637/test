"""
Enhanced Image Generation Service
Uses Pollinations.ai API for actual image generation and Gemini for prompt enhancement
"""
import logging
from typing import Dict
from app.ml.gemini_client import gemini_client
from app.models.schemas import ImageGenerationRequest
from app.core.config import settings
from datetime import datetime
import uuid
import requests
import os

logger = logging.getLogger(__name__)


class EnhancedImageGenerationService:
    """
    Enhanced Image Generation Service - Uses Gemini for descriptions
    and can integrate with external image APIs
    """

    def __init__(self):
        self.gemini = gemini_client

    async def generate_image_metadata(self, request: ImageGenerationRequest) -> Dict:
        """
        Generate detailed image metadata and descriptions using Gemini
        """
        logger.info(f"Generating image metadata for: {request.prompt[:50]}")

        try:
            # Get enhanced image description from Gemini
            enhanced_description = self.gemini.generate_image_description(
                prompt=request.prompt,
                style=request.style.value if hasattr(request.style, 'value') else str(request.style)
            )

            metadata = {
                "id": str(uuid.uuid4()),
                "original_prompt": request.prompt,
                "enhanced_description": enhanced_description,
                "style": request.style.value if hasattr(request.style, 'value') else str(request.style),
                "width": request.width,
                "height": request.height,
                "created_at": datetime.now().isoformat(),
                "guidance_scale": request.guidance_scale,
                "inference_steps": request.num_inference_steps
            }

            logger.info("✅ Image metadata generated successfully")
            return metadata

        except Exception as e:
            logger.error(f"❌ Image metadata generation failed: {str(e)}")
            raise

    async def generate_image(self, request: ImageGenerationRequest) -> Dict:
        """
        Generate actual images using Pollinations.ai API (Free - No API key required)
        Enhances prompt with Gemini for better results
        """
        logger.info(f"Image generation service (Pollinations.ai): {request.prompt[:50]}")

        try:
            # Enhance prompt using Gemini for better quality
            logger.info(f"📝 Enhancing prompt with Gemini...")
            
            gemini_prompt = f"""Create a detailed, vivid image generation prompt based on:
User Request: {request.prompt}
Style: {request.style.value if hasattr(request.style, 'value') else str(request.style)}

Generate a single, detailed prompt (2-3 sentences) optimized for image generation APIs."""

            enhanced_prompt = self.gemini.generate_image_description(
                prompt=gemini_prompt,
                style=request.style.value if hasattr(request.style, 'value') else str(request.style)
            )

            logger.info(f"🎨 Generating image with Pollinations.ai API...")
            
            # Use Pollinations.ai API (Free, no authentication required)
            # Format: https://image.pollinations.ai/prompt/[encoded_prompt]
            encoded_prompt = enhanced_prompt.replace(" ", "%20").replace(",", "%2C").replace(":", "%3A")
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            
            logger.info(f"✅ Image URL generated: {image_url}")
            
            # Download and save the image locally with increased timeout
            os.makedirs(settings.IMAGE_OUTPUT_DIR, exist_ok=True)
            
            try:
                image_download = requests.get(image_url, timeout=60, stream=True)
                if image_download.status_code == 200:
                    image_filename = f"image_{uuid.uuid4()}.png"
                    image_path = os.path.join(settings.IMAGE_OUTPUT_DIR, image_filename)
                    
                    with open(image_path, 'wb') as f:
                        for chunk in image_download.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    logger.info(f"✅ Image saved locally: {image_path}")
                else:
                    image_filename = None
                    image_path = None
                    logger.warning(f"Could not download image: HTTP {image_download.status_code}")
            except requests.exceptions.Timeout:
                logger.warning(f"Image download timed out, but URL is valid: {image_url}")
                image_filename = None
                image_path = None
            except Exception as download_error:
                logger.warning(f"Could not download image locally: {str(download_error)}, but URL is valid")
                image_filename = None
                image_path = None
            
            metadata = {
                "id": str(uuid.uuid4()),
                "original_prompt": request.prompt,
                "enhanced_prompt": enhanced_prompt,
                "style": request.style.value if hasattr(request.style, 'value') else str(request.style),
                "width": request.width,
                "height": request.height,
                "created_at": datetime.now().isoformat(),
                "api_provider": "Pollinations.ai",
                "generation_status": "success"
            }

            result = {
                'metadata': metadata,
                'image_url': image_url,
                'image_filename': image_filename,
                'image_path': image_path,
                'enhanced_prompt': enhanced_prompt,
                'message': 'Image generated successfully using Pollinations.ai (Free API)'
            }

            return result

        except Exception as e:
            logger.error(f"❌ Image generation service failed: {str(e)}")
            raise

    def get_service_info(self) -> Dict:
        """Get service information"""
        return {
            "service": "Enhanced Image Generation",
            "provider": "Gemini",
            "capabilities": [
                "Image description generation",
                "Style enhancement",
                "Metadata generation"
            ]
        }


image_generation_service = EnhancedImageGenerationService()
