from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User,Listing,Bid

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)