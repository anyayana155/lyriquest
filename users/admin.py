from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import User
import json

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'formatted_favorites')
    readonly_fields = ('formatted_favorites',)
    
    def formatted_favorites(self, obj):
        return mark_safe(f"<pre>{json.dumps(obj.favorite_artists, indent=2)}</pre>")
    formatted_favorites.short_description = "Favorite Artists (Pretty)"

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Preferences', {
            'fields': (
                'favorite_artists',
                'disliked_artists',
                'formatted_favorites',
            ),
            'classes': ('collapse',)
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

admin.site.register(User, CustomUserAdmin)