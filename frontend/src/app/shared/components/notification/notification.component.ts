import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NotificationService, Notification } from '../../../core/services/notification.service';

@Component({
  selector: 'app-notification',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './notification.component.html',
  styleUrls: ['./notification.component.css']
})
export class NotificationComponent implements OnInit {
  notifications: Notification[] = [];

  constructor(private notificationService: NotificationService) {}

  ngOnInit() {
    this.notificationService.getNotifications().subscribe(
      notifications => this.notifications = notifications
    );
  }

  remove(id: string) {
    this.notificationService.remove(id);
  }

  getIcon(type: string): string {
    const icons: any = {
      success: '✅',
      error: '❌',
      warning: '⚠️',
      info: 'ℹ️'
    };
    return icons[type] || 'ℹ️';
  }

  getColorClasses(type: string): string {
    const colors: any = {
      success: 'bg-green-50 border-green-200 text-green-800',
      error: 'bg-red-50 border-red-200 text-red-800',
      warning: 'bg-orange-50 border-orange-200 text-orange-800',
      info: 'bg-blue-50 border-blue-200 text-blue-800'
    };
    return colors[type] || colors.info;
  }
}