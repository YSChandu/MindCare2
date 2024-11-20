from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disorder_scores = models.JSONField()  # Store scores as JSON
    completed_at = models.DateTimeField(auto_now_add=True)  # Track completion time

    def __str__(self):
        return f"Quiz Result for {self.user.username} at {self.completed_at}"
    

class Question(models.Model):
    question_type = models.CharField(max_length=50 , default="stage_1")
    question_text = models.TextField()

    def __str__(self):
        return self.question_text


from django.db import models

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options',on_delete=models.CASCADE)
    anxiety_percentage = models.IntegerField(default=0)
    depression_percentage = models.IntegerField(default=0)
    dissociative_disorders_percentage = models.IntegerField(default=0)
    eating_percentage = models.IntegerField(default=0)
    mood_disorder_percentage = models.IntegerField(default=0)
    neurocognitive_percentage = models.IntegerField(default=0)
    neurodevelopmental_percentage = models.IntegerField(default=0)
    obsessive_compulsive_percentage = models.IntegerField(default=0)
    option_text = models.TextField()
    personality_precentage = models.IntegerField(default=0)
    psychotic_percentage = models.IntegerField(default=0)
    self_harm_percentage = models.IntegerField(default=0)
    sleep_disorder_percentage = models.IntegerField(default=0)
    somatic_disorder_percentage = models.IntegerField(default=0)
    stress_precentage = models.IntegerField(default=0)
    substance_use_percentage = models.IntegerField(default=0)
    trauma_percentage = models.IntegerField(default=0)

    def __str__(self):
        return self.option_text

# class Option(models.Model):
#     question = models.ForeignKey(Question, related_name='options',on_delete=models.CASCADE)
#     depression_percentage = models.IntegerField(default=0)
#     mood_disorders_percentage = models.IntegerField(default=0)
#     anxiety_disorders_percentage = models.IntegerField(default=0)
#     somatic_disorders_percentage = models.IntegerField(default=0)
#     trauma_related_disorders_percentage = models.IntegerField(default=0)
#     stress_related_disorders_percentage = models.IntegerField(default=0)
#     obsessive_compulsive_disorders_percentage = models.IntegerField(default=0)
#     psychotic_disorders_percentage = models.IntegerField(default=0)
#     dissociative_disorders_percentage = models.IntegerField(default=0)
#     neurocognitive_disorders_percentage = models.IntegerField(default=0)
#     neurodevelopmental_disorders_percentage = models.IntegerField(default=0)
#     substance_use_disorders_percentage = models.IntegerField(default=0)
#     personality_disorders_percentage = models.IntegerField(default=0)
#     sleep_wake_disorders_percentage = models.IntegerField(default=0)
#     self_harm_percentage = models.IntegerField(default=0)
#     eating_disorders_percentage = models.IntegerField(default=0)
#     option_text = models.TextField()

#     def __str__(self):
#         return self.option_text




# seperate tables for recommendation approach 3 

class BreathingExercise(models.Model):
    exercise_name = models.CharField(max_length=50)
    depression_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    anxiety_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mood_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    somatic_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    trauma_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stress_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    obsessive_compulsive_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    psychotic_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dissociative_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neurocognitive_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neurodevelopmental_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    substance_use_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    personality_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sleep_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    self_harm_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    eating_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.exercise_name



class Workout(models.Model):
    workout_name = models.CharField(max_length=50)
    depression_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    anxiety_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mood_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    somatic_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    trauma_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stress_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    obsessive_compulsive_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    psychotic_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dissociative_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neurocognitive_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neurodevelopmental_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    substance_use_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    personality_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sleep_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    self_harm_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    eating_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.workout_name


class Music(models.Model):
    music_name = models.CharField(max_length=50)
    depression_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    anxiety_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mood_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    somatic_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    trauma_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stress_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    obsessive_compulsive_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    psychotic_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dissociative_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neurocognitive_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neurodevelopmental_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    substance_use_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    personality_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sleep_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    self_harm_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    eating_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.music_name


class Yoga(models.Model):
    yoga_name = models.CharField(max_length=50)
    depression_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    anxiety_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mood_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    somatic_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    trauma_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stress_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    obsessive_compulsive_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    psychotic_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dissociative_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neurocognitive_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neurodevelopmental_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    substance_use_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    personality_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sleep_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    self_harm_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    eating_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.yoga_name


class Book(models.Model):
    book_name = models.CharField(max_length=100)
    depression_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    anxiety_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mood_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    somatic_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    trauma_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stress_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    obsessive_compulsive_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    psychotic_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dissociative_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neurocognitive_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neurodevelopmental_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    substance_use_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    personality_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sleep_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    self_harm_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    eating_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.book_name



class Podcast(models.Model):
    podcast_name = models.CharField(max_length=100)
    depression_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    anxiety_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mood_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    somatic_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    trauma_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stress_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    obsessive_compulsive_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    psychotic_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dissociative_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neurocognitive_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neurodevelopmental_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    substance_use_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    personality_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sleep_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    self_harm_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    eating_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.podcast_name



class Movie(models.Model):
    movie_name = models.CharField(max_length=100)
    depression_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    anxiety_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mood_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    somatic_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    trauma_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stress_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    obsessive_compulsive_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    psychotic_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dissociative_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neurocognitive_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neurodevelopmental_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    substance_use_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    personality_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sleep_disorder_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    self_harm_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    eating_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.movie_name


class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.question.text} - {self.selected_option.text}'



class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'


class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)  # Optional field
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)  # Optional field
    nationality = models.CharField(max_length=50, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


