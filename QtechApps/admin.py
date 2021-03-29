from django.contrib import admin
from . models import UserSearchHistory
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

admin.site.register(UserSearchHistory)

'''
class SearchHistory(admin.StackedInline):
    model=UserSearchHistory

class UserAdmin(AuthUserAdmin):
 inlines = [SearchHistory]

# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)
'''