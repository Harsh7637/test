"""
Enhanced Resume Generator API Endpoints
Uses Gemini AI for content optimization and improvement suggestions
"""
from fastapi import APIRouter, HTTPException
import os
import logging

from app.models.schemas import ResumeRequest, ResumeResponse
from app.services.resume_service import resume_generation_service
from app.utils.pdf_generator import pdf_generator
from app.utils.helpers import generate_short_id

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate", response_model=ResumeResponse)
async def generate_resume(request: ResumeRequest):
    """
    Generate an ATS-optimized resume enhanced with Gemini AI
    
    - Optimizes content for Applicant Tracking Systems using traditional NLP
    - Uses Gemini AI to enhance descriptions and suggestions
    - Applies STAR method to achievements
    - Prioritizes relevant keywords
    - Generates professional PDF
    """
    try:
        logger.info(f"📝 Resume generation request for: {request.name}")
        
        # Generate and enhance resume using both traditional and AI methods
        result = await resume_generation_service.generate_resume(request)
        
        # Generate PDF
        pdf_path = pdf_generator.generate_resume_pdf(
            result.get('optimized_resume', {})
        )
        
        # Get filename from path
        filename = os.path.basename(pdf_path)
        pdf_url = f"/resumes/{filename}"
        
        resume_id = generate_short_id()
        
        logger.info(f"✅ Resume generated successfully: {filename}")
        
        return ResumeResponse(
            pdf_url=pdf_url,
            optimized_resume=result.get('optimized_resume', {}),
            suggestions=result.get('suggestions', []),
            resume_id=resume_id,
            gemini_enhancements=result.get('gemini_enhancements', {}),
            ai_powered=True
        )
    
    except Exception as e:
        logger.error(f"❌ Resume generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Resume generation failed: {str(e)}"
        )


@router.post("/enhance")
async def enhance_resume(resume_dict: dict):
    """
    Enhance an existing resume with Gemini AI
    Provides targeted improvements and suggestions
    """
    try:
        logger.info("📝 Resume enhancement request")
        
        # Enhance resume using Gemini
        enhancements = await resume_generation_service.enhance_resume(resume_dict)
        
        logger.info("✅ Resume enhanced successfully")
        
        return {
            "enhancements": enhancements,
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"❌ Resume enhancement failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Resume enhancement failed: {str(e)}"
        )


@router.get("/service-info")
async def get_service_info():
    """Get information about the resume generation service"""
    try:
        info = resume_generation_service.get_service_info()
        return {"service": info, "status": "operational"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))