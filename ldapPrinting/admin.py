from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)

admin.site.register(session)
