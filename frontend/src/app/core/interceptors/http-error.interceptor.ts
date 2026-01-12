import { Injectable } from '@angular/core';
import { 
  HttpInterceptor, 
  HttpRequest, 
  HttpHandler, 
  HttpEvent, 
  HttpErrorResponse 
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { NotificationService } from '../services/notification.service';

/**
 * HTTP Error Interceptor
 * Handles HTTP errors globally and displays user-friendly messages
 */
@Injectable()
export class HttpErrorInterceptor implements HttpInterceptor {

  constructor(private notificationService: NotificationService) {}

  intercept(
    request: HttpRequest<any>, 
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    
    return next.handle(request).pipe(
      // Retry failed requests once (except for POST/PUT/DELETE)
      retry({
        count: 1,
        delay: 1000,
        resetOnSuccess: true
      }),
      
      // Catch errors
      catchError((error: HttpErrorResponse) => {
        let errorMessage = '';

        if (error.error instanceof ErrorEvent) {
          // Client-side error
          errorMessage = `Client Error: ${error.error.message}`;
        } else {
          // Server-side error
          errorMessage = this.getServerErrorMessage(error);
        }

        // Show notification to user
        this.notificationService.error(errorMessage);

        // Log to console for debugging
        console.error('HTTP Error:', {
          status: error.status,
          message: errorMessage,
          url: request.url,
          error: error
        });

        return throwError(() => new Error(errorMessage));
      })
    );
  }

  private getServerErrorMessage(error: HttpErrorResponse): string {
    switch (error.status) {
      case 0:
        return 'Cannot connect to server. Please check your internet connection.';
      case 400:
        return error.error?.detail || 'Invalid request. Please check your input.';
      case 401:
        return 'Unauthorized. Please log in.';
      case 403:
        return 'Access forbidden.';
      case 404:
        return 'Resource not found.';
      case 408:
        return 'Request timeout. Please try again.';
      case 500:
        return error.error?.detail || 'Server error. Please try again later.';
      case 503:
        return 'Service temporarily unavailable.';
      default:
        return error.error?.detail || `Server error: ${error.status}`;
    }
  }
}

