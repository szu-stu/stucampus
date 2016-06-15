from django.contrib import admin
from .models import User,PlanCategory,Plan,PlanRecord,Lottery,LotteryList

admin.site.register(User)
admin.site.register(PlanCategory)
admin.site.register(Plan)
admin.site.register(PlanRecord)
admin.site.register(Lottery)
admin.site.register(LotteryList)