from django.contrib import admin
from .models import Performance

@admin.register(Performance)  # Μόνο το μοντέλο που θέλουμε να καταχωρίσουμε στο Admin
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('performance_id','title', 'festival', 'description','kind','performance_status', 'duration', 'starting_time', 'datetime')  # Ορίζουμε τι θα εμφανίζεται στη λίστα
    search_fields = ('title', 'kind',)           # Πεδία με τα οποία μπορεί να γίνει αναζήτηση
