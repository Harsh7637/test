"""
Gemini API Client
Handles all interactions with Google's Generative AI API
"""
import logging
import json
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai
from PIL import Image
import io
import base64

from app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiClient:
    """
    Google Gemini API Client
    Handles text generation, image analysis, and content enhancement
    """

    def __init__(self):
        self.client_initialized = False
        self.model = None
        self.initialize_client()

    def initialize_client(self):
        """Initialize Gemini API client"""
        if self.client_initialized:
            return

        try:
            api_key = settings.GEMINI_API_KEY
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")

            genai.configure(api_key=api_key)
            self.client_initialized = True
            logger.info("✅ Gemini API client initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini API: {str(e)}")
            raise

    def generate_image_description(self, prompt: str, style: str) -> str:
        """
        Generate detailed image description using Gemini
        This can be used for documentation or metadata
        """
        try:
            model = genai.GenerativeModel(settings.GEMINI_MODEL)

            full_prompt = f"""You are an expert image description writer. 
Create a detailed, artistic description for an image generation system based on this request:

User Prompt: {prompt}
Style: {style}

Provide an enhanced description that:
1. Maintains the core user intent
2. Adds artistic and technical details appropriate for the style
3. Includes lighting, composition, and mood suggestions
4. Is concise but vivid (max 150 words)

Return ONLY the enhanced description, no additional text."""

            response = model.generate_content(full_prompt)
            return response.text

        except Exception as e:
            logger.error(f"❌ Image description generation failed: {str(e)}")
            raise

    def optimize_resume_content(self, resume_dict: Dict) -> Dict:
        """
        Use Gemini to optimize resume content
        Enhances descriptions, suggests improvements, and ensures ATS compatibility
        """
        try:
            model = genai.GenerativeModel(settings.GEMINI_MODEL)

            # Prepare resume summary for Gemini
            resume_summary = f"""
Name: {resume_dict.get('name', 'N/A')}
Target Role: {resume_dict.get('target_role', 'N/A')}
Summary: {resume_dict.get('summary', 'N/A')}
Skills: {', '.join(resume_dict.get('skills', []))}
Target Job Description: {resume_dict.get('job_description', 'N/A')[:500]}
"""

            prompt = f"""You are an expert resume writer and ATS specialist. 
Analyze this resume and provide optimization suggestions:

{resume_summary}

Provide a JSON response with the following structure:
{{
    "summary_enhancement": "An improved 2-3 sentence professional summary that aligns with the job description",
    "suggested_skills": ["skill1", "skill2", "skill3", ...],
    "ats_score_feedback": "Brief feedback on ATS compatibility (0-100)",
    "improvement_suggestions": ["suggestion1", "suggestion2", "suggestion3"],
    "keyword_recommendations": ["keyword1", "keyword2", "keyword3"]
}}

Ensure the response is ONLY valid JSON."""

            response = model.generate_content(prompt)
            response_text = response.text

            # Parse JSON from response
            try:
                # Try to extract JSON from response
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                if json_start != -1 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    return json.loads(json_str)
            except json.JSONDecodeError:
                logger.warning("Could not parse JSON response from Gemini")

            return {
                "summary_enhancement": response_text,
                "suggested_skills": [],
                "ats_score_feedback": "Unable to parse structured response",
                "improvement_suggestions": [],
                "keyword_recommendations": []
            }

        except Exception as e:
            logger.error(f"❌ Resume optimization failed: {str(e)}")
            raise

    def enhance_bullet_points(self, bullets: List[str], job_description: str) -> List[str]:
        """
        Use Gemini to enhance resume bullet points
        Makes them more impactful and ATS-friendly
        """
        try:
            model = genai.GenerativeModel(settings.GEMINI_MODEL)

            bullets_text = "\n".join([f"- {bullet}" for bullet in bullets])

            prompt = f"""You are an expert resume writer specializing in ATS optimization and impact.
Enhance these resume bullet points to be more impactful and ATS-friendly:

BULLET POINTS:
{bullets_text}

JOB DESCRIPTION:
{job_description[:500]}

Requirements for enhanced bullets:
1. Start with strong action verbs
2. Quantify achievements with metrics
3. Include relevant keywords from job description
4. Ensure ATS compatibility (no special characters)
5. Maintain professional tone

Return ONLY the enhanced bullet points, one per line, starting with a dash (-)."""

            response = model.generate_content(prompt)
            enhanced_bullets = response.text.strip().split("\n")
            # Clean up bullet points
            cleaned = [
                bullet.strip().lstrip("-").strip()
                for bullet in enhanced_bullets
                if bullet.strip()
            ]
            return cleaned

        except Exception as e:
            logger.error(f"❌ Bullet point enhancement failed: {str(e)}")
            raise

    def analyze_ats_compatibility(
        self, resume_content: str, job_description: str
    ) -> Dict:
        """
        Use Gemini to analyze ATS compatibility
        Provides detailed score and recommendations
        """
        try:
            model = genai.GenerativeModel(settings.GEMINI_MODEL)

            prompt = f"""You are an expert ATS (Applicant Tracking System) analyst.
Analyze this resume for ATS compatibility with the given job description.

RESUME:
{resume_content[:1000]}

JOB DESCRIPTION:
{job_description[:500]}

Provide a detailed JSON analysis with:
{{
    "ats_score": <0-100 number>,
    "keyword_match_percentage": <0-100 number>,
    "matched_keywords": ["keyword1", "keyword2", ...],
    "missing_keywords": ["keyword1", "keyword2", ...],
    "formatting_issues": ["issue1", "issue2", ...],
    "strengths": ["strength1", "strength2", ...],
    "improvements": ["improvement1", "improvement2", ...],
    "overall_assessment": "Brief summary of compatibility"
}}

Return ONLY valid JSON."""

            response = model.generate_content(prompt)
            response_text = response.text

            try:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                if json_start != -1 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    return json.loads(json_str)
            except json.JSONDecodeError:
                logger.warning("Could not parse JSON response from Gemini")

            return {
                "ats_score": 0,
                "keyword_match_percentage": 0,
                "matched_keywords": [],
                "missing_keywords": [],
                "formatting_issues": [],
                "strengths": [],
                "improvements": [],
                "overall_assessment": "Analysis pending"
            }

        except Exception as e:
            logger.error(f"❌ ATS compatibility analysis failed: {str(e)}")
            raise

    def generate_cover_letter(
        self, resume_dict: Dict, job_description: str, company_name: str
    ) -> str:
        """
        Generate a personalized cover letter using Gemini
        """
        try:
            model = genai.GenerativeModel(settings.GEMINI_MODEL)

            prompt = f"""You are an expert cover letter writer. 
Generate a compelling, professional cover letter based on the following information:

CANDIDATE:
Name: {resume_dict.get('name', 'N/A')}
Target Role: {resume_dict.get('target_role', 'N/A')}
Summary: {resume_dict.get('summary', 'N/A')}
Key Skills: {', '.join(resume_dict.get('skills', [])[:5])}

COMPANY: {company_name}

JOB DESCRIPTION:
{job_description[:500]}

Requirements:
1. Professional and engaging tone
2. 3-4 paragraphs
3. Highlight relevant achievements
4. Show genuine interest in the company
5. End with call to action

Return ONLY the cover letter content, ready to use."""

            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            logger.error(f"❌ Cover letter generation failed: {str(e)}")
            raise

    def extract_job_keywords(self, job_description: str) -> List[str]:
        """
        Extract important keywords from job description using Gemini
        """
        try:
            model = genai.GenerativeModel(settings.GEMINI_MODEL)

            prompt = f"""Extract the top 20 most important keywords and skills from this job description.
These will be used to match against resumes.

JOB DESCRIPTION:
{job_description}

Return ONLY a JSON array of keywords as strings, like: ["keyword1", "keyword2", ...]"""

            response = model.generate_content(prompt)
            response_text = response.text

            try:
                json_start = response_text.find("[")
                json_end = response_text.rfind("]") + 1
                if json_start != -1 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    return json.loads(json_str)
            except json.JSONDecodeError:
                logger.warning("Could not parse JSON response from Gemini")
                return []

        except Exception as e:
            logger.error(f"❌ Job keyword extraction failed: {str(e)}")
            raise

    def get_model_info(self) -> Dict:
        """Get information about the Gemini API client"""
        return {
            "provider": "Google Gemini",
            "model": settings.GEMINI_MODEL,
            "initialized": self.client_initialized,
            "capabilities": [
                "Image description generation",
                "Resume optimization",
                "ATS compatibility analysis",
                "Cover letter generation",
                "Job keyword extraction",
                "Content enhancement"
            ]
        }


# Singleton instance
_gemini_client = None


def get_gemini_client() -> GeminiClient:
    """Get or create the Gemini API client singleton"""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client


gemini_client = get_gemini_client()
