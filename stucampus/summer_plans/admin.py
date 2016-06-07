from django.contrib import admin
from .models import User,PlanCategory,Plan

admin.site.register(User)
admin.site.register(PlanCategory)
admin.site.register(Plan)
