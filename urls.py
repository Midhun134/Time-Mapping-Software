from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.home, name='home'),
    
    # Job management
    path('job/register/', views.job_registration, name='job_registration'),
    path('job/search/', views.job_search, name='job_search'),
    path('job/<str:job_id>/', views.job_details, name='job_details'),
    
    # QR Code
    path('generate-qr/', views.generate_qr, name='generate_qr'),
    path('scan-qr/', views.scan_qr, name='scan_qr'),

    # path('jobs/create/', CreateJobView.as_view(), name='create_job'),
    # path('jobs/', ListJobView.as_view(), name='list_jobs'),
    # path('jobs/update/<int:job_id>/', UpdateJobView.as_view(), name='update_job'),
    # path('jobs/delete/<int:job_id>/', DeleteJobView.as_view(), name='delete_job'),
    
    # Staff management (for admin)
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/add/', views.add_staff, name='add_staff'),
    path('staff/<int:staff_id>/edit/', views.edit_staff, name='edit_staff'),
    path('staff/<int:staff_id>/delete/', views.delete_staff, name='delete_staff'),
    
    # API endpoints for mobile app
    path('api/', include([
        path('login/', views.api_login, name='api_login'),
        path('job/entry/', views.api_job_entry, name='api_job_entry'),
        path('job/exit/', views.api_job_exit, name='api_job_exit'),
        path('job/details/<str:job_id>/', views.api_job_details, name='api_job_details'),
        path('update_job_status/', views.update_job_status, name='update_job_status'),
    ])),
    
    # Reports
    path('reports/efficiency/', views.efficiency_report, name='efficiency_report'),
    path('reports/time-lag/', views.time_lag_report, name='time_lag_report'),
]

# This urls.py file defines the URL patterns for the Django backend of the time mapping application. 

# Admin interface
# Authentication (login/logout)
# Dashboard (home page)
# Job management (registration, search, details)
# QR code generation and scanning
# Staff management (for admin users)
# API endpoints for the mobile app
# Reports for efficiency and time lag analysis