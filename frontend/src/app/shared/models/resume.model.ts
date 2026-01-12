export interface Education {
  degree: string;
  institution: string;
  year: string;
  gpa?: string;
}

export interface Experience {
  title: string;
  company: string;
  duration: string;
  responsibilities: string[];
}

export interface ResumeRequest {
  name: string;
  email: string;
  phone: string;
  target_role: string;
  summary?: string;
  skills: string[];
  experience: Experience[];
  education: Education[];
  job_description: string;
}

export interface ResumeResponse {
  pdf_url: string;
  optimized_resume: any;
  suggestions: string[];
  resume_id: string;
}