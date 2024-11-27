from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.db import connection
from django.http import JsonResponse
from django.utils import timezone
import json
from django.shortcuts import render
from django.db.models import Q
import json
import openai


def process_quiz_results(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            disorder_scores = data.get("disorder_scores", {})
            
            # Save results to the database
            if request.user.is_authenticated:
                QuizResult.objects.create(user=request.user, disorder_scores=disorder_scores)
            
            # Redirect to recommendations
            return JsonResponse({"redirect_url": "/recommendations/"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    
    return JsonResponse({"error": "Invalid request method."}, status=405)





DISORDER_COLUMN_MAPPING = {
    "Depression": "depression_percentage",
    "Mood Disorders": "mood_disorder_percentage",
    "Anxiety Disorders": "anxiety_percentage",
    "Somatic Disorders": "somatic_disorder_percentage",
    "Trauma-Related Disorders": "trauma_percentage",
    "Stress-Related Disorders": "stress_percentage",
    "Obsessive-Compulsive Disorder (OCD)": "obsessive_compulsive_percentage",
    "Psychotic Disorders": "psychotic_percentage",
    "Dissociative Disorders": "dissociative_percentage",
    "Neurocognitive Disorders": "neurocognitive_percentage",
    "Neurodevelopmental Disorders": "neurodevelopmental_percentage",
    "Substance Use Disorders": "substance_use_percentage",
    "Personality Disorders": "personality_percentage",
    "Sleep-Wake Disorders": "sleep_disorder_percentage",
    "Self-Harm": "self_harm_percentage",
    "Eating Disorders": "eating_percentage",
}

SCORE_DESCRIPTION_MAPPING = {
    0: "No signs of this disorder.",
    100: "Mild symptoms detected.",
    200: "Significant symptoms detected; consider seeking help.",
}

def recommendations(request):
    # Fetch the latest quiz results for the user
    result = QuizResult.objects.filter(user=request.user).order_by('-completed_at').first()

    if not result:
        return render(request, "no_results.html", {"message": "No results found."})

    # Use scores directly (0, 100, or 200)
    disorder_scores = result.disorder_scores

    # Filter non-zero scores and add descriptions
    non_zero_disorder_scores = {
        disorder: {
            "score": score,
            "description": SCORE_DESCRIPTION_MAPPING.get(score, "Unknown severity"),
        }
        for disorder, score in disorder_scores.items() if score > 0
    }

    # Check if all scores are zero
    if not non_zero_disorder_scores:
        return render(request, "recommendation.html", {
            "message": "Great news! Your scores indicate that you are doing well. No specific recommendations are needed at this time.",
            "book_recommendations": [],
            "exercise_recommendations": [],
            "podcast_recommendations": [],
            "movie_recommendations": [],
            "music_recommendations": [],
            "workout_recommendations": [],
            "yoga_recommendations": [],
            "non_zero_disorder_scores": {},
        })

    # Separate recommendations for each type
    book_recommendations = set()
    exercise_recommendations = set()
    podcast_recommendations = set()
    movie_recommendations = set()
    music_recommendations = set()
    workout_recommendations = set()
    yoga_recommendations = set()

    # Gather recommendations for non-zero scores
    for disorder, data in non_zero_disorder_scores.items():
        score = data["score"]
        disorder_column = DISORDER_COLUMN_MAPPING.get(disorder)
        if disorder_column:
            # Fetch books where disorder value matches user's score
            books = Book.objects.filter(
                **{f"{disorder_column}": score}
            )
            book_recommendations.update(book.book_name for book in books)

            # Fetch breathing exercises
            exercises = BreathingExercise.objects.filter(
                **{f"{disorder_column}": score}
            )
            exercise_recommendations.update(exercise.exercise_name for exercise in exercises)

            # Fetch podcasts
            podcasts = Podcast.objects.filter(
                **{f"{disorder_column}": score}
            )
            podcast_recommendations.update(podcast.podcast_name for podcast in podcasts)

            # Fetch movies
            movies = Movie.objects.filter(
                **{f"{disorder_column}": score}
            )
            movie_recommendations.update(movie.movie_name for movie in movies)

            # Fetch music
            music_tracks = Music.objects.filter(
                **{f"{disorder_column}": score}
            )
            music_recommendations.update(track.music_name for track in music_tracks)

            # Fetch workouts
            workouts = Workout.objects.filter(
                **{f"{disorder_column}": score}
            )
            workout_recommendations.update(workout.workout_name for workout in workouts)

            # Fetch yoga
            yoga_poses = Yoga.objects.filter(
                **{f"{disorder_column}": score}
            )
            yoga_recommendations.update(pose.yoga_name for pose in yoga_poses)

    # Check if all recommendations are empty
    all_recommendations = [
        book_recommendations, 
        exercise_recommendations, 
        podcast_recommendations, 
        movie_recommendations, 
        music_recommendations, 
        workout_recommendations, 
        yoga_recommendations
    ]

    if all(not rec for rec in all_recommendations):
        return render(request, "recommendation.html", {
            "message": "No specific recommendations found for your current scores.",
            "book_recommendations": [],
            "exercise_recommendations": [],
            "podcast_recommendations": [],
            "movie_recommendations": [],
            "music_recommendations": [],
            "workout_recommendations": [],
            "yoga_recommendations": [],
            "non_zero_disorder_scores": non_zero_disorder_scores,
        })

    return render(
        request,
        "recommendation.html",
        {
            "message": "",
            "book_recommendations": list(book_recommendations),
            "exercise_recommendations": list(exercise_recommendations),
            "podcast_recommendations": list(podcast_recommendations),
            "movie_recommendations": list(movie_recommendations),
            "music_recommendations": list(music_recommendations),
            "workout_recommendations": list(workout_recommendations),
            "yoga_recommendations": list(yoga_recommendations),
            "non_zero_disorder_scores": non_zero_disorder_scores,
        },
    )

   

@login_required
def quiz(request):
    questions_data = []
    questions = Question.objects.prefetch_related('options').all()

    # Prepare quiz data
    for question in questions:
        options = [
            {
                "id": option.id,
                "text": option.option_text,
                "disorders": {
                        "Depression": option.depression_percentage,
                        "Mood Disorders": option.mood_disorder_percentage,
                        "Anxiety Disorders": option.anxiety_percentage,
                        "Somatic Disorders": option.somatic_disorder_percentage,
                        "Trauma-Related Disorders": option.trauma_percentage,
                        "Stress-Related Disorders": option.stress_precentage,
                        "Obsessive-Compulsive Disorder (OCD)": option.obsessive_compulsive_percentage,
                        "Psychotic Disorders": option.psychotic_percentage,
                        "Dissociative Disorders": option.dissociative_disorders_percentage,
                        "Neurocognitive Disorders": option.neurocognitive_percentage,
                        "Neurodevelopmental Disorders": option.neurodevelopmental_percentage,
                        "Substance Use Disorders": option.substance_use_percentage,
                        "Personality Disorders": option.personality_precentage,
                        "Sleep-Wake Disorders": option.sleep_disorder_percentage,
                        "Self-Harm": option.self_harm_percentage,
                        "Eating Disorders": option.eating_percentage
                        
                }
            } for option in question.options.all()
        ]

        questions_data.append({
            "id": question.id,
            "type": question.question_type,
            "text": question.question_text,
            "options": options
        })

    # Handle POST request for recommendations
    if request.method == "POST":
        threshold = 150
        scores = json.loads(request.POST.get('disorder_scores', '{}'))
        high_scoring_disorders = {disorder: score for disorder, score in scores.items() if score > threshold}

        # Map high scoring disorders to model fields and build query
        field_mapping = {
            "Depression": "depression_percentage",
            "Mood Disorders": "mood_disorder_percentage",
            "Anxiety Disorders": "anxiety_percentage",
            "Somatic Disorders": "somatic_disorder_percentage",
            "Trauma-Related Disorders": "trauma_percentage",
            "Stress-Related Disorders": "stress_percentage",
            "Obsessive-Compulsive Disorder (OCD)": "obsessive_compulsive_percentage",
            "Psychotic Disorders": "psychotic_percentage",
            "Dissociative Disorders": "dissociative_percentage",
            "Neurocognitive Disorders": "neurocognitive_percentage",
            "Neurodevelopmental Disorders": "neurodevelopmental_percentage",
            "Substance Use Disorders": "substance_use_percentage",
            "Personality Disorders": "personality_percentage",
            "Sleep-Wake Disorders": "sleep_disorder_percentage",
            "Self-Harm": "self_harm_percentage",
            "Eating Disorders": "eating_percentage",
        }

        query = Q()
        for disorder, score in high_scoring_disorders.items():
            field_name = field_mapping.get(disorder)
            if field_name:
                query |= Q(**{f"{field_name}__gt": 0})

        recommendations = []
        if query:
            books = Book.objects.filter(query)
            recommendations = [{"name": book.book_name} for book in books]

        return render(request, 'quiz.html', {
            "quiz_data": json.dumps(questions_data),
            "recommendations": recommendations,
        })

    return render(request, 'quiz.html', {"quiz_data": json.dumps(questions_data)})



# @login_required
# def quiz(request):
#     questions_data = []
#     questions = Question.objects.prefetch_related('options').all()

#     for question in questions:
#         # Debugging: Check if options are correctly loaded
#         print(f"Question: {question.question_type}")
#         options = []
#         for option in question.options.all():
#             options.append({
#                 "id": option.id,
#                 "text": option.option_text,
                # "disorders": {
                #         "Depression": option.depression_percentage,
                #         "Mood Disorders": option.mood_disorder_percentage,
                #         "Anxiety Disorders": option.anxiety_percentage,
                #         "Somatic Disorders": option.somatic_disorder_percentage,
                #         "Trauma-Related Disorders": option.trauma_percentage,
                #         "Stress-Related Disorders": option.stress_precentage,
                #         "Obsessive-Compulsive Disorder (OCD)": option.obsessive_compulsive_percentage,
                #         "Psychotic Disorders": option.psychotic_percentage,
                #         "Dissociative Disorders": option.dissociative_disorders_percentage,
                #         "Neurocognitive Disorders": option.neurocognitive_percentage,
                #         "Neurodevelopmental Disorders": option.neurodevelopmental_percentage,
                #         "Substance Use Disorders": option.substance_use_percentage,
                #         "Personality Disorders": option.personality_precentage,
                #         "Sleep-Wake Disorders": option.sleep_disorder_percentage,
                #         "Self-Harm": option.self_harm_percentage,
                #         "Eating Disorders": option.eating_percentage
                        
                # }
#             })
        
#         questions_data.append({
#             "id": question.id,
#             "type":question.question_type,
#             "text": question.question_text,
#             "options": options
#         })
    
    

#     return render(request, 'quiz.html', {"quiz_data": json.dumps(questions_data)})



# def quiz(request):
#     questions_data = []
#     questions = Question.objects.prefetch_related('options').all()

#     for question in questions:
#         options = [
#             {
#                 "id": option.id,
#                 "text": option.option_text,
#                 "disorders": {
#                     "Depression": option.depression_percentage,
#                     "Mood Disorder": option.mood_disorder_percentage,
#                     "Anxiety": option.anxiety_percentage,
#                     "Somatic Disorder": option.somatic_disorder_percentage,
#                     "Trauma": option.trauma_percentage,
#                     "Stress": option.stress_precentage,
#                     "Obsessive Compulsive": option.obsessive_compulsive_percentage,
#                     "Psychotic": option.psychotic_percentage,
#                     "Dissociative": option.dissociative_precentage,
#                     "Neurocognitive": option.neurocognitive_percentage,
#                     "Neurodevelopmental": option.neurodevelopmental_percentage,
#                     "Substance Use": option.substance_use_percentage,
#                     "Personality": option.personality_precentage,
#                     "Sleep-Wake": option.sleep_disorder_percentage,
#                     "Self-Harm": option.self_harm_percentage,
#                     "Eating Disorder": option.eating_percentage,
#                 }
#             }
#             for option in question.options.all()
#         ]

#         questions_data.append({
#             "id": question.id,
#             "text": question.question_text,
#             "options": options
#         })
        
     
      

#     return render(request, 'quiz.html', {"quiz_data": json.dumps(questions_data) })


# def quiz(request):
    
#     stage_1_questions = Question.objects.filter(stage=1).prefetch_related('options')
#     stage_2_questions = Question.objects.filter(stage=2).prefetch_related('options')
    
#     quiz_data = {
#         'stage_1': [],
#         'stage_2': []
#     }
    
    
#     for question in stage_1_questions:
#         options = [{'id': option.id, 'text': option.text} for option in question.options.all()]
#         quiz_data['stage_1'].append({
#             'question_id': question.id,
#             'text': question.text,
#             'options': options
#         })

    
#     for question in stage_2_questions:
#         options = [{'id': option.id, 'text': option.text} for option in question.options.all()]
#         quiz_data['stage_2'].append({
#             'question_id': question.id,
#             'text': question.text,
#             'options': options
#         })

    
#     context = {
#         'quiz_data': json.dumps(quiz_data),
#     }
#     return render(request, 'quiz.html', context)

import os
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils import timezone
import openai

import logging

def assess_support_level(message):
    """
    Assess the support level based on message content
    """
    high_risk_keywords = [
        'suicide', 'kill myself', 'want to die', 
        'hopeless', 'cant go on', 'ending it all',
        'giving up', 'no way out', 'pain is too much'
    ]
    
    moderate_risk_keywords = [
        'depressed', 'anxious', 'stressed', 
        'overwhelmed', 'struggling', 'help',
        'sad', 'lonely', 'worthless', 'exhausted'
    ]
    
    message_lower = message.lower()
    
    if any(keyword in message_lower for keyword in high_risk_keywords):
        return 'high_risk'
    elif any(keyword in message_lower for keyword in moderate_risk_keywords):
        return 'moderate_risk'
    
    return 'low_risk'

def ask_openai(message):
    """
    Generate a response using OpenAI's ChatGPT with support level assessment
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a compassionate, empathetic mental health support assistant. " 
                               "Provide supportive, understanding responses. Be kind, non-judgmental, " 
                               "and offer gentle guidance when appropriate."
                },
                {"role": "user", "content": message}
            ]
        )
        
        # Extract the response from the assistant
        bot_response = response['choices'][0]['message']['content'].strip()
        return bot_response
    
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return "I'm here to listen. Would you like to share more about how you're feeling?"

@login_required
def chatbot(request):
    """
    Handle chatbot interactions with chat history management
    """
    # Clear existing chat history on page refresh/load
    if request.method == 'GET':
        Chat.objects.filter(user=request.user).delete()
    
    # Handle POST requests for sending messages
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        
        if not message:
            return JsonResponse({
                'message': '', 
                'response': 'I noticed you sent an empty message. Would you like to share something?',
                'support_level': 'low_risk'
            })
        
        # Assess support level
        support_level = assess_support_level(message)
        
        # Generate response using OpenAI
        try:
            response = ask_openai(message)
            
            # Create and save chat entry
            chat = Chat(
                user=request.user, 
                message=message, 
                response=response, 
                support_level=support_level,
                created_at=timezone.now()
            )
            chat.save()
            
            return JsonResponse({
                'message': message, 
                'response': response,
                'support_level': support_level
            })
        
        except Exception as e:
            logging.error(f"Chatbot error: {e}")
            return JsonResponse({
                'message': message, 
                'response': 'Sorry, I am experiencing some technical difficulties.',
                'support_level': 'low_risk'
            }, status=500)
    
    # Render chatbot template
    return render(request, 'chatbot.html')

def logout(request):
    """
    Custom logout view with chat history clearing
    """
    # Clear chat history for the current user
    if request.user.is_authenticated:
        Chat.objects.filter(user=request.user).delete()
    
    # Standard logout process
    auth_logout(request)
    
    # Redirect to login page
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def login(request):
    """
    Custom login view with chat history clearing
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Clear previous chat history for the user
            Chat.objects.filter(user=user).delete()
            
            # Log in the user
            auth_login(request, user)
            
            # Redirect to home or desired page
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')
        else:
            # Return an 'invalid login' error message
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


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

def schedules(request):
    return render(request,'Schedule.html')
