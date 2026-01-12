export interface ImageGenerationRequest {
  prompt: string;
  style: 'realistic' | 'anime' | 'sketch' | '3d' | 'watercolor';
  width?: number;
  height?: number;
  num_inference_steps?: number;
  guidance_scale?: number;
}

export interface ImageGenerationResponse {
  metadata?: {
    id: string;
    original_prompt: string;
    enhanced_prompt: string;
    style: string;
    width: number;
    height: number;
    created_at: string;
    api_provider: string;
    generation_status: string;
  };
  image_url: string;
  image_filename?: string;
  image_path?: string;
  enhanced_prompt: string;
  message: string;
  prompt?: string; // Fallback for backward compatibility
  generation_time?: number; // Fallback for backward compatibility
  style?: string; // Fallback for backward compatibility
  image_id?: string; // Fallback for backward compatibility
}

export interface ImageStyle {
  value: string;
  label: string;
  icon: string;
  description: string;
}