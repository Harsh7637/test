import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private notifications$ = new BehaviorSubject<Notification[]>([]);

  getNotifications(): Observable<Notification[]> {
    return this.notifications$.asObservable();
  }

  show(type: Notification['type'], message: string, duration: number = 5000) {
    const notification: Notification = {
      id: this.generateId(),
      type,
      message,
      duration
    };

    const current = this.notifications$.value;
    this.notifications$.next([...current, notification]);

    if (duration > 0) {
      setTimeout(() => {
        this.remove(notification.id);
      }, duration);
    }
  }

  success(message: string) {
    this.show('success', message);
  }

  error(message: string) {
    this.show('error', message, 7000);
  }

  warning(message: string) {
    this.show('warning', message);
  }

  info(message: string) {
    this.show('info', message);
  }

  remove(id: string) {
    const current = this.notifications$.value;
    this.notifications$.next(current.filter(n => n.id !== id));
  }

  private generateId(): string {
    return `notif_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}