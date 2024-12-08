from django.contrib import admin
from .models import Festival

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ('title','description','place', 'festival_dates', 'festival_status', 'created_by', 'festival_id','datetime')  # Ορίζουμε τι θα εμφανίζεται στη λίστα
    search_fields = ('title',)           # Πεδία με τα οποία μπορεί να γίνει αναζήτηση