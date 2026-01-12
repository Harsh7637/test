import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, timeout } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;
  private defaultTimeout = 120000; // 2 minutes for AI operations

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json'
    });
  }

  get<T>(endpoint: string, timeoutMs?: number): Observable<T> {
    return this.http.get<T>(`${this.apiUrl}${endpoint}`, {
      headers: this.getHeaders()
    }).pipe(
      timeout(timeoutMs || this.defaultTimeout),
      catchError(this.handleError)
    );
  }

  post<T>(endpoint: string, data: any, timeoutMs?: number): Observable<T> {
    return this.http.post<T>(`${this.apiUrl}${endpoint}`, data, {
      headers: this.getHeaders()
    }).pipe(
      timeout(timeoutMs || this.defaultTimeout),
      catchError(this.handleError)
    );
  }

  put<T>(endpoint: string, data: any): Observable<T> {
    return this.http.put<T>(`${this.apiUrl}${endpoint}`, data, {
      headers: this.getHeaders()
    }).pipe(
      timeout(this.defaultTimeout),
      catchError(this.handleError)
    );
  }

  delete<T>(endpoint: string): Observable<T> {
    return this.http.delete<T>(`${this.apiUrl}${endpoint}`, {
      headers: this.getHeaders()
    }).pipe(
      timeout(this.defaultTimeout),
      catchError(this.handleError)
    );
  }

  private handleError(error: any) {
    let errorMessage = 'An error occurred';
    
    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side error
      errorMessage = error.error?.detail || error.message || 'Server error';
    }
    
    console.error('API Error:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}