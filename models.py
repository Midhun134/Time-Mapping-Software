# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('Manager', 'Manager'), ('Worker', 'Worker')])

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=50, unique=True)
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vehicle_number



# Job Model
class Job(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    job_description = models.TextField()
    job_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    idle_time = models.DurationField(default=timedelta)  # Time spent in idle
    worker_efficiency = models.FloatField(default=0.0)  # Efficiency in percentage

    def calculate_idle_time(self):
        """Calculate the idle time between start and end."""
        if self.end_time and self.start_time:
            total_time = self.end_time - self.start_time
            return total_time - self.get_active_work_time()
        return timedelta(0)

    def get_active_work_time(self):
        """Simulate getting active work time (you can add specific job timings here)."""
        # Placeholder for actual work time tracking
        # Assuming the job work took 70% of the total time, the rest is idle.
        return (self.end_time - self.start_time) * 0.7

    def calculate_worker_efficiency(self):
        """Calculate the efficiency of the worker based on time."""
        if self.start_time and self.end_time:
            total_time = (self.end_time - self.start_time).total_seconds()
            active_work_time = self.get_active_work_time().total_seconds()
            if total_time > 0:
                self.worker_efficiency = (active_work_time / total_time) * 100
            return self.worker_efficiency
        return 0.0

    def save(self, *args, **kwargs):
        """Override the save method to calculate idle time and efficiency."""
        if self.start_time and self.end_time:
            self.idle_time = self.calculate_idle_time()
            self.worker_efficiency = self.calculate_worker_efficiency()
        super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return f"Job for {self.vehicle.vehicle_number} - {self.job_status}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Manager' if self.is_manager else 'Worker'}"