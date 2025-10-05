from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from booking.models import Room, Reservation
from datetime import datetime, timedelta

class BookingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='12345')
        self.room = Room.objects.create(name='Room A', capacity=5, location='Floor 2')

    def test_home_page_accessible(self):
        """ GOOD PATH: หน้าหลักเข้าได้"""
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        """ GOOD PATH: ล็อกอินสำเร็จ"""
        login_url = reverse('login')
        response = self.client.post(login_url, {
            'username': 'tester',
            'password': '12345'
        })
        self.assertIn(response.status_code, [200, 302])

    def test_login_fail(self):
        """ BAD PATH: ล็อกอินผิด"""
        login_url = reverse('login')
        response = self.client.post(login_url, {
            'username': 'wrong',
            'password': 'nope'
        })
        self.assertEqual(response.status_code, 200)

    def test_reservation_good_path(self):
        """ GOOD PATH: จองห้องสำเร็จ"""
        self.client.login(username='tester', password='12345')
        url = reverse('reserve_new')  # แก้ตรงนี้ให้ตรงกับ urls.py ของหนู
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        data = {
            'room': self.room.id,
            'start_at': start_time.strftime('%Y-%m-%dT%H:%M'),
            'end_at': end_time.strftime('%Y-%m-%dT%H:%M'),
            'note': 'Meeting test'
        }
        response = self.client.post(url, data)
        
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(
            Reservation.objects.filter(room=self.room, user=self.user).exists()
        )

    def test_reservation_bad_path_duplicate(self):
        """ BAD PATH: จองซ้ำเวลาเดิม"""
        self.client.login(username='tester', password='12345')
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        Reservation.objects.create(
            room=self.room,
            user=self.user,
            start_at=start_time,
            end_at=end_time
        )
        url = reverse('reserve_new')
        data = {
            'room': self.room.id,
            'start_at': start_time.strftime('%Y-%m-%dT%H:%M'),
            'end_at': end_time.strftime('%Y-%m-%dT%H:%M'),
            'note': 'Duplicate test'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, 'ช่วงเวลานี้ถูกจองแล้ว')
    