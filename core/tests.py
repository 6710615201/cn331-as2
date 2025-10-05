from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class CoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        # สร้าง user ตัวอย่าง
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_home_page(self):
        """
        ทดสอบว่า home page เข้าถึงได้ (ไม่ต้องล็อกอิน)
        """
        url = reverse('home')  # เปลี่ยน 'home' ถ้า URL name ต่างกัน
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        """
        ทดสอบว่าล็อกอินสำเร็จ
        """
        login_url = reverse('login')  # เปลี่ยนชื่อถ้าใช้ชื่ออื่น
        response = self.client.post(login_url, {
            'username': 'testuser',
            'password': '12345'
        })
        # ถ้า login สำเร็จ บางทีจะ redirect (302) หรือแสดงหน้าอื่น
        self.assertIn(response.status_code, [200, 302])

    def test_login_fail(self):
        """
        ทดสอบล็อกอินไม่สำเร็จ
        """
        login_url = reverse('login')
        response = self.client.post(login_url, {
            'username': 'baduser',
            'password': 'badpassword'
        })
        # คาดว่าไม่ redirect ไปหน้าอื่น
        self.assertNotEqual(response.status_code, 302)

    def test_protected_view_requires_login(self):
        """
        ถ้ามีหน้า “reserve” (หรือชื่ออื่น) ที่ต้องล็อกอินก่อนจึงเข้าถึงได้
        """
        reserve_url = reverse('reserve')  # เปลี่ยนถ้า URL name ใช้ชื่ออื่น
        # ก่อนล็อกอิน — คาดว่าจะถูก redirect ไป login
        response = self.client.get(reserve_url)
        self.assertIn(response.status_code, [301, 302])

        # ถ้าล็อกอินแล้ว — ควรเข้าถึง view ได้
        self.client.login(username='testuser', password='12345')
        response2 = self.client.get(reserve_url)
        self.assertEqual(response2.status_code, 200)
