from django.db import models
from django.contrib.auth.models import User

class SignupUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    email = models.EmailField()
    full_name = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    address = models.TextField(blank=True, null=True)



    def __str__(self):
        return self.username

class UserPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    symptoms = models.TextField()
    diagnosis = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    precautions = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    diet = models.TextField(blank=True)
    workout = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.diagnosis} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

