from django.http import JsonResponse
from django.shortcuts import render
import qrcode
import io
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def generate_qr_code(request):
    if request.method == 'POST':
        data = request.POST.get('data', 'Default Data')
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        file_name = f"qr_codes/{data}.png"
        file = ContentFile(buf.getvalue())
        default_storage.save(file_name, file)

        return JsonResponse({'message': 'QR Code generated successfully', 'file_path': file_name})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('generate_qr/', views.generate_qr_code, name='generate_qr'),
]

# settings.py
# Add the following settings to handle media files
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# models.py (optional if storing QR Code data in the database)
from django.db import models

class QRCode(models.Model):
    data = models.CharField(max_length=255)
    image = models.ImageField(upload_to='qr_codes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.data

# templates/generate_qr.html (optional, for a simple form to generate QR codes)
# <form method="post" action="/generate_qr/">
#     {% csrf_token %}
#     <label for="data">Enter Data for QR Code:</label>
#     <input type="text" id="data" name="data" required>
#     <button type="submit">Generate QR Code</button>
# </form>

# To run the server
# 1. Add the app to INSTALLED_APPS in settings.py
# 2. Run migrations: python manage.py makemigrations and python manage.py migrate
# 3. Start the server: python manage.py runserver

# Django dependencies
# Make sure to install Django and Pillow for image handling:
# pip install django pillow