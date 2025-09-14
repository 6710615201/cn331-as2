from django.contrib import admin
from django.urls import path, include
from booking.views import home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('booking.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
