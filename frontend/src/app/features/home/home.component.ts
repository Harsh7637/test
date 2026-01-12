import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

interface FeatureCard {
  icon: string;
  title: string;
  description: string;
  tag: string;
  color: string;
}

interface Feature {
  icon: string;
  title: string;
  description: string;
  link: string;
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  floatingCards: FeatureCard[] = [
    {
      icon: '🎨',
      title: 'AI Image Gen',
      description: 'Create stunning visuals from text prompts using Stable Diffusion XL',
      tag: 'Creative',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: '📄',
      title: 'Resume Builder',
      description: 'Generate ATS-optimized resumes tailored to your dream job',
      tag: 'Professional',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: '🎯',
      title: 'ATS Analyzer',
      description: 'Optimize your resume with AI-powered scoring and insights',
      tag: 'Smart',
      color: 'from-green-500 to-emerald-500'
    }
  ];

  features: Feature[] = [
    {
      icon: '🖼️',
      title: 'AI Image Generation',
      description: 'Transform your ideas into beautiful images with multiple artistic styles using Stable Diffusion XL',
      link: '/image-generation'
    },
    {
      icon: '📝',
      title: 'Resume Generator',
      description: 'Build professional, ATS-optimized resumes with AI-powered content optimization and PDF export',
      link: '/resume-generator'
    },
    {
      icon: '📊',
      title: 'ATS Analyzer',
      description: 'Get detailed feedback, keyword analysis, and improvement suggestions to boost your resume score',
      link: '/ats-analyzer'
    }
  ];

  stats = [
    { value: '100%', label: 'Self-Hosted AI' },
    { value: '< 30s', label: 'Generation Time' },
    { value: '95+', label: 'ATS Score Possible' }
  ];

  ngOnInit() {
    // Any initialization logic
  }
}