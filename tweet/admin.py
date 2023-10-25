from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Twit
# Register your models here.

admin.site.unregister(Group)

# Mix Profile into User info
class ProfileInline(admin.StackedInline):
    model = Profile

#Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    #Displaying only usernames on admin page

    fields = ["username"]
    inline = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Twit)

