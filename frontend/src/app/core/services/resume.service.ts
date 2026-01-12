import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { ResumeRequest, ResumeResponse } from '../../shared/models/resume.model';

@Injectable({
  providedIn: 'root'
})
export class ResumeService {
  constructor(private api: ApiService) {}

  generateResume(request: ResumeRequest): Observable<ResumeResponse> {
    return this.api.post<ResumeResponse>('/resume/generate', request);
  }

  getResumeUrl(pdfPath: string): string {
    return `http://localhost:8000${pdfPath}`;
  }
}