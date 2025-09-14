
from django.urls import path
from . import views
urlpatterns = [
    path('rooms/', views.rooms, name='rooms'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('reserve/new/', views.reserve_new, name='reserve_new'),
    path('my/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),
    path('signup/', views.signup, name='signup'),
    path('manage/', views.admin_requests, name='admin_requests'),
]
