"""
Enhanced Image Generation API Endpoints
Uses Gemini AI for image descriptions and metadata
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging

from app.models.schemas import ImageGenerationRequest, ImageGenerationResponse
from app.services.image_service import image_generation_service
from app.ml.gemini_client import gemini_client

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """
    Generate images using Pollinations.ai API with Gemini prompt enhancement
    
    - **prompt**: Text description of the desired image
    - **style**: Artistic style (realistic, anime, sketch, 3d, watercolor)
    - **width/height**: Image dimensions (512-1024px)
    - **num_inference_steps**: Quality vs speed tradeoff (10-50)
    - **guidance_scale**: How closely to follow prompt (1-20)
    """
    try:
        logger.info(f"🎨 Image generation request: {request.prompt[:50]}...")
        
        # Generate image using Pollinations.ai
        result = await image_generation_service.generate_image(request)
        
        return ImageGenerationResponse(
            image_url=result.get('image_url', ''),
            prompt=result.get('metadata', {}).get('original_prompt', request.prompt),
            style=request.style.value,
            generation_time=result.get('generation_time', 0),
            image_id=result.get('metadata', {}).get('id', ''),
            enhanced_description=result.get('enhanced_prompt', ''),
            message=result.get('message', ''),
            image_path=result.get('image_path'),
            metadata=result.get('metadata')
        )
    
    except Exception as e:
        logger.error(f"❌ Image generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Image generation failed: {str(e)}"
        )


@router.get("/model-info")
async def get_model_info():
    """Get information about the image generation service"""
    try:
        info = image_generation_service.get_service_info()
        gemini_info = gemini_client.get_model_info()
        
        return JSONResponse(
            content={
                "service": info,
                "ai_provider": gemini_info
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))