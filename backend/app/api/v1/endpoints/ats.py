"""
Enhanced ATS Analyzer API Endpoints
Uses Gemini AI for comprehensive ATS compatibility analysis
"""
from fastapi import APIRouter, HTTPException
import logging

from app.models.schemas import ATSAnalyzerRequest, ATSAnalyzerResponse
from app.services.ats_service import ats_analysis_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=ATSAnalyzerResponse)
async def analyze_resume(request: ATSAnalyzerRequest):
    """
    Analyze resume against job description with Gemini AI enhancement
    
    - Calculates ATS compatibility score (0-100) using multiple methods
    - Uses traditional NLP and Gemini AI for analysis
    - Identifies matched and missing keywords
    - Checks resume structure and formatting
    - Provides actionable improvement suggestions
    """
    try:
        logger.info("🔍 Enhanced ATS analysis request received")
        
        # Perform enhanced ATS analysis (traditional + Gemini)
        analysis = await ats_analysis_service.analyze_resume(request)
        
        # Get combined score
        combined_score = analysis.get('combined_score', 0)
        logger.info(f"✅ Analysis complete. Score: {combined_score:.1f}")
        
        # Extract data from traditional analysis
        traditional = analysis.get('traditional_analysis', {})
        gemini = analysis.get('gemini_analysis', {})
        
        return ATSAnalyzerResponse(
            score=int(combined_score),
            matched_keywords=gemini.get('matched_keywords', traditional.get('matched_keywords', [])),
            missing_keywords=gemini.get('missing_keywords', traditional.get('missing_keywords', [])),
            suggestions=gemini.get('improvements', traditional.get('suggestions', [])),
            section_analysis=traditional.get('section_analysis', {}),
            formatting_score=traditional.get('formatting_score', 0),
            keyword_score=traditional.get('keyword_score', 0),
            semantic_score=traditional.get('semantic_score', 0),
            gemini_assessment=gemini.get('overall_assessment', ''),
            ai_powered=True
        )
    
    except Exception as e:
        logger.error(f"❌ ATS analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"ATS analysis failed: {str(e)}"
        )


@router.post("/improve")
async def get_improvement_suggestions(request: ATSAnalyzerRequest):
    """
    Get AI-powered improvement suggestions for resume
    """
    try:
        logger.info("💡 Getting improvement suggestions")
        
        suggestions = await ats_analysis_service.get_improvement_suggestions(request)
        
        logger.info("✅ Suggestions generated successfully")
        
        return {
            "suggestions": suggestions,
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"❌ Suggestion generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Suggestion generation failed: {str(e)}"
        )


@router.post("/cover-letter")
async def generate_cover_letter(
    resume_text: str,
    job_description: str,
    company_name: str
):
    """
    Generate a customized cover letter using Gemini AI
    """
    try:
        logger.info(f"✍️ Generating cover letter for: {company_name}")
        
        cover_letter = await ats_analysis_service.generate_cover_letter(
            resume_text=resume_text,
            job_description=job_description,
            company_name=company_name
        )
        
        logger.info("✅ Cover letter generated successfully")
        
        return cover_letter
    
    except Exception as e:
        logger.error(f"❌ Cover letter generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Cover letter generation failed: {str(e)}"
        )


@router.get("/service-info")
async def get_service_info():
    """Get information about the ATS analysis service"""
    try:
        info = ats_analysis_service.get_service_info()
        return {"service": info, "status": "operational"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))