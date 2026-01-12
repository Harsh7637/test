export interface ATSRequest {
  resume_text: string;
  job_description: string;
}

export interface ATSResponse {
  score: number;
  matched_keywords: string[];
  missing_keywords: string[];
  suggestions: string[];
  section_analysis: { [key: string]: boolean };
  formatting_score: number;
  keyword_score: number;
  semantic_score: number;
}