import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { ATSRequest, ATSResponse } from '../../shared/models/ats.model';

@Injectable({
  providedIn: 'root'
})
export class AtsService {
  constructor(private api: ApiService) {}

  analyzeResume(request: ATSRequest): Observable<ATSResponse> {
    return this.api.post<ATSResponse>('/ats/analyze', request);
  }
}