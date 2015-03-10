from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from profiles.models.user_profile import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'venue user'


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = UserAdmin.list_display + ('is_superuser', 'is_admin')

    def is_admin(self, user):
        return user.is_admin

    is_admin.boolean = True

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)