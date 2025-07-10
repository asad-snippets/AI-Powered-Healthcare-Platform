from django.shortcuts import render,redirect
import pickle
import time
import json
import os
import numpy as np
import pandas as pd
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.contrib import messages  # For user-friendly alerts
from django.views.decorators.cache import never_cache
# from .models import profilepic
from .noCache import no_cache
from django.template.loader import render_to_string
import tempfile
import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import JsonResponse
from home.models import SignupUser,UserPrediction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from io import BytesIO
from django.utils import timezone
from django.contrib.auth import authenticate, update_session_auth_hash
from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
from django.views.decorators.csrf import csrf_exempt

from dotenv import load_dotenv
load_dotenv()
import random
from django.utils import timezone
from datetime import date
from .models import SignupUser, UserPrediction


#load the datasets
sym_des = pd.read_csv("implementation/symtoms_df.csv")
precautions = pd.read_csv("implementation/updated_precautions.csv")
workout = pd.read_csv("implementation/updated_workouts.csv")
description = pd.read_csv("implementation/updated_description.csv")
medication = pd.read_csv("implementation/medications_clean.csv")
diets = pd.read_csv("implementation/updated_diets.csv")

#load model read bind
svc = pickle.load(open("Implementation/svc.pkl","rb"))

# Helping function
def helper(dis):
    # Description (as a string)
    desc_row = description[description['Disease'] == dis]['Description']
    desc = desc_row.iloc[0] if not desc_row.empty else ""

    # Precautions (correctly handled as a list of strings)
    pre_row = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = pre_row.iloc[0].tolist() if not pre_row.empty else []



    # Medications (as a list)
    med_row = medication[medication['Disease'] == dis]['Medication']
    med = [med_row.iloc[0]] if not med_row.empty else []

    # Diet (as a list)
    die_row = diets[diets['Disease'] == dis]['Diet']
    die = [die_row.iloc[0]] if not die_row.empty else []

    # Workout (as a list, not string!)
    wrkout_row = workout[workout['Disease'] == dis]['Workout']
    wrkout = [wrkout_row.iloc[0]] if not wrkout_row.empty else []

    return desc, pre, med, die, wrkout


symptoms_dict={'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list={15: 'Fungal infection',4: 'Allergy',16:  'GERD',9:  'Chronic cholestasis',14: 'Drug Reaction',33: 'Peptic ulcer disease',1: 'AIDS',12: 'Diabetes ',17: 'Gastroenteritis',6: 'Bronchial Asthma',23:  'Hypertension ',30: 'Migraine',7: 'Cervical spondylosis',32: 'Paralysis (brain hemorrhage)',28: 'Jaundice',29: 'Malaria',8: 'Chicken pox',11: 'Dengue',37: 'Typhoid',40: 'hepatitis A',19:'Hepatitis B',20: 'Hepatitis C',21: 'Hepatitis D',22: 'Hepatitis E',3:'Alcoholic hepatitis',36: 'Tuberculosis',10: 'Common Cold',34: 'Pneumonia',13:'Dimorphic hemmorhoids(piles)',18: 'Heart attack',39: 'Varicose veins',26:'Hypothyroidism',24: 'Hyperthyroidism',25:  'Hypoglycemia',31: 'Osteoarthristis',5:  'Arthritis',0:'(vertigo) Paroymsal  Positional Vertigo',2: 'Acne',38:'Urinary tract infection',35: 'Psoriasis',27: 'Impetigo'}

def get_predicted_value(patient_symptoms):
    input_vector=np.zeros(len(symptoms_dict))

    for item in patient_symptoms:
        input_vector[symptoms_dict[item]]=1
    return diseases_list[svc.predict([input_vector])[0]]


#Creating the Routes
def index(request):
    return render(request, 'index.html')
@never_cache
@no_cache
@login_required
def Dashboard(request):
        # User is logged in, redirect to the dashboard
    return render(request, 'Dashboard.html')


def Disease_Prediction(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            symptoms = request.POST.get('symptoms', '').strip()

            if not symptoms:
                return render(request, 'Disease_Prediction.html', {'error': 'Please enter symptoms before predicting.'})

            user_symptoms = [s.strip().lower() for s in symptoms.split(',') if s.strip()]

            try:
                predicted_disease = get_predicted_value(user_symptoms)
                desc, pre, med, die, workouts = helper(predicted_disease)

                # Save full prediction with description & precautions
                prediction = UserPrediction.objects.create(
                    user=request.user,
                    symptoms=", ".join(user_symptoms),
                    diagnosis=predicted_disease,
                    description=desc,
                    precautions=", ".join(pre),
                    medications=", ".join(med),
                    diet=", ".join(die),
                    workout=", ".join(workouts),
                )

                # Adjust created_at to local time for display purposes
                prediction.created_at = timezone.localtime(prediction.created_at)
                prediction.save()

                request.session['can_view_report'] = True

                return render(request, 'Disease_Prediction.html', {
                    'pred': predicted_disease,
                    'dis_des': desc,
                    'dis_pre': pre,
                    'dis_med': med,
                    'dis_diet': die,
                    'dis_workout': workouts,
                    'result_ready': True
                })

            except KeyError as e:
                return render(request, 'Disease_Prediction.html', {
                    'error': f"Invalid symptom entered: {str(e)}. Please check and try again."
                })
            except Exception as e:
                return render(request, 'Disease_Prediction.html', {
                    'error': f"Something went wrong: {str(e)}"
                })

        # Render the disease prediction page with the symptom list
        return render(request, 'Disease_Prediction.html', {
            'symptom_list': SYMPTOM_LIST
        })
    else:
        return redirect('Login')



@login_required

def Report(request):
    # Only allow once after prediction
    if not request.session.get('can_view_report'):
        return render(request, 'Report.html', {'error': 'No recent prediction available for report.'})

    try:
        # 1. Fetch latest prediction
        latest = UserPrediction.objects.filter(user=request.user).latest('created_at')

        # 2. Fetch user profile
        profile = SignupUser.objects.get(user=request.user)

        # 3. Compute age
        age = ''
        if profile.dob:
            today = date.today()
            born = profile.dob
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        # 4. Generate Patient ID (using user PK)
        patient_id = f"PAT-{request.user.pk:04d}"

        # 5. Generate Report ID (start at 101 + total count)
        total = UserPrediction.objects.count()
        report_number = 101 + total
        report_id = f"Rep-{report_number}"

        # 6. Convert current time to local time (Pakistan Standard Time)
        local_time = timezone.localtime(timezone.now())  # Convert UTC time to local time
        timestamp = local_time.strftime('%Y-%m-%d %H:%M:%S')  # Format the local time

        # Build context
        context = {
            'full_name': profile.full_name or request.user.get_full_name() or request.user.username,
            'age': age,
            'gender': profile.get_gender_display() if profile.gender else '',
            'patient_id': patient_id,
            'report_id': report_id,
            'timestamp': timestamp,
            'pred': latest.diagnosis,
            'dis_des': latest.description,
            'dis_pre': latest.precautions.split(', ') if latest.precautions else [],
            'dis_med': latest.medications.split(', ') if latest.medications else [],
            'dis_diet': latest.diet.split(', ') if latest.diet else [],
            'dis_workout': latest.workout.split(', ') if latest.workout else [],
            'symptoms': latest.symptoms.split(', ') if latest.symptoms else [],
        }

        return render(request, 'Report.html', context)

    except UserPrediction.DoesNotExist:
        return render(request, 'Report.html', {'error': 'No prediction data available.'})
    except SignupUser.DoesNotExist:
        return render(request, 'Report.html', {'error': 'Please complete your profile first.'})




@login_required
def pdf_report(request):
    # Fetch latest prediction (same as Report view)
    try:
        latest = UserPrediction.objects.filter(user=request.user).latest('created_at')
    except UserPrediction.DoesNotExist:
        return HttpResponse("No prediction data available.", status=400)

    # Fetch user profile
    try:
        profile = SignupUser.objects.get(user=request.user)
    except SignupUser.DoesNotExist:
        return HttpResponse("Please complete your profile first.", status=400)

    # Compute age
    age = ''
    if profile.dob:
        today = date.today()
        born = profile.dob
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    # Generate Patient ID and Report ID
    patient_id = f"PAT-{request.user.pk:04d}"
    total_reports = UserPrediction.objects.count()
    report_number = 101 + total_reports
    report_id = f"Rep-{report_number}"

    # Timestamp
    local_time = timezone.localtime(timezone.now())  # Convert UTC time to local time
    timestamp = local_time.strftime('%Y-%m-%d %H:%M:%S')  # Format the local time
    # Build context for PDF
    context = {
        'full_name': profile.full_name or request.user.get_full_name() or request.user.username,
        'patient_id': patient_id,
        'age': age,
        'gender': profile.get_gender_display() if profile.gender else '',
        'report_id': report_id,
        'timestamp': timestamp,
        'symptoms': latest.symptoms.split(', '),
        'pred': latest.diagnosis,
        'dis_des': latest.description,
        'dis_pre': latest.precautions.split(', ') if latest.precautions else [],
        'dis_med': latest.medications.split(', ') if latest.medications else [],
        'dis_diet': latest.diet.split(', ') if latest.diet else [],
        'dis_workout': latest.workout.split(', ') if latest.workout else [],
    }

    # Render to HTML string
    html = render_to_string("pdf_template.html", context)

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="medical_report.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("PDF generation failed", status=500)
    return response




def Blogs(request):
    return render(request, 'Blogs.html')

def Blogs1(request):
    return render(request, 'Blogs1.html')

@login_required(login_url='Login')
def User_Data(request):
    try:
        user_profile = SignupUser.objects.get(user=request.user)
        full_name = user_profile.full_name  # Get full_name from SignupUser model
    except SignupUser.DoesNotExist:
        full_name = request.user.username  # Fallback to username if no SignupUser found

    user_reports = request.user.predictions.all().order_by('-created_at')
    
    # Convert `created_at` to local time if timezone is used
    for report in user_reports:
        if hasattr(report, 'created_at') and report.created_at:
            # Convert to local timezone before passing it to the template
            local_time = timezone.localtime(report.created_at)
            report.created_at_12hr = local_time.strftime('%d-%m-%Y %I:%M %p')  # Format it as you need
        else:
            report.created_at_12hr = ''
    
    q = request.GET.get('q', '').strip()
    if q:
        user_reports = user_reports.filter(diagnosis__icontains=q)

    return render(request, 'User_Data.html', {'user_reports': user_reports, 'query': q, 'full_name': full_name})


@login_required(login_url='Login')
def user_data_pdf(request):
    # 1. Fetch reports
    user_reports = request.user.predictions.all().order_by('-created_at')
    # 2. Render HTML template to string
    html = render_to_string('pdf_user_data.html', {'user': request.user,'user_reports': user_reports,
    })
    # 3. Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="prediction_history.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response

def Login(request):
    if request.user.is_authenticated:
        return redirect("Dashboard")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Flush any old session, then log in
            request.session.flush()
            auth_login(request, user)

            # Prevent session fixation
            request.session.cycle_key()

            # Stamp the time of this request as 'last_activity'
            request.session["last_activity"] = int(time.time())

            return redirect("Dashboard")
        else:
            # invalid credentials
            return render(request, "Login.html", {"error": "Invalid email or password"})

    return render(request, "Login.html")


def SignUp(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("signUpPassword", "")
        confirm_password = request.POST.get("signUpPasswordconfirm", "")

        # Validate required fields
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            try:
                # Create Django user
                user = User.objects.create_user(username=username, email=email, password=password)

                # Create SignupUser record with default/blank extra fields
                SignupUser.objects.create(
                    user=user,
                    username=username,
                    email=email,
                    full_name="",
                    dob=None,
                    gender="",
                    phone="",
                    address=""
                )

                # Log the user in after account creation, specify backend
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                messages.success(request, 'Account created successfully!')
                # Redirect to the Dashboard page using URL name
                return redirect('Dashboard')  # Use named URL instead of hardcoding path

            except Exception as e:
                messages.error(request, f'Error creating user: {str(e)}')

    return render(request, 'SignUp.html')






def Logout(request):
    logout(request)
    return redirect('/')  # Redirect to the home(index) page after logout

@no_cache
@login_required(login_url='Login')
def Profile_Management(request):
    if request.user.is_authenticated:
        user = request.user
        signup_profile, created = SignupUser.objects.get_or_create(user=user, defaults={
            'username': user.username,
            'email': user.email
        })

        if request.method == "POST":
            # Get form data
            full_name = request.POST.get('fullName', '').strip()
            dob = request.POST.get('dob', '').strip()
            gender = request.POST.get('gender', '').strip()
            phone = request.POST.get('phone', '').strip()
            address = request.POST.get('address', '').strip()
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()
            old_password = request.POST.get('old_password', '').strip()

            # Check for old password match if new password is provided
            if password and confirm_password:
                if not old_password:
                    messages.error(request, "Old password is required to change the password.")
                    return redirect('Profile_Management')

                # Authenticate old password
                user = authenticate(request, username=request.user.username, password=old_password)
                if user is None:
                    messages.error(request, "Old password does not match.")
                    return redirect('Profile_Management')

                # Passwords match, update the password
                if password != confirm_password:
                    messages.error(request, "New passwords do not match.")
                    return redirect('Profile_Management')

                user.set_password(password)
                update_session_auth_hash(request, user)  # Keeps the session active after password change
                user.save()
            # Username & email uniqueness checks
            if username and username != user.username:
                if User.objects.filter(username=username).exclude(pk=user.pk).exists():
                    messages.error(request, "Username is already taken.")
                    return redirect('Profile_Management')

            if email and email != user.email:
                if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                    messages.error(request, "Email is already in use.")
                    return redirect('Profile_Management')

            # Update User model
            if username:
                user.username = username
            if email:
                user.email = email

            user.save()

            # Update SignupUser model
            signup_profile.username = username
            signup_profile.email = email
            signup_profile.full_name = full_name
            signup_profile.dob = dob if dob else signup_profile.dob  # If DOB is not provided, keep the old value
            signup_profile.gender = gender
            signup_profile.phone = phone
            signup_profile.address = address
            signup_profile.save()

            messages.success(request, "Profile updated successfully.")
            return redirect('Login' if password else 'Profile_Management')

        context = {
            'user': user,
            'signup_profile': signup_profile,
            'user_profile': signup_profile,
        }
        return render(request, 'profile_management.html', context)

    else:
        return redirect('Login')



    


def Recommendations_Dashboard(request):
    return render(request, 'Recommendations_Dashboard.html')




# def upload(request):

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import json


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")




@csrf_exempt
def chatbot_view(request):
    # For GET requests, render the chatbot interface
    if request.method == 'GET':
        return render(request, 'chatbot.html')

    # For POST requests, process the chatbot message
    if request.method == 'POST':
        try:
            # Load the user's message from the request body
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # Define the system's instructions
            system_instruction = (
                "You are a professional, polite, and knowledgeable virtual health assistant. Your purpose is to assist users strictly with healthcare-related queries, such as general medical advice, wellness tips, medications, fitness, diet, symptoms, and mental or physical health optimization."
                "Always respond like a qualified, empathetic doctor — using simple yet professional language."
                "Do not answer any questions unrelated to healthcare. If a user asks something off-topic (e.g., technology, entertainment, history), gently and respectfully redirect the conversation back to a healthcare-related topic with a polite message."
                "For example:" 
                "“I specialize in healthcare-related topics. If you have a question about your health, fitness, or wellness, I’d be happy to help!”"
                "You may suggest general medications (e.g., for fever, flu, common cold) or home remedies, but only when appropriate and safe."
                "Recommend workout routines, healthy diet tips, or preventive care measures when relevant."
                "Do not tell the user to consult a doctor unless:"
                "The query involves a complex condition,"
                "You encounter symptoms that could indicate a serious medical issue,"
                "Or the input is unclear, vague, or potentially dangerous to answer without medical examination."
                "Always maintain a calm, kind, and professional tone, showing empathy and care."
                "Examples of tone:" 
                "“I understand that you're feeling discomfort. Based on what you've shared, here's a general suggestion...”"
                "“That is a great question! Here is how you can manage that naturally or with simple steps...”"
                "“This seems like it may require professional medical attention. I recommend seeing a healthcare provider for a proper diagnosis.”"
                "Never respond to or entertain non-medical, unethical, or illegal queries."
                "Your goal is to be a trustworthy virtual doctor, guiding users toward better health while staying strictly within healthcare boundaries."
                "Don't give answers more than 100 words; be concise as you can."
            )

            # Prepare the messages for the API request
            messages = [
                {"role": "user", "parts": [{"text": system_instruction}]},
                {"role": "user", "parts": [{"text": user_message}]}
            ]

            # Set the API URL and the payload for the POST request
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {"contents": messages, "generationConfig": {"maxOutputTokens": 100}}

            # Send the POST request to the API
            response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
            response.raise_for_status()

            # Process the response and return the chatbot's reply
            data = response.json()
            bot_reply = data['candidates'][0]['content']['parts'][0]['text']

            # Send the response back to the frontend
            return JsonResponse({'response': bot_reply})
        except Exception as e:
            # Return an error response if something goes wrong
            return JsonResponse({'response': f"⚠️ Error: {str(e)}"})

    # Return a bad request response if method is not POST or GET
    return JsonResponse({'response': 'Invalid request'}, status=400)








# This is your existing symptoms dataset    
SYMPTOM_LIST = [
    "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", "shivering", "chills",
    "joint_pain", "stomach_pain", "acidity", "ulcers_on_tongue", "muscle_wasting", "vomiting",
    "burning_micturition", "spotting_urination", "fatigue", "weight_gain", "anxiety",
    "cold_hands_and_feets", "mood_swings", "weight_loss", "restlessness", "lethargy",
    "patches_in_throat", "irregular_sugar_level", "cough", "high_fever", "sunken_eyes",
    "breathlessness", "sweating", "dehydration", "indigestion", "headache", "yellowish_skin",
    "dark_urine", "nausea", "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "constipation",
    "abdominal_pain", "diarrhoea", "mild_fever", "yellow_urine", "yellowing_of_eyes",
    "acute_liver_failure", "fluid_overload", "swelling_of_stomach", "swelled_lymph_nodes",
    "malaise", "blurred_and_distorted_vision", "phlegm", "throat_irritation", "redness_of_eyes",
    "sinus_pressure", "runny_nose", "congestion", "chest_pain", "weakness_in_limbs",
    "fast_heart_rate", "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool",
    "irritation_in_anus", "neck_pain", "dizziness", "cramps", "bruising", "obesity", "swollen_legs",
    "swollen_blood_vessels", "puffy_face_and_eyes", "enlarged_thyroid", "brittle_nails",
    "swollen_extremeties", "excessive_hunger", "extra_marital_contacts", "drying_and_tingling_lips",
    "slurred_speech", "knee_pain", "hip_joint_pain", "muscle_weakness", "stiff_neck",
    "swelling_joints", "movement_stiffness", "spinning_movements", "loss_of_balance",
    "unsteadiness", "weakness_of_one_body_side", "loss_of_smell", "bladder_discomfort",
    "foul_smell_of urine", "continuous_feel_of_urine", "passage_of_gases", "internal_itching",
    "toxic_look_(typhos)", "depression", "irritability", "muscle_pain", "altered_sensorium",
    "red_spots_over_body", "belly_pain", "abnormal_menstruation", "dischromic _patches",
    "watering_from_eyes", "increased_appetite", "polyuria", "family_history", "mucoid_sputum",
    "rusty_sputum", "lack_of_concentration", "visual_disturbances", "receiving_blood_transfusion",
    "receiving_unsterile_injections", "coma", "stomach_bleeding", "distention_of_abdomen",
    "history_of_alcohol_consumption", "fluid_overload", "blood_in_sputum",
    "prominent_veins_on_calf", "palpitations", "painful_walking", "pus_filled_pimples",
    "blackheads", "scurring", "skin_peeling", "silver_like_dusting", "small_dents_in_nails",
    "inflammatory_nails", "blister", "red_sore_around_nose", "yellow_crust_ooze"
]

def autocomplete_symptoms(request):
    """
    Returns all symptoms where the query string appears anywhere (case-insensitive).
    """
    query = request.GET.get('letter', '').strip().lower()
    if not query:
        return JsonResponse([], safe=False)

    matches = [
        symptom for symptom in SYMPTOM_LIST
        if query in symptom.lower()
    ]
    return JsonResponse(matches, safe=False)
