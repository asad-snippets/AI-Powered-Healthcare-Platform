from django.contrib import admin
from .models import SignupUser, UserPrediction
class SignupUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'dob','gender', 'phone', 'address')
    search_fields = ('username', 'email', 'full_name')
admin.site.register(SignupUser, SignupUserAdmin)

class UserPredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'diagnosis', 'created_at')
    search_fields = ('user__username', 'diagnosis')
    list_filter = ('created_at',)
admin.site.register(UserPrediction, UserPredictionAdmin)