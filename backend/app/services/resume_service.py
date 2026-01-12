"""
Enhanced Resume Generation Service
Uses Gemini API for content optimization and ATS analysis
"""
import logging
from typing import Dict
from app.ml.resume_optimizer import resume_optimizer
from app.ml.gemini_client import gemini_client
from app.models.schemas import ResumeRequest

logger = logging.getLogger(__name__)


class EnhancedResumeGenerationService:
    """Business logic for resume generation with Gemini enhancement"""

    def __init__(self):
        self.gemini = gemini_client
        self.optimizer = resume_optimizer

    async def generate_resume(self, request: ResumeRequest) -> Dict:
        """
        Generate and optimize resume using both traditional methods and Gemini AI
        """
        logger.info(f"Resume generation service for: {request.name}")

        try:
            # Convert to dict for optimizer
            resume_dict = {
                'name': request.name,
                'email': request.email,
                'phone': request.phone,
                'target_role': request.target_role,
                'summary': request.summary,
                'skills': request.skills,
                'experience': [exp.dict() for exp in request.experience],
                'education': [edu.dict() for edu in request.education],
                'job_description': request.job_description
            }

            # Traditional optimization
            optimized_result = self.optimizer.optimize_resume(resume_dict)

            # Enhance with Gemini
            logger.info("Enhancing resume with Gemini AI...")
            gemini_enhancements = self.gemini.optimize_resume_content(resume_dict)

            # Merge results
            result = {
                **optimized_result,
                'gemini_enhancements': gemini_enhancements,
                'ai_powered': True
            }

            logger.info("✅ Resume generated and enhanced successfully")
            return result

        except Exception as e:
            logger.error(f"❌ Resume generation failed: {str(e)}")
            raise

    async def enhance_resume(self, resume_dict: Dict) -> Dict:
        """
        Enhance an existing resume with Gemini AI
        """
        logger.info(f"Enhancing resume for: {resume_dict.get('name')}")

        try:
            # Get Gemini enhancements
            gemini_enhancements = self.gemini.optimize_resume_content(resume_dict)

            # Get enhanced bullet points if experience exists
            enhanced_bullets = []
            if resume_dict.get('experience'):
                job_desc = resume_dict.get('job_description', '')
                for exp in resume_dict.get('experience', []):
                    if exp.get('description'):
                        bullets = exp.get('description').split('\n')
                        enhanced = self.gemini.enhance_bullet_points(
                            bullets, job_desc
                        )
                        enhanced_bullets.append({
                            'company': exp.get('company'),
                            'enhanced_bullets': enhanced
                        })

            return {
                'gemini_enhancements': gemini_enhancements,
                'enhanced_bullets': enhanced_bullets,
                'timestamp': __import__('datetime').datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Resume enhancement failed: {str(e)}")
            raise

    def get_service_info(self) -> Dict:
        """Get service information"""
        return {
            "service": "Enhanced Resume Generation",
            "providers": ["Traditional NLP", "Gemini AI"],
            "capabilities": [
                "Resume content optimization",
                "ATS compatibility analysis",
                "Bullet point enhancement",
                "Job keyword extraction"
            ]
        }


resume_generation_service = EnhancedResumeGenerationService()


