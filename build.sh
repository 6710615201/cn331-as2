#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

# สร้าง admin + users + rooms แบบ idempotent (รันซ้ำได้ ไม่ซ้ำซ้อน)
python manage.py shell <<'PY'
from django.contrib.auth import get_user_model
U = get_user_model()
if not U.objects.filter(username='admin').exists():
    U.objects.create_superuser('admin','admin@example.com','admin1234')
for name in ['user1','user2','user3']:
    if not U.objects.filter(username=name).exists():
        U.objects.create_user(name, password='user1234')
from booking.models import Room
for r in ['A101','B202','C303']:
    Room.objects.get_or_create(name=r)
print("✅ ensured admin/user1-3/rooms exist")
PY
