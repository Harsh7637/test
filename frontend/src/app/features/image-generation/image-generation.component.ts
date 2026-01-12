import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ImageService } from '../../core/services/image.service';
import { ImageGenerationRequest, ImageGenerationResponse } from '../../shared/models/image.model';

@Component({
  selector: 'app-image-generation',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './image-generation.component.html',
  styleUrls: ['./image-generation.component.css']
})
export class ImageGenerationComponent {
  prompt = '';
  selectedStyle = 'realistic';
  loading = false;
  error = '';
  generatedImage: ImageGenerationResponse | null = null;
  history: ImageGenerationResponse[] = [];

  styles = [
    { value: 'realistic', label: 'Realistic', icon: '📸', desc: 'Photorealistic images' },
    { value: 'anime', label: 'Anime', icon: '🎌', desc: 'Anime & manga style' },
    { value: 'sketch', label: 'Sketch', icon: '✏️', desc: 'Pencil drawings' },
    { value: '3d', label: '3D Render', icon: '🎲', desc: '3D rendered art' },
    { value: 'watercolor', label: 'Watercolor', icon: '🎨', desc: 'Watercolor paintings' }
  ];

  constructor(private imageService: ImageService) {}

  generateImage() {
    if (!this.prompt.trim()) {
      this.error = 'Please enter a prompt';
      return;
    }

    this.loading = true;
    this.error = '';

    const request: ImageGenerationRequest = {
      prompt: this.prompt,
      style: this.selectedStyle as any,
      width: 1024,
      height: 1024
    };

    this.imageService.generateImage(request).subscribe({
      next: (response) => {
        this.generatedImage = response;
        // Preserve original prompt for history
        this.generatedImage.prompt = this.prompt;
        this.generatedImage.style = this.selectedStyle;
        this.history.unshift(response);
        if (this.history.length > 12) this.history.pop();
        this.loading = false;
      },
      error: (err) => {
        this.error = err.message || 'Generation failed. Please try again.';
        this.loading = false;
      }
    });
  }

  getImageUrl(path: string): string {
    return this.imageService.getImageUrl(path);
  }

  downloadImage() {
    if (this.generatedImage) {
      const link = document.createElement('a');
      link.href = this.getImageUrl(this.generatedImage.image_url);
      link.download = `ai-generated-${Date.now()}.png`;
      link.click();
    }
  }

  loadFromHistory(item: ImageGenerationResponse) {
    this.prompt = item.prompt || item.metadata?.original_prompt || '';
    this.selectedStyle = item.style || item.metadata?.style || 'realistic';
    this.generatedImage = item;
  }

  onImageLoadError(event: any) {
    console.error('Image failed to load:', event);
    this.error = 'Image failed to load. This may be a CORS or network issue.';
  }
}