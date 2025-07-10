from django.urls import path
from home import views
from . import views
from .views import chatbot_view
from django.urls import path
from . import views





urlpatterns = [
    path('', views.index, name='home'),
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('Disease_Prediction/', views.Disease_Prediction, name='Disease_Prediction'),
    path('Report/', views.Report, name='Report'),
    path('Blogs/', views.Blogs, name='Blogs'),
    path('Blogs1/', views.Blogs1, name='Blogs1'),
    path('User_Data/', views.User_Data, name='User_Data'),
    path('User_Data/export_pdf/', views.user_data_pdf, name='export_user_data_pdf'),
    path('Login/', views.Login, name='Login'),
    path('SignUp/', views.SignUp, name='SignUp'),
    path('Profile_Management/', views.Profile_Management, name='Profile_Management'),
    path('Recommendations_Dashboard/', views.Recommendations_Dashboard, name='Recommendations_Dashboard'),
    path('Login/', views.Login, name='Login'),
    path('SignUp/', views.SignUp, name='SignUp'),
    path('Logout/', views.Logout, name='Logout'),
    path("pdf_report/", views.pdf_report, name="pdf_report"),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('autocomplete/', views.autocomplete_symptoms, name='autocomplete_symptoms'),
    #  path('User_Data/', views.User_Data, name='user_data'),



]







