// TypeScript file: frontend/src/app/features/ats-analyzer/ats-analyzer.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AtsService } from '../../core/services/ats.service';
import { ATSRequest, ATSResponse } from '../../shared/models/ats.model';
import { LoaderComponent } from '../../shared/components/loader/loader.component';

@Component({
  selector: 'app-ats-analyzer',
  standalone: true,
  imports: [CommonModule, FormsModule, LoaderComponent],
  templateUrl: './ats-analyzer.component.html',
  styleUrls: ['./ats-analyzer.component.css']
})
export class AtsAnalyzerComponent {
  resumeText = '';
  jobDescription = '';
  loading = false;
  error = '';
  result: ATSResponse | null = null;

  constructor(private atsService: AtsService) {}

  analyzeResume() {
    if (!this.resumeText || !this.jobDescription) {
      this.error = 'Please fill both fields';
      return;
    }

    this.loading = true;
    this.error = '';

    const request: ATSRequest = {
      resume_text: this.resumeText,
      job_description: this.jobDescription
    };

    this.atsService.analyzeResume(request).subscribe({
      next: (response) => {
        this.result = response;
        this.loading = false;
      },
      error: (err) => {
        this.error = err.message || 'Analysis failed. Please try again.';
        this.loading = false;
      }
    });
  }

  getScoreColor(score: number): string {
    if (score >= 80) return '#22c55e';
    if (score >= 60) return '#f59e0b';
    return '#ef4444';
  }

  getScoreLabel(score: number): string {
    if (score >= 80) return 'Excellent - Ready to Apply!';
    if (score >= 60) return 'Good - Minor Improvements Needed';
    if (score >= 40) return 'Fair - Needs Optimization';
    return 'Poor - Significant Changes Required';
  }

  getSections(sections: { [key: string]: boolean }): Array<{ key: string, value: boolean }> {
    return Object.entries(sections).map(([key, value]) => ({ key, value }));
  }
}