from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from .models import Room, Reservation
from .forms import ReservationForm

def home(request):
    my_res = Reservation.objects.filter(user=request.user)[:5] if request.user.is_authenticated and not request.user.is_staff else []
    return render(request, 'home.html', {'my_res': my_res})

def rooms(request):
    q = request.GET.get('q', '').strip()
    qs = Room.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(location__icontains=q))
    return render(request, 'room_list.html', {'rooms': qs, 'q': q})

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    res = Reservation.objects.filter(room=room).order_by('-start_at')[:10]
    return render(request, 'room_detail.html', {'room': room, 'reservations': res})

@login_required
def reserve_new(request):
    if request.user.is_staff:
        return redirect('admin_requests')
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            overlaps = Reservation.objects.filter(room=obj.room, status__in=['pending', 'approved']).filter(start_at__lt=obj.end_at, end_at__gt=obj.start_at).exists()
            if overlaps:
                return render(request, 'reserve_form.html', {'form': form, 'error': 'ช่วงเวลานี้ถูกจองแล้ว'})
            obj.save()
            return redirect('my_bookings')
    else:
        form = ReservationForm()
    return render(request, 'reserve_form.html', {'form': form})

@login_required
def my_bookings(request):
    if request.user.is_staff:
        return redirect('admin_requests')
    qs = Reservation.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'items': qs})

@login_required
def cancel_booking(request, pk):
    obj = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        obj.status = 'rejected'
        obj.save()
        return redirect('my_bookings')
    return render(request, 'confirm_cancel.html', {'item': obj})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = False
            user.is_superuser = False
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@staff_member_required
def admin_requests(request):
    qs = Reservation.objects.filter(status__in=['pending']).select_related('room', 'user').order_by('start_at')
    if request.method == 'POST':
        pk = request.POST.get('pk')
        action = request.POST.get('action')
        obj = get_object_or_404(Reservation, pk=pk)
        obj.status = 'approved' if action == 'approve' else 'rejected'
        obj.save()
        return redirect('admin_requests')
    return render(request, 'admin_requests.html', {'items': qs})
