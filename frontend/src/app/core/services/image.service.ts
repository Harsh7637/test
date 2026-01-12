import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { ImageGenerationRequest, ImageGenerationResponse } from '../../shared/models/image.model';

@Injectable({
  providedIn: 'root'
})
export class ImageService {
  constructor(private api: ApiService) {}

  generateImage(request: ImageGenerationRequest): Observable<ImageGenerationResponse> {
    return this.api.post<ImageGenerationResponse>('/image/generate', request, 300000); // 5 min timeout
  }

  getImageUrl(imageSource: string): string {
    // If it's a full URL (starts with http), use it directly
    if (imageSource && (imageSource.startsWith('http://') || imageSource.startsWith('https://'))) {
      return imageSource;
    }
    // Otherwise, treat it as a local path
    return `http://localhost:8000/images/${imageSource}`;
  }
}