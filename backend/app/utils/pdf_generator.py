"""
PDF Resume Generator
Creates professional, ATS-friendly PDF resumes
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from typing import Dict, List
import os
import logging
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)

class PDFResumeGenerator:
    """
    Professional PDF Resume Generator
    Creates clean, ATS-friendly resume PDFs
    """
    
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or settings.RESUME_OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize styles
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles for resume"""
        
        # Name/Header style
        self.styles.add(ParagraphStyle(
            name='ResumeName',
            parent=self.styles['Heading1'],
            fontSize=26,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=4,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=30
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#555555'),
            alignment=TA_CENTER,
            spaceAfter=14,
            fontName='Helvetica'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=8,
            spaceBefore=14,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=colors.HexColor('#2563eb'),
            borderPadding=(0, 0, 3, 0),  # bottom border
            leading=16
        ))
        
        # Job title style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=2,
            fontName='Helvetica-Bold',
            leading=14
        ))
        
        # Company/Institution style
        self.styles.add(ParagraphStyle(
            name='Company',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            spaceAfter=6,
            fontName='Helvetica-Oblique',
            leading=12
        ))
        
        # Bullet point style
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            spaceAfter=4,
            leftIndent=20,
            bulletIndent=10,
            fontName='Helvetica',
            leading=14
        ))
        
        # Professional summary style
        self.styles.add(ParagraphStyle(
            name='Summary',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=14
        ))
        
        # Skills style
        self.styles.add(ParagraphStyle(
            name='Skills',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            spaceAfter=8,
            fontName='Helvetica',
            leading=13
        ))
    
    def _add_header(self, story: List, resume_data: Dict):
        """Add header with name and contact information"""
        # Name
        name = Paragraph(resume_data['name'], self.styles['ResumeName'])
        story.append(name)
        
        # Contact information
        contact_parts = [resume_data['email'], resume_data['phone']]
        contact_info = ' | '.join(contact_parts)
        contact = Paragraph(contact_info, self.styles['ContactInfo'])
        story.append(contact)
        
        # Add a subtle horizontal line
        story.append(HRFlowable(
            width="100%",
            thickness=0.5,
            color=colors.HexColor('#cccccc'),
            spaceAfter=8
        ))
    
    def _add_summary(self, story: List, summary: str):
        """Add professional summary section"""
        if summary:
            header = Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeader'])
            story.append(header)
            
            summary_para = Paragraph(summary, self.styles['Summary'])
            story.append(summary_para)
    
    def _add_skills(self, story: List, skills: List[str]):
        """Add skills section"""
        if skills:
            header = Paragraph("CORE COMPETENCIES", self.styles['SectionHeader'])
            story.append(header)
            
            # Format skills in a clean way (bullet points)
            skills_text = ' • '.join(skills[:15])  # Limit to top 15 skills
            skills_para = Paragraph(skills_text, self.styles['Skills'])
            story.append(skills_para)
    
    def _add_experience(self, story: List, experiences: List[Dict]):
        """Add professional experience section"""
        if experiences:
            header = Paragraph("PROFESSIONAL EXPERIENCE", self.styles['SectionHeader'])
            story.append(header)
            
            for exp in experiences:
                # Job title
                job_title = Paragraph(exp['title'], self.styles['JobTitle'])
                story.append(job_title)
                
                # Company and duration
                company_duration = f"{exp['company']} | {exp['duration']}"
                company = Paragraph(company_duration, self.styles['Company'])
                story.append(company)
                
                # Responsibilities/Achievements
                for resp in exp.get('responsibilities', []):
                    # Clean up the text
                    resp_clean = resp.strip()
                    if resp_clean:
                        bullet_text = f"• {resp_clean}"
                        bullet = Paragraph(bullet_text, self.styles['BulletPoint'])
                        story.append(bullet)
                
                # Add space between jobs
                story.append(Spacer(1, 0.15*inch))
    
    def _add_education(self, story: List, education: List[Dict]):
        """Add education section"""
        if education:
            header = Paragraph("EDUCATION", self.styles['SectionHeader'])
            story.append(header)
            
            for edu in education:
                # Degree
                degree_text = f"<b>{edu['degree']}</b>"
                if edu.get('gpa'):
                    degree_text += f" | GPA: {edu['gpa']}"
                degree = Paragraph(degree_text, self.styles['JobTitle'])
                story.append(degree)
                
                # Institution and year
                institution_year = f"{edu['institution']} | {edu['year']}"
                institution = Paragraph(institution_year, self.styles['Company'])
                story.append(institution)
                
                story.append(Spacer(1, 0.08*inch))
    
    def generate_resume_pdf(self, resume_data: Dict) -> str:
        """
        Generate a professional PDF resume
        
        Args:
            resume_data: Dictionary containing all resume information
        
        Returns:
            Path to generated PDF file
        """
        try:
            logger.info("📄 Generating PDF resume...")
            
            # Create filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = resume_data.get('name', 'resume').replace(' ', '_')
            filename = f"resume_{safe_name}_{timestamp}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.6*inch,
                bottomMargin=0.6*inch
            )
            
            # Build content
            story = []
            
            # Add sections
            self._add_header(story, resume_data)
            
            if resume_data.get('summary'):
                self._add_summary(story, resume_data['summary'])
            
            if resume_data.get('skills'):
                self._add_skills(story, resume_data['skills'])
            
            if resume_data.get('experience'):
                self._add_experience(story, resume_data['experience'])
            
            if resume_data.get('education'):
                self._add_education(story, resume_data['education'])
            
            # Add footer with generation timestamp
            story.append(Spacer(1, 0.3*inch))
            footer_text = f"<i>Generated on {datetime.now().strftime('%B %d, %Y')}</i>"
            footer = Paragraph(footer_text, self.styles['ContactInfo'])
            story.append(footer)
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"✅ PDF generated successfully: {filename}")
            return filepath
            
        except Exception as e:
            logger.error(f"❌ PDF generation failed: {str(e)}")
            raise

# Global instance
_pdf_generator = None

def get_pdf_generator() -> PDFResumeGenerator:
    """Get or create the global PDF generator instance"""
    global _pdf_generator
    if _pdf_generator is None:
        _pdf_generator = PDFResumeGenerator()
    return _pdf_generator

pdf_generator = get_pdf_generator()