import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ResumeService } from '../../core/services/resume.service';
import { ResumeRequest, ResumeResponse, Experience, Education } from '../../shared/models/resume.model';

@Component({
  selector: 'app-resume-generator',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './resume-generator.component.html',
  styleUrls: ['./resume-generator.component.css']
})
export class ResumeGeneratorComponent {
  resumeData: ResumeRequest = {
    name: '',
    email: '',
    phone: '',
    target_role: '',
    skills: [],
    experience: [{ title: '', company: '', duration: '', responsibilities: [''] }],
    education: [{ degree: '', institution: '', year: '', gpa: '' }],
    job_description: ''
  };

  skillsInput = '';
  loading = false;
  error = '';
  result: ResumeResponse | null = null;

  constructor(private resumeService: ResumeService) {}

  addExperience() {
    this.resumeData.experience.push({
      title: '',
      company: '',
      duration: '',
      responsibilities: ['']
    });
  }

  removeExperience(index: number) {
    if (this.resumeData.experience.length > 1) {
      this.resumeData.experience.splice(index, 1);
    }
  }

  addResponsibility(expIndex: number) {
    this.resumeData.experience[expIndex].responsibilities.push('');
  }

  removeResponsibility(expIndex: number, respIndex: number) {
    if (this.resumeData.experience[expIndex].responsibilities.length > 1) {
      this.resumeData.experience[expIndex].responsibilities.splice(respIndex, 1);
    }
  }

  addEducation() {
    this.resumeData.education.push({
      degree: '',
      institution: '',
      year: '',
      gpa: ''
    });
  }

  removeEducation(index: number) {
    if (this.resumeData.education.length > 1) {
      this.resumeData.education.splice(index, 1);
    }
  }

  isFormValid(): boolean {
    return !!(
      this.resumeData.name &&
      this.resumeData.email &&
      this.resumeData.phone &&
      this.resumeData.target_role &&
      this.skillsInput &&
      this.resumeData.job_description
    );
  }

  generateResume() {
    if (!this.isFormValid()) {
      this.error = 'Please fill all required fields';
      return;
    }

    this.loading = true;
    this.error = '';
    
    // Parse skills
    this.resumeData.skills = this.skillsInput.split(',').map(s => s.trim()).filter(s => s);

    this.resumeService.generateResume(this.resumeData).subscribe({
      next: (response) => {
        this.result = response;
        this.loading = false;
      },
      error: (err) => {
        this.error = err.message || 'Resume generation failed. Please try again.';
        this.loading = false;
      }
    });
  }

  downloadResume() {
    if (this.result) {
      const link = document.createElement('a');
      link.href = this.resumeService.getResumeUrl(this.result.pdf_url);
      link.download = `resume-${Date.now()}.pdf`;
      link.click();
    }
  }

  trackByIndex(index: number): number {
    return index;
  }
}