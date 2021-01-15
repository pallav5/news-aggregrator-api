from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Headline)
admin.site.register(Topic)
admin.site.register(Subscription)