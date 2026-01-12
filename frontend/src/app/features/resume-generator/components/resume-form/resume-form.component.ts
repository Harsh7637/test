import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ResumeRequest, Experience, Education } from '../../../../shared/models/resume.model';

@Component({
  selector: 'app-resume-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './resume-form.component.html',
  styleUrls: ['./resume-form.component.css']
})
export class ResumeFormComponent {
  @Input() resumeData!: ResumeRequest;
  @Input() loading: boolean = false;
  @Output() generateResume = new EventEmitter<void>();
  @Output() dataChange = new EventEmitter<ResumeRequest>();

  skillsInput: string = '';

  addExperience() {
    this.resumeData.experience.push({
      title: '',
      company: '',
      duration: '',
      responsibilities: ['']
    });
    this.emitChange();
  }

  removeExperience(index: number) {
    if (this.resumeData.experience.length > 1) {
      this.resumeData.experience.splice(index, 1);
      this.emitChange();
    }
  }

  addResponsibility(expIndex: number) {
    this.resumeData.experience[expIndex].responsibilities.push('');
    this.emitChange();
  }

  removeResponsibility(expIndex: number, respIndex: number) {
    const responsibilities = this.resumeData.experience[expIndex].responsibilities;
    if (responsibilities.length > 1) {
      responsibilities.splice(respIndex, 1);
      this.emitChange();
    }
  }

  addEducation() {
    this.resumeData.education.push({
      degree: '',
      institution: '',
      year: '',
      gpa: ''
    });
    this.emitChange();
  }

  removeEducation(index: number) {
    if (this.resumeData.education.length > 1) {
      this.resumeData.education.splice(index, 1);
      this.emitChange();
    }
  }

  onGenerate() {
    // Parse skills from comma-separated input
    this.resumeData.skills = this.skillsInput
      .split(',')
      .map(s => s.trim())
      .filter(s => s.length > 0);
    
    this.generateResume.emit();
  }

  emitChange() {
    this.dataChange.emit(this.resumeData);
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
}


