from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Diagnosis)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(UserResponse)
admin.site.register(Chat)
admin.site.register(Profile)
