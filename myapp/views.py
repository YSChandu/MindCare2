from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.db import connection
from django.http import JsonResponse
import openai
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from .models import Question, Option, UserResponse
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Question


@login_required
def quiz(request):
    # Fetch all questions for stage 1 and stage 2, prefetching their associated options
    stage_1_questions = Question.objects.filter(stage=1).prefetch_related('options')
    stage_2_questions = Question.objects.filter(stage=2).prefetch_related('options')
    
    quiz_data = {
        'stage_1': [],
        'stage_2': []
    }
    
    # Organize stage 1 questions
    for question in stage_1_questions:
        options = [{'id': option.id, 'text': option.text} for option in question.options.all()]
        quiz_data['stage_1'].append({
            'question_id': question.id,
            'text': question.text,
            'options': options
        })

    # Organize stage 2 questions
    for question in stage_2_questions:
        options = [{'id': option.id, 'text': option.text} for option in question.options.all()]
        quiz_data['stage_2'].append({
            'question_id': question.id,
            'text': question.text,
            'options': options
        })

    
    context = {
        'quiz_data': json.dumps(quiz_data),
    }
    return render(request, 'quiz.html', context)


























# def quiz(request):
#     # Fetch all questions and their associated options and diagnoses
#     questions = Question.objects.prefetch_related('options__diagnosis')  # Prefetch related options and diagnoses
    
#     quiz_data = []
    
#     for question in questions:
#         options = []
#         for option in question.options.all():
#             # Collecting option text and its corresponding diagnosis
#             options.append({
#                 'text': option.text,
#                 'diagnosis': option.diagnosis.name if option.diagnosis else None  # Safely getting diagnosis name
#             })

#         quiz_data.append({
#             'question': question.text,
#             'options': options,
#         })
        
#     context = {
#         'quiz_data': json.dumps(quiz_data),  
#     }
    
#     return render(request, 'quiz.html', context)




# openai_api_key = ''
# openai.api_key = openai_api_key

def ask_openai(message):
    # Ensure you're using the correct model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
    )
    
    # Extract the response from the assistant
    bot_response = response['choices'][0]['message']['content'].strip()
    return bot_response

# Create your views here.
@login_required
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})



def home(request):
    return render(request ,'home.html')

def my_profile(request):
    user = request.user 
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM myapp_profile;")
        rows = cursor.fetchall()
        
    results = [{'1': row[0], '2': row[2], '3': row[3] , '4':row[4]} for row in rows]
    context = {
        'user': user,
        'result':results
    }
    
    return render(request, 'myprofile.html', context)


def register(request):
    if request.method =='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"username is already exists")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email is already exists")
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name,password=password)
                user.save();
                return redirect('login')
            
        else:
            messages.info(request,"passwords are not the same")
            return redirect('register')
    else:
        return render(request,'register.html')
    
    
def login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('login')
        
    else:
       return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def resources(request):
    return render(request ,'resources.html')

def yoga(request):
    return render(request,'yoga.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

@login_required
def edit_profile(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)
    
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

def issues(request):
    return render(request,'issues.html')

def anxietyissue(request):
    return render(request,'anxiety_issue.html')

def music(request):
    return render(request,"music.html")

def mooddisorder(request):
    return render(request,'mood_issue.html')

def OCD(request):
    return render(request,'OCD.html')

def trauma(request):
    return render(request,'trauma.html')

def personality(request):
    return render(request,'personality_issue.html')

def dissociative(request):
    return render(request,'dissociative.html')

def eating(request):
    return render(request,'eating.html')

def neurodevelop(request):
    return render(request,'neurodevelop.html')

def psychotic(request):
    return render(request,'psychotic.html')

def somatic(request):
    return render(request,'somatic.html')

def sleepissue(request):
    return render(request,'sleep_issue.html')

def impulse(request):
    return render(request,'impulse.html')

def drugs(request):
    return render(request,'drugs.html')

def neurocognit(request):
    return render(request,'neurocognit.html')

def selfharm(request):
    return render(request,'self_harm.html')

def aboutus(request):
    return render(request,'about.html')

def selfhelpbooks(request):
    return render(request,'selfhelp_books.html')

def exercise(request):
    return render(request,'workout.html')

def breathing(request):
    return render(request,'breathing.html')

def movies(request):
    return render(request,'movies.html')
