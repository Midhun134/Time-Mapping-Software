from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Job, Staff, Vehicle
from .forms import JobRegistrationForm, StaffForm
import qrcode
from io import BytesIO
import base64
from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, Vehicle, Staff
from django.views import View
from django.http import HttpResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


# Create a new job
class CreateJobView(View):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        return render(request, 'create_job.html', {'vehicles': vehicles})

    def post(self, request):
        vehicle_id = request.POST.get('vehicle')
        job_description = request.POST.get('job_description')
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        
        job = Job(vehicle=vehicle, job_description=job_description, job_status='Pending')
        job.save()
        return HttpResponse('Job created successfully!')



# View a list of jobs
class ListJobView(View):
    def get(self, request):
        jobs = Job.objects.all()
        return render(request, 'list_jobs.html', {'jobs': jobs})

# Update a job
class UpdateJobView(View):
    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        return render(request, 'update_job.html', {'job': job})

    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        job.job_status = request.POST.get('job_status')
        job.save()
        return HttpResponse('Job updated successfully!')

# Delete a job
class DeleteJobView(View):
    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        job.delete()
        return HttpResponse('Job deleted successfully!')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def job_registration(request):
    if request.method == 'POST':
        form = JobRegistrationForm(request.POST)
        if form.is_valid():
            job = form.save()
            return redirect('job_details', job_id=job.id)
    else:
        form = JobRegistrationForm()
    return render(request, 'job_registration.html', {'form': form})

@login_required
def job_search(request):
    if request.method == 'POST':
        vehicle_number = request.POST.get('vehicle_number')
        job_description = request.POST.get('job_description', 'General Service')

        try:
            vehicle = Vehicle.objects.get(vehicle_number=vehicle_number)
            job = Job.objects.create(
                vehicle=vehicle,
                job_description=job_description,
                start_time=timezone.now(),
                status='In Progress'
            )
            return JsonResponse({'message': 'Job started successfully', 'job_id': job.id})
        except Vehicle.DoesNotExist:
            return JsonResponse({'error': 'Vehicle not found'}, status=404)
    return render(request, 'job_search.html', {'jobs': job})

@login_required
def job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_details.html', {'job': job})

@login_required
def generate_qr(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(job_id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_image = base64.b64encode(buffer.getvalue()).decode()
    return render(request, 'qr_code.html', {'qr_image': qr_image})

@login_required
def staff_list(request):
    staffs = Staff.objects.all()
    return render(request, 'staff_list.html', {'staffs': staffs})

@login_required
def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'staff_form.html', {'form': form})

# API views
def api_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
def api_job_entry(request):
    if request.method == 'POST':
        job_id = request.POST['job_id']
        job = get_object_or_404(Job, id=job_id)
        job.start_time = timezone.now()
        job.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
def api_job_exit(request):
    if request.method == 'POST':
        job_id = request.POST['job_id']
        job = get_object_or_404(Job, id=job_id)
        job.end_time = timezone.now()
        job.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


# QR Code Scan Job Entry
def start_job(request, vehicle_number):
    vehicle = get_object_or_404(Vehicle, vehicle_number=vehicle_number)
    job = Job.objects.filter(vehicle=vehicle, job_status='Pending').first()
    
    if job:
        job.start_time = now()
        job.job_status = 'In Progress'
        job.save()
        return render(request, 'job_started.html', {'job': job})
    return render(request, 'error.html', {'message': 'Job not found or already started'})

# QR Code Scan Job Exit
@login_required
def end_job(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        try:
            job = Job.objects.get(id=job_id, status='In Progress')
            job.end_time = timezone.now()
            job.status = 'Completed'
            job.save()
            return JsonResponse({'message': 'Job completed successfully', 'job_id': job.id})
        except Job.DoesNotExist:
            return JsonResponse({'error': 'Job not found or already completed'}, status=404)
    return render(request, 'error.html', {'message': 'Job not found or not started'}, status=404)

@login_required
def update_job_status(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        new_status = request.POST.get('status')
        try:
            job = Job.objects.get(id=job_id)
            job.status = new_status
            job.save()
            return JsonResponse({'message': 'Job status updated successfully', 'job_id': job.id, 'status': new_status})
        except Job.DoesNotExist:
            return JsonResponse({'error': 'Job not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

# View to generate job report
def job_report(request):
    jobs = Job.objects.all()
    
    # Calculate total efficiency and idle time for each job
    report_data = []
    for job in jobs:
        idle_time = job.idle_time
        efficiency = job.worker_efficiency
        report_data.append({
            'vehicle_number': job.vehicle.vehicle_number,
            'job_description': job.job_description,
            'idle_time': idle_time,
            'worker_efficiency': efficiency,
            'job_status': job.job_status,
        })

    return render(request, 'job_report.html', {'report_data': report_data})

@csrf_exempt
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

        # Create Vehicle entry in the database
        vehicle, created = Vehicle.objects.get_or_create(vehicle_number=data)
        vehicle.qr_code_image = file_name
        vehicle.save()

        return JsonResponse({'message': 'QR Code generated successfully', 'file_path': file_name})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_profile = UserProfile.objects.get(user=user)
            role = 'Manager' if user_profile.is_manager else 'Worker'
            return JsonResponse({'message': 'Login successful', 'role': role})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'Invalid request method'}, status=400)