from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Stuff

@admin.register(Stuff)
class CustomStuffAdmin(UserAdmin):
    # Καθορίζεις τα πεδία που εμφανίζονται στη λίστα
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_active')
    # Καθορίζεις ποια πεδία μπορούν να χρησιμοποιηθούν για αναζήτηση
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')

    # Ρύθμιση των πεδίων που εμφανίζονται στην επεξεργασία ενός χρήστη
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Ρύθμιση των πεδίων κατά τη δημιουργία ενός νέου χρήστη
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone'),
        }),
    )
