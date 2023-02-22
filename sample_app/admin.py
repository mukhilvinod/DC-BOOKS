from django.contrib import admin
from .models import *
# Register your models here.



admin.site.register(shopregmodels)

admin.site.register(productmodels)

admin.site.register(cart)
admin.site.register( wishlist)
admin.site.register(buy)
admin.site.register(customercardM)
admin.site.register(shopNotification)
admin.site.register(userNotification)