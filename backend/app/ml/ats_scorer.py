"""
ATS (Applicant Tracking System) Resume Scorer
Uses NLP and ML to analyze resume compatibility with job descriptions
"""
import re
import logging
from typing import List, Dict, Tuple
from collections import Counter
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from app.core.config import settings

logger = logging.getLogger(__name__)

class ATSScorer:
    """
    ATS Resume Analyzer
    Provides comprehensive resume analysis using NLP and semantic matching
    """
    
    def __init__(self):
        self.nlp = None
        self.sentence_model = None
        self.models_loaded = False
        
        # Required resume sections
        self.required_sections = {
            'contact': ['email', 'phone', 'contact', 'linkedin', '@', 'tel'],
            'experience': ['experience', 'work history', 'employment', 'professional experience'],
            'education': ['education', 'degree', 'university', 'college', 'bachelor', 'master'],
            'skills': ['skills', 'technologies', 'proficiencies', 'technical skills', 'core competencies']
        }
        
        # Common ATS-friendly action verbs
        self.action_verbs = [
            'achieved', 'administered', 'analyzed', 'architected', 'built',
            'collaborated', 'created', 'delivered', 'designed', 'developed',
            'directed', 'engineered', 'established', 'executed', 'improved',
            'implemented', 'increased', 'launched', 'led', 'managed',
            'optimized', 'orchestrated', 'reduced', 'redesigned', 'spearheaded',
            'streamlined', 'transformed'
        ]
    
    def load_models(self):
        """Load NLP models (spaCy and Sentence Transformers)"""
        if self.models_loaded:
            return
        
        try:
            logger.info("Loading NLP models...")
            
            # Load spaCy for keyword extraction
            try:
                self.nlp = spacy.load(settings.SPACY_MODEL)
            except OSError:
                logger.warning("spaCy model not found, downloading...")
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", settings.SPACY_MODEL])
                self.nlp = spacy.load(settings.SPACY_MODEL)
            
            # Load Sentence Transformer for semantic similarity
            self.sentence_model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)
            
            self.models_loaded = True
            logger.info("✅ NLP models loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load NLP models: {str(e)}")
            raise
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract meaningful keywords from text using NLP
        """
        self.load_models()
        
        doc = self.nlp(text.lower())
        keywords = set()
        
        # Extract nouns and proper nouns (likely to be skills/technologies)
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2 and not token.is_stop:
                keywords.add(token.text)
        
        # Extract noun chunks (multi-word phrases like "machine learning")
        for chunk in doc.noun_chunks:
            if len(chunk.text) > 3 and not all(token.is_stop for token in chunk):
                keywords.add(chunk.text.strip())
        
        # Extract entities (organizations, technologies, etc.)
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'GPE', 'WORK_OF_ART']:
                keywords.add(ent.text.lower())
        
        return list(keywords)
    
    def extract_technical_skills(self, text: str) -> List[str]:
        """
        Extract technical skills and programming languages
        """
        # Common technical patterns
        patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Capitalized terms
            r'\b\w+\.js\b',  # JavaScript frameworks
            r'\bC\+\+\b', r'\bC#\b',  # Programming languages
            r'\b[A-Z]{2,}\b'  # Acronyms (SQL, AWS, etc.)
        ]
        
        skills = set()
        for pattern in patterns:
            matches = re.findall(pattern, text)
            skills.update(matches)
        
        return list(skills)
    
    def calculate_keyword_match(
        self,
        resume_keywords: List[str],
        jd_keywords: List[str]
    ) -> Tuple[float, List[str], List[str]]:
        """
        Calculate keyword matching score
        
        Returns:
            (match_score, matched_keywords, missing_keywords)
        """
        resume_set = set(kw.lower() for kw in resume_keywords)
        jd_set = set(kw.lower() for kw in jd_keywords)
        
        matched = list(resume_set.intersection(jd_set))
        missing = list(jd_set - resume_set)
        
        # Calculate match percentage
        if len(jd_set) == 0:
            match_score = 0
        else:
            match_score = (len(matched) / len(jd_set)) * 100
        
        return match_score, matched, missing
    
    def calculate_semantic_similarity(
        self,
        resume_text: str,
        jd_text: str
    ) -> float:
        """
        Calculate semantic similarity using sentence transformers
        This captures meaning beyond simple keyword matching
        """
        self.load_models()
        
        # Generate embeddings
        resume_embedding = self.sentence_model.encode([resume_text])
        jd_embedding = self.sentence_model.encode([jd_text])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]
        
        # Convert to percentage
        return float(similarity) * 100
    
    def check_sections(self, resume_text: str) -> Dict[str, bool]:
        """
        Check if all required resume sections are present
        """
        text_lower = resume_text.lower()
        sections_found = {}
        
        for section, keywords in self.required_sections.items():
            # Section is found if any of its keywords are present
            sections_found[section] = any(kw in text_lower for kw in keywords)
        
        return sections_found
    
    def calculate_formatting_score(
        self,
        resume_text: str,
        sections: Dict[str, bool]
    ) -> float:
        """
        Calculate formatting and structure quality score
        """
        score = 0
        
        # Check section presence (40 points)
        section_score = (sum(sections.values()) / len(sections)) * 40
        score += section_score
        
        # Check for bullet points (20 points)
        bullet_indicators = ['•', '-', '*', '◦', '▪']
        if any(bullet in resume_text for bullet in bullet_indicators):
            score += 20
        elif '\n-' in resume_text or '\n*' in resume_text:
            score += 15
        
        # Check for appropriate length (20 points)
        word_count = len(resume_text.split())
        if 300 <= word_count <= 1500:  # Ideal resume length
            score += 20
        elif 200 <= word_count < 300 or 1500 < word_count <= 2000:
            score += 15
        elif word_count > 150:
            score += 10
        
        # Check for contact information (20 points)
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text))
        has_phone = bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', resume_text))
        
        if has_email:
            score += 10
        if has_phone:
            score += 10
        
        return min(score, 100)  # Cap at 100
    
    def check_action_verbs(self, resume_text: str) -> Tuple[int, float]:
        """
        Check usage of strong action verbs
        Returns: (count of action verbs, score)
        """
        text_lower = resume_text.lower()
        action_verb_count = sum(1 for verb in self.action_verbs if verb in text_lower)
        
        # Score based on verb usage (max 100)
        verb_score = min((action_verb_count / 10) * 100, 100)
        
        return action_verb_count, verb_score
    
    def check_quantifiable_achievements(self, resume_text: str) -> Tuple[int, bool]:
        """
        Check for quantifiable achievements (numbers, percentages)
        """
        # Look for numbers and percentages
        numbers = re.findall(r'\b\d+\.?\d*%?\b', resume_text)
        has_metrics = len(numbers) > 0
        
        return len(numbers), has_metrics
    
    def generate_suggestions(
        self,
        missing_keywords: List[str],
        sections: Dict[str, bool],
        keyword_score: float,
        semantic_score: float,
        formatting_score: float,
        has_metrics: bool,
        action_verb_count: int
    ) -> List[str]:
        """
        Generate actionable improvement suggestions
        """
        suggestions = []
        
        # Missing sections
        missing_sections = [s for s, present in sections.items() if not present]
        if missing_sections:
            suggestions.append(
                f"✏️ Add missing resume sections: {', '.join(s.title() for s in missing_sections)}"
            )
        
        # Keyword optimization
        if keyword_score < 50:
            suggestions.append(
                "🔑 Include more relevant keywords from the job description in your resume"
            )
        
        if len(missing_keywords) > 0:
            top_missing = sorted(missing_keywords, key=len, reverse=True)[:5]
            suggestions.append(
                f"💡 Consider adding these important skills/keywords: {', '.join(top_missing)}"
            )
        
        # Semantic matching
        if semantic_score < 60:
            suggestions.append(
                "🎯 Better align your experience descriptions with the job requirements and responsibilities"
            )
        
        # Formatting
        if formatting_score < 70:
            suggestions.append(
                "📝 Improve resume formatting: use bullet points, clear section headers, and proper structure"
            )
        
        # Metrics
        if not has_metrics:
            suggestions.append(
                "📊 Add quantifiable achievements with numbers (e.g., 'Increased sales by 40%', 'Led team of 5 engineers')"
            )
        
        # Action verbs
        if action_verb_count < 5:
            suggestions.append(
                "💪 Use strong action verbs to start your bullet points: Led, Developed, Implemented, Achieved, Optimized"
            )
        
        # General best practices
        suggestions.append(
            "⭐ Use the STAR method (Situation, Task, Action, Result) for achievement descriptions"
        )
        
        suggestions.append(
            "✨ Tailor your resume specifically for each job application"
        )
        
        if keyword_score >= 70 and semantic_score >= 70:
            suggestions.append(
                "🎉 Great job! Your resume shows strong alignment with the job description. Consider minor refinements."
            )
        
        return suggestions
    
    def analyze_resume(
        self,
        resume_text: str,
        job_description: str
    ) -> Dict:
        """
        Perform comprehensive ATS analysis
        
        Returns:
            Complete analysis results with scores and suggestions
        """
        logger.info("🔍 Starting ATS analysis...")
        
        # Extract keywords
        resume_keywords = self.extract_keywords(resume_text)
        jd_keywords = self.extract_keywords(job_description)
        
        # Add technical skills
        resume_keywords.extend(self.extract_technical_skills(resume_text))
        jd_keywords.extend(self.extract_technical_skills(job_description))
        
        # Calculate keyword match
        keyword_score, matched, missing = self.calculate_keyword_match(
            resume_keywords, jd_keywords
        )
        
        # Calculate semantic similarity
        semantic_score = self.calculate_semantic_similarity(
            resume_text, job_description
        )
        
        # Check sections
        sections = self.check_sections(resume_text)
        
        # Calculate formatting score
        formatting_score = self.calculate_formatting_score(resume_text, sections)
        
        # Check action verbs
        action_verb_count, verb_score = self.check_action_verbs(resume_text)
        
        # Check for metrics
        metric_count, has_metrics = self.check_quantifiable_achievements(resume_text)
        
        # Calculate overall ATS score (weighted average)
        overall_score = (
            keyword_score * 0.35 +      # 35% keyword matching
            semantic_score * 0.30 +      # 30% semantic similarity
            formatting_score * 0.20 +    # 20% formatting
            verb_score * 0.15            # 15% action verb usage
        )
        
        # Generate suggestions
        suggestions = self.generate_suggestions(
            missing, sections, keyword_score, semantic_score,
            formatting_score, has_metrics, action_verb_count
        )
        
        logger.info(f"✅ Analysis complete. Overall score: {overall_score:.2f}")
        
        return {
            'score': round(overall_score, 2),
            'matched_keywords': matched[:20],  # Top 20
            'missing_keywords': missing[:15],   # Top 15
            'suggestions': suggestions,
            'section_analysis': sections,
            'formatting_score': round(formatting_score, 2),
            'keyword_score': round(keyword_score, 2),
            'semantic_score': round(semantic_score, 2),
            'action_verb_count': action_verb_count,
            'metric_count': metric_count
        }

# Global instance
_ats_scorer = None

def get_ats_scorer() -> ATSScorer:
    """Get or create the global ATS scorer instance"""
    global _ats_scorer
    if _ats_scorer is None:
        _ats_scorer = ATSScorer()
    return _ats_scorer

ats_scorer = get_ats_scorer()