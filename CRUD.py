from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, Vehicle, Staff
from django.views import View
from django.http import HttpResponse

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
