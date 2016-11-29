from django.contrib import admin
import stucampus.christmas.models as giftChange_models

# Register your models here.

admin.site.register(giftChange_models.GiftSystem_user)
admin.site.register(giftChange_models.GivenGift)
admin.site.register(giftChange_models.ExchangeGift)
admin.site.register(giftChange_models.ChangeResult)
admin.site.register(giftChange_models.Gift)
