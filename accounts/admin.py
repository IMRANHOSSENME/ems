from django.contrib import admin
from accounts.models import MyUser as User

# Register your models here.
admin.site.register(User)
