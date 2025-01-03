from django.contrib import admin
from django.forms import ModelForm, Textarea
from .models import Performance

# Δημιουργούμε μια φόρμα για το Performance
class PerformanceForm(ModelForm):
    class Meta:
        model = Performance
        fields = '__all__'
        widgets = {
            'comments': Textarea(attrs={'rows': 3, 'cols': 40}),  # Ρυθμίζουμε το comments ως Textarea
        }

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    form = PerformanceForm  # Συνδέουμε τη φόρμα με το admin
    list_display = (
        'performance_id', 'title', 'festival', 'description', 'kind', 
        'technical_specs', 'performance_status', 'duration', 
        'starting_time', 'datetime'
    )
    search_fields = ('title', 'kind',)
