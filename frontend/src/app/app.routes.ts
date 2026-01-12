import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./features/home/home.component').then(m => m.HomeComponent),
    title: 'AI Platform - Home'
  },
  {
    path: 'image-generation',
    loadComponent: () => import('./features/image-generation/image-generation.component').then(m => m.ImageGenerationComponent),
    title: 'AI Image Generation'
  },
  {
    path: 'resume-generator',
    loadComponent: () => import('./features/resume-generator/resume-generator.component').then(m => m.ResumeGeneratorComponent),
    title: 'Resume Generator'
  },
  {
    path: 'ats-analyzer',
    loadComponent: () => import('./features/ats-analyzer/ats-analyzer.component').then(m => m.AtsAnalyzerComponent),
    title: 'ATS Resume Analyzer'
  },
  {
    path: '**',
    redirectTo: ''
  }
];