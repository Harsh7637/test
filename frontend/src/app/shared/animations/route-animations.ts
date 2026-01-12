import { trigger, transition, style, animate, query, group } from '@angular/animations';

export const routeAnimations = trigger('routeAnimations', [
  transition('* <=> *', [
    query(':enter, :leave', [
      style({
        position: 'absolute',
        width: '100%',
        opacity: 0
      })
    ], { optional: true }),
    query(':enter', [
      animate('300ms ease-in', style({ opacity: 1 }))
    ], { optional: true })
  ])
]);

export const fadeInAnimation = trigger('fadeIn', [
  transition(':enter', [
    style({ opacity: 0, transform: 'translateY(10px)' }),
    animate('400ms ease-out', style({ opacity: 1, transform: 'translateY(0)' }))
  ])
]);

export const slideInAnimation = trigger('slideIn', [
  transition(':enter', [
    style({ transform: 'translateX(-100%)', opacity: 0 }),
    animate('400ms ease-out', style({ transform: 'translateX(0)', opacity: 1 }))
  ])
]);