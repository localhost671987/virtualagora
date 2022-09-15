from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ('email', 'user_name', 'first_name',)
    list_filter = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name',
                    'is_active', 'is_staff','is_subscribed')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name','last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_subscribed')}),
        ('Personal', {'fields': ('about', 'avatar')}),
    )
    formfield_overrides = {
        CustomUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff', 'avatar')}
         ),
    )


admin.site.register(CustomUser, UserAdminConfig)
