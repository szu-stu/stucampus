from django.contrib import admin
from .models import User,PlanCategory,Plan,PlanRecord

admin.site.register(User)
admin.site.register(PlanCategory)
admin.site.register(Plan)
admin.site.register(PlanRecord)