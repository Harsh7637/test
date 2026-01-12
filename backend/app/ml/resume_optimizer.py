"""
Resume Content Optimizer
Optimizes resume content for ATS compatibility and impact
"""
import re
import logging
from typing import List, Dict, Tuple
from collections import Counter

logger = logging.getLogger(__name__)

class ResumeOptimizer:
    """
    Resume Content Optimization Engine
    Applies best practices for ATS-friendly, impactful resumes
    """
    
    def __init__(self):
        # Strong action verbs categorized by type
        self.action_verbs = {
            'leadership': ['Led', 'Directed', 'Managed', 'Supervised', 'Coordinated', 'Spearheaded', 'Orchestrated'],
            'achievement': ['Achieved', 'Exceeded', 'Surpassed', 'Delivered', 'Accomplished', 'Attained'],
            'technical': ['Developed', 'Engineered', 'Designed', 'Built', 'Architected', 'Implemented', 'Created'],
            'improvement': ['Improved', 'Optimized', 'Streamlined', 'Enhanced', 'Refined', 'Upgraded', 'Transformed'],
            'analytical': ['Analyzed', 'Evaluated', 'Assessed', 'Investigated', 'Researched', 'Examined'],
            'communication': ['Presented', 'Communicated', 'Collaborated', 'Negotiated', 'Facilitated'],
            'financial': ['Reduced costs', 'Increased revenue', 'Saved', 'Generated', 'Budgeted']
        }
        
        # All action verbs flattened
        self.all_action_verbs = [verb for verbs in self.action_verbs.values() for verb in verbs]
        
        # Weak words to avoid
        self.weak_words = [
            'responsible for', 'duties included', 'worked on', 'helped with',
            'assisted', 'participated', 'involved in', 'tasked with'
        ]
    
    def extract_jd_keywords(self, job_description: str, top_n: int = 25) -> List[str]:
        """
        Extract the most important keywords from job description
        """
        # Remove common stopwords
        stopwords = {
            'the', 'and', 'for', 'with', 'this', 'that', 'from', 'will', 'are',
            'our', 'you', 'your', 'about', 'all', 'also', 'any', 'have', 'has',
            'can', 'could', 'should', 'would', 'must', 'may', 'very', 'more'
        }
        
        # Extract words (3+ characters)
        words = re.findall(r'\b[A-Za-z]{3,}\b', job_description.lower())
        
        # Filter stopwords and count frequency
        filtered = [w for w in words if w not in stopwords]
        word_freq = Counter(filtered)
        
        # Get top N keywords
        top_keywords = [word for word, count in word_freq.most_common(top_n)]
        
        # Also extract technical terms (capitalized phrases)
        tech_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', job_description)
        tech_terms = list(set([term.lower() for term in tech_terms if len(term) > 2]))
        
        # Combine and return unique keywords
        all_keywords = list(set(top_keywords + tech_terms))
        
        return all_keywords[:top_n]
    
    def optimize_bullet_point(
        self,
        bullet: str,
        jd_keywords: List[str],
        category: str = 'technical'
    ) -> str:
        """
        Optimize a single bullet point using best practices
        """
        bullet = bullet.strip()
        
        # Remove weak phrases
        for weak in self.weak_words:
            if weak in bullet.lower():
                bullet = re.sub(re.escape(weak), '', bullet, flags=re.IGNORECASE)
                bullet = bullet.strip()
        
        # Ensure it starts with a strong action verb
        words = bullet.split()
        if words:
            first_word = words[0]
            
            # If first word is not a strong action verb, replace it
            if first_word not in self.all_action_verbs:
                # Choose appropriate action verb based on category
                verbs = self.action_verbs.get(category, self.action_verbs['technical'])
                action_verb = verbs[0]  # Default to first in category
                
                # Keep the rest of the sentence
                bullet = f"{action_verb} {' '.join(words)}"
        
        # Ensure proper capitalization
        if bullet:
            bullet = bullet[0].upper() + bullet[1:]
        
        # Remove any double spaces
        bullet = re.sub(r'\s+', ' ', bullet)
        
        # Try to incorporate relevant JD keywords naturally
        bullet_lower = bullet.lower()
        incorporated = False
        
        for keyword in jd_keywords[:5]:  # Top 5 keywords
            if keyword.lower() not in bullet_lower and len(bullet) < 150:
                # Add keyword naturally
                if 'using' not in bullet_lower:
                    bullet = f"{bullet} using {keyword}"
                    incorporated = True
                    break
                elif 'with' not in bullet_lower[-20:]:  # Check last 20 chars
                    bullet = f"{bullet} with {keyword}"
                    incorporated = True
                    break
        
        return bullet.strip()
    
    def generate_professional_summary(
        self,
        name: str,
        target_role: str,
        years_experience: int,
        top_skills: List[str],
        jd_keywords: List[str]
    ) -> str:
        """
        Generate an impactful professional summary
        """
        # Incorporate JD keywords into summary
        relevant_skills = []
        for skill in top_skills[:6]:
            if any(keyword in skill.lower() for keyword in jd_keywords):
                relevant_skills.insert(0, skill)
            else:
                relevant_skills.append(skill)
        
        skills_str = ', '.join(relevant_skills[:5])
        
        # Generate summary based on experience level
        if years_experience >= 7:
            level = "seasoned"
            descriptor = "extensive expertise"
        elif years_experience >= 4:
            level = "experienced"
            descriptor = "proven track record"
        elif years_experience >= 2:
            level = "motivated"
            descriptor = "solid foundation"
        else:
            level = "emerging"
            descriptor = "strong foundation"
        
        summary = (
            f"Results-driven {target_role} with {years_experience}+ years of "
            f"{descriptor} in {skills_str}. {level.capitalize()} professional "
            f"specializing in delivering high-impact solutions that drive business growth "
            f"and operational excellence through innovative approaches and technical expertise."
        )
        
        return summary
    
    def optimize_experience_section(
        self,
        experiences: List[Dict],
        jd_keywords: List[str]
    ) -> List[Dict]:
        """
        Optimize all experience entries
        """
        optimized = []
        
        for idx, exp in enumerate(experiences):
            optimized_exp = exp.copy()
            
            # Determine category based on job title
            title_lower = exp.get('title', '').lower()
            if 'manager' in title_lower or 'lead' in title_lower:
                category = 'leadership'
            elif 'engineer' in title_lower or 'developer' in title_lower:
                category = 'technical'
            elif 'analyst' in title_lower:
                category = 'analytical'
            else:
                category = 'achievement'
            
            # Optimize each responsibility
            optimized_responsibilities = []
            responsibilities = exp.get('responsibilities', [])
            
            for bullet in responsibilities:
                if bullet.strip():
                    optimized_bullet = self.optimize_bullet_point(
                        bullet,
                        jd_keywords,
                        category
                    )
                    optimized_responsibilities.append(optimized_bullet)
            
            # Limit to 4-6 bullets per job (ATS best practice)
            if len(optimized_responsibilities) > 6:
                optimized_responsibilities = optimized_responsibilities[:6]
            
            optimized_exp['responsibilities'] = optimized_responsibilities
            optimized.append(optimized_exp)
        
        return optimized
    
    def prioritize_skills(
        self,
        skills: List[str],
        jd_keywords: List[str]
    ) -> List[str]:
        """
        Prioritize skills based on job description relevance
        """
        jd_keywords_lower = [k.lower() for k in jd_keywords]
        
        # Categorize skills
        relevant = []  # Skills matching JD
        technical = []  # Technical skills
        soft = []      # Soft skills
        other = []     # Other skills
        
        soft_skill_indicators = ['communication', 'leadership', 'management', 'team', 'collaboration']
        
        for skill in skills:
            skill_lower = skill.lower()
            
            # Check if skill matches JD keywords
            if any(keyword in skill_lower for keyword in jd_keywords_lower):
                relevant.append(skill)
            # Check if it's a soft skill
            elif any(indicator in skill_lower for indicator in soft_skill_indicators):
                soft.append(skill)
            # Check if it's technical (has uppercase, numbers, or special chars)
            elif any(c.isupper() for c in skill) or any(c.isdigit() for c in skill):
                technical.append(skill)
            else:
                other.append(skill)
        
        # Prioritize: Relevant > Technical > Other > Soft
        prioritized = relevant + technical + other + soft
        
        # Remove duplicates while preserving order
        seen = set()
        final = []
        for skill in prioritized:
            if skill.lower() not in seen:
                seen.add(skill.lower())
                final.append(skill)
        
        return final
    
    def generate_suggestions(
        self,
        resume_data: Dict,
        has_numbers: bool
    ) -> List[str]:
        """
        Generate personalized improvement suggestions
        """
        suggestions = []
        
        # Check for quantifiable metrics
        if not has_numbers:
            suggestions.append(
                "📊 Add quantifiable achievements with specific metrics "
                "(e.g., 'Increased efficiency by 40%', 'Reduced costs by $50K annually')"
            )
        
        # Check bullet point count
        total_bullets = sum(
            len(exp.get('responsibilities', []))
            for exp in resume_data.get('experience', [])
        )
        
        if total_bullets < 8:
            suggestions.append(
                "📝 Add more detailed accomplishments to showcase your impact "
                "(aim for 4-6 bullet points per role)"
            )
        
        # Check skills count
        skills_count = len(resume_data.get('skills', []))
        if skills_count < 8:
            suggestions.append(
                "💡 Include more relevant technical skills and competencies "
                "(aim for 10-15 skills)"
            )
        elif skills_count > 20:
            suggestions.append(
                "✂️ Consider focusing on your most relevant and strongest skills "
                "(10-15 skills is ideal)"
            )
        
        # General best practices
        suggestions.extend([
            "⭐ Use the STAR method (Situation, Task, Action, Result) for impactful descriptions",
            "🎯 Tailor your resume for each specific job application",
            "📄 Keep resume length to 1-2 pages maximum",
            "✅ Proofread carefully for spelling and grammar errors",
            "🔄 Update your resume regularly with new skills and achievements"
        ])
        
        return suggestions
    
    def optimize_resume(self, resume_data: Dict) -> Dict:
        """
        Perform complete resume optimization
        
        Args:
            resume_data: Dictionary containing all resume information
        
        Returns:
            Dictionary with optimized resume and suggestions
        """
        logger.info("🔧 Optimizing resume content...")
        
        # Extract JD keywords
        jd_keywords = self.extract_jd_keywords(
            resume_data.get('job_description', '')
        )
        
        # Calculate years of experience
        years_experience = len(resume_data.get('experience', []))
        
        # Generate professional summary
        summary = self.generate_professional_summary(
            name=resume_data.get('name', ''),
            target_role=resume_data.get('target_role', ''),
            years_experience=years_experience,
            top_skills=resume_data.get('skills', []),
            jd_keywords=jd_keywords
        )
        
        # Optimize experience section
        optimized_experience = self.optimize_experience_section(
            resume_data.get('experience', []),
            jd_keywords
        )
        
        # Prioritize skills
        prioritized_skills = self.prioritize_skills(
            resume_data.get('skills', []),
            jd_keywords
        )
        
        # Check for quantifiable achievements
        all_text = ' '.join([
            bullet
            for exp in optimized_experience
            for bullet in exp.get('responsibilities', [])
        ])
        has_numbers = bool(re.search(r'\d+', all_text))
        
        # Generate suggestions
        suggestions = self.generate_suggestions(
            resume_data,
            has_numbers
        )
        
        # Build optimized resume
        optimized_resume = {
            'name': resume_data.get('name'),
            'email': resume_data.get('email'),
            'phone': resume_data.get('phone'),
            'summary': summary,
            'skills': prioritized_skills,
            'experience': optimized_experience,
            'education': resume_data.get('education', []),
            'target_role': resume_data.get('target_role')
        }
        
        logger.info("✅ Resume optimization complete")
        
        return {
            'optimized_resume': optimized_resume,
            'suggestions': suggestions,
            'jd_keywords': jd_keywords[:10],  # Top 10 keywords for reference
            'optimization_applied': True
        }

# Global instance
_resume_optimizer = None

def get_resume_optimizer() -> ResumeOptimizer:
    """Get or create the global resume optimizer instance"""
    global _resume_optimizer
    if _resume_optimizer is None:
        _resume_optimizer = ResumeOptimizer()
    return _resume_optimizer

resume_optimizer = get_resume_optimizer()