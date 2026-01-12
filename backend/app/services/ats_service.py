"""
Enhanced ATS Analysis Service
Uses Gemini API for comprehensive ATS compatibility analysis
"""
import logging
from typing import Dict
from app.ml.ats_scorer import ats_scorer
from app.ml.gemini_client import gemini_client
from app.models.schemas import ATSAnalyzerRequest

logger = logging.getLogger(__name__)


class EnhancedATSAnalysisService:
    """Business logic for ATS analysis with Gemini AI enhancement"""

    def __init__(self):
        self.gemini = gemini_client
        self.traditional_scorer = ats_scorer

    async def analyze_resume(self, request: ATSAnalyzerRequest) -> Dict:
        """
        Analyze resume with business logic layer using both traditional and AI methods
        """
        logger.info("Enhanced ATS analysis service started")

        try:
            # Traditional analysis
            logger.info("Performing traditional ATS analysis...")
            traditional_result = self.traditional_scorer.analyze_resume(
                resume_text=request.resume_text,
                job_description=request.job_description
            )

            # Gemini-powered analysis
            logger.info("Performing Gemini AI analysis...")
            gemini_analysis = self.gemini.analyze_ats_compatibility(
                resume_content=request.resume_text,
                job_description=request.job_description
            )

            # Combine results
            result = {
                'traditional_analysis': traditional_result,
                'gemini_analysis': gemini_analysis,
                'combined_score': (
                    (traditional_result.get('ats_score', 0) + 
                     gemini_analysis.get('ats_score', 0)) / 2
                ),
                'ai_powered': True
            }

            logger.info("✅ ATS analysis completed successfully")
            return result

        except Exception as e:
            logger.error(f"❌ ATS analysis failed: {str(e)}")
            raise

    async def get_improvement_suggestions(self, request: ATSAnalyzerRequest) -> Dict:
        """
        Get specific improvement suggestions from Gemini AI
        """
        logger.info("Getting AI-powered improvement suggestions...")

        try:
            suggestions = self.gemini.analyze_ats_compatibility(
                resume_content=request.resume_text,
                job_description=request.job_description
            )

            return {
                'improvements': suggestions.get('improvements', []),
                'missing_keywords': suggestions.get('missing_keywords', []),
                'formatting_issues': suggestions.get('formatting_issues', []),
                'overall_assessment': suggestions.get('overall_assessment', '')
            }

        except Exception as e:
            logger.error(f"❌ Suggestion generation failed: {str(e)}")
            raise

    async def generate_cover_letter(self, resume_text: str, job_description: str, company_name: str) -> Dict:
        """
        Generate a customized cover letter using Gemini AI
        """
        logger.info(f"Generating cover letter for: {company_name}")

        try:
            # Extract resume data for context
            resume_dict = {
                'name': 'Applicant',
                'target_role': '',
                'summary': resume_text[:200],
                'skills': []
            }

            cover_letter = self.gemini.generate_cover_letter(
                resume_dict=resume_dict,
                job_description=job_description,
                company_name=company_name
            )

            return {
                'cover_letter': cover_letter,
                'company': company_name,
                'generated_at': __import__('datetime').datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Cover letter generation failed: {str(e)}")
            raise

    def get_service_info(self) -> Dict:
        """Get service information"""
        return {
            "service": "Enhanced ATS Analysis",
            "providers": ["Traditional NLP", "Gemini AI"],
            "capabilities": [
                "Resume ATS compatibility analysis",
                "Keyword matching",
                "Formatting validation",
                "Improvement suggestions",
                "Cover letter generation"
            ]
        }


ats_analysis_service = EnhancedATSAnalysisService()