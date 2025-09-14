from django.contrib import admin
from .models import Room, Reservation
from datetime import timedelta

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'location', 'max_hours', 'total_hours')
    readonly_fields = ('total_hours',)
    def total_hours(self, obj):
        reservations = Reservation.objects.filter(room=obj, status__in=['pending', 'approved'])
        total = timedelta()
        for r in reservations:
            total += (r.end_at - r.start_at)
        hours = total.total_seconds() / 3600
        return f"{hours:.1f} ชั่วโมง"

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'start_at', 'end_at', 'status')
    list_filter = ('status', 'room')
    search_fields = ('room__name', 'user__username')

admin.site.register(Room, RoomAdmin)
admin.site.register(Reservation, ReservationAdmin)
