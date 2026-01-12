import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ResumeResponse } from '../../../../shared/models/resume.model';
import { LoaderComponent } from '../../../../shared/components/loader/loader.component';

@Component({
  selector: 'app-resume-preview',
  standalone: true,
  imports: [CommonModule, LoaderComponent],
  templateUrl: './resume-preview.component.html',
  styleUrls: ['./resume-preview.component.css']
})
export class ResumePreviewComponent {
  @Input() result: ResumeResponse | null = null;
  @Input() loading: boolean = false;
  @Input() error: string = '';
  @Output() downloadResume = new EventEmitter<void>();

  onDownload() {
    this.downloadResume.emit();
  }
}

