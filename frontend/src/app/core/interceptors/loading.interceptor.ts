import { Injectable } from '@angular/core';
import { 
  HttpInterceptor, 
  HttpRequest, 
  HttpHandler, 
  HttpEvent 
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { finalize } from 'rxjs/operators';

/**
 * Loading Interceptor
 * Tracks HTTP requests to show/hide global loading indicator
 */
@Injectable()
export class LoadingInterceptor implements HttpInterceptor {
  private activeRequests = 0;

  intercept(
    request: HttpRequest<any>, 
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    
    // Increment active requests
    if (this.activeRequests === 0) {
      // Show global loading indicator
      // You can emit to a LoadingService here
    }
    this.activeRequests++;

    return next.handle(request).pipe(
      finalize(() => {
        // Decrement active requests
        this.activeRequests--;
        if (this.activeRequests === 0) {
          // Hide global loading indicator
        }
      })
    );
  }
}
