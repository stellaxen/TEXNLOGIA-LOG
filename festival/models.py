from django.db import models
from datetime import time
from django.utils.timezone import now  # Χρήση του timezone για timezone-aware datetime

from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.conf import settings

from django.db.models.signals import post_save
from performance.models import Performance

class Festival(models.Model):
  # Μοναδίκός αριθμός festival που δεν είναι κλείδί στη βάση και τον ενημερώνει η εφαρμογή
  festival_id = models.PositiveIntegerField(editable=False, unique=True, null=True, blank=True)
  # Ημερομηνία δημιουργίας της festival, παίρνει αυτόματα το current datetime
  datetime = models.DateTimeField(default=now, editable=False)
  # Τιτλος festival
  title = models.CharField(max_length=100)
  # Περιγραφή festival
  description = models.CharField(max_length=255)
  # Χώρος διεξαγωγής festival
  place = models.CharField(max_length=80)  
  # Ημερομηνίες διεξαγωγής festival
  festival_dates = models.CharField(max_length=80)    

  created_by = models.ForeignKey(
      settings.AUTH_USER_MODEL,  # Συνδέεται με το προσαρμοσμένο μοντέλο χρήστη
      on_delete=models.CASCADE,  # Αν διαγραφεί ο χρήστης, διαγράφεται και το Performance
      related_name='festivals'  # Για ευκολότερη πρόσβαση από την πλευρά του χρήστη
  )

  STATUSES = [
        ('created', 'CREATED'), 
        ('submission', 'SUBMISSION'), 
        ('assignment', 'ASSIGNMENT'), 
        ('review', 'REVIEW'), 
        ('scheduling', 'SCHEDULING'), 
        ('final_submission', 'FINAL_SUBMISSION'),
        ('decision', 'DECISION'), 
        ('announced', 'ANNOUNCED'), 
    ]    


  # Το πεδίο με τις επιλογές
  festival_status = models.CharField(
      max_length=20,  # Το μέγιστο μήκος του string
      choices=STATUSES,  # Οι επιλογές
      default='created',  # Προαιρετικά, η προεπιλεγμένη επιλογή
  )

  def clean(self):
        # Έλεγχος για ύπαρξη άλλου αντικειμένου με τον ίδιο τίτλο
        if Festival.objects.filter(title=self.title).exclude(pk=self.pk).exists():
            raise ValidationError(f"Υπάρχει ήδη καταχωρημένο φεστιβάλ με τίτλο '{self.title}'.")
        
  def save(self, *args, **kwargs):
    # Εκτέλεση του clean() πριν την αποθήκευση
    self.clean()
    super().save(*args, **kwargs)

  def __str__(self):
     return self.title  # Επιστρέφει τον τίτλο του festival για καλύτερη αναπαράσταση

# Σήμα για αυτόματη αύξηση του festival_id
@receiver(pre_save, sender=Festival)
def set_festival_id(sender, instance, **kwargs):
    if instance.festival_id is None:  # Αν το πεδίο δεν έχει ήδη τιμή
        max_id = sender.objects.aggregate(models.Max('festival_id'))['festival_id__max'] or 0
        instance.festival_id = max_id + 1

@receiver(post_save, sender=Festival)
def update_performances_on_status_change(sender, instance, **kwargs):
    if instance.festival_status == 'decision':
        Performance.objects.filter(festival=instance, performance_status='approved').update(performance_status='rejected')
