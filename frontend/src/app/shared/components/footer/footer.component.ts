import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.css']
})
export class FooterComponent {
  currentYear = new Date().getFullYear();
  
  links = {
    features: [
      { name: 'Image Generation', path: '/image-generation' },
      { name: 'Resume Builder', path: '/resume-generator' },
      { name: 'ATS Analyzer', path: '/ats-analyzer' }
    ],
    company: [
      { name: 'About', path: '/' },
      { name: 'Blog', path: '/' },
      { name: 'Contact', path: '/' }
    ]
  };
}