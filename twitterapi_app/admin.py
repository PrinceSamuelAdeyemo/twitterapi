from django.contrib import admin
from .models import UserModel, ClientModel
# Register your models here.

admin.site.register(UserModel)
admin.site.register(ClientModel)