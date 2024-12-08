from django.db import models
from datetime import time
from django.utils.timezone import now  # Χρήση του timezone για timezone-aware datetime
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings


class Performance(models.Model):
    # Μοναδίκός αριθμός παράστασης που δεν είναι κλείδί στη βάση και τον ενημερώνει η εφαρμογή
    performance_id = models.PositiveIntegerField(editable=False, unique=True, null=True, blank=True)
    # Ημερομηνία δημιουργίας της παράστασης, παίρνει αυτόματα το current datetime
    datetime = models.DateTimeField(default=now, editable=False)
    # Τίτλος παράστασης
    title = models.CharField(max_length=100, blank=False)
    # Περιγραφή παράστασης
    description = models.CharField(max_length=255, blank=False)
    # Είδος παράστασης
    kind = models.CharField(max_length=80, blank=False)
    # Διάρκεια παράστασης
    duration = models.FloatField()
    # Ώρα έναρξης παράστασης
    starting_time = models.TimeField(default=time(0, 0))  # Προεπιλογή: 00:00

    STATUSES = [
        ('created', 'CREATED'),
        ('submitted', 'SUBMITTED'),
        ('reviewed', 'REVIEWED'),
        ('rejected', 'REJECTED'),
        ('approved', 'APPROVED'),
        ('scheduled', 'SCHEDULED')
    ]
    # Το πεδίο με τις επιλογές
    performance_status = models.CharField(
        max_length=20,  # Το μέγιστο μήκος του string
        choices=STATUSES,  # Οι επιλογές
        default='created',  # Προαιρετικά, η προεπιλεγμένη επιλογή
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Συνδέεται με το προσαρμοσμένο μοντέλο χρήστη
        on_delete=models.CASCADE,  # Αν διαγραφεί ο χρήστης, διαγράφεται και το Performance
        related_name='performances'  # Για ευκολότερη πρόσβαση από την πλευρά του χρήστη
    )

  # Το πεδίο manager (επιτρέπει την επιλογή ενός χρήστη)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Συνδέεται με το μοντέλο χρήστη
        on_delete=models.SET_NULL,  # Αν διαγραφεί ο χρήστης, το πεδίο γίνεται NULL
        null=True,  # Επιτρέπει την τιμή NULL
        blank=True,  # Επιτρέπει να είναι προαιρετικό
        related_name='managed_performance',  # Επιστροφή από την πλευρά του χρήστη
    )

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],  # Επαλήθευση τιμών 1-5
        default=5,
        null=True,  # Επιτρέπει το NULL αν θέλουμε το πεδίο να είναι προαιρετικό
        blank=True  # Επιτρέπει να μείνει κενό στη φόρμα
    )

    administrators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='performance_admins')

  
    def clean(self):
        # Έλεγχος για ύπαρξη άλλου αντικειμένου με τον ίδιο τίτλο
        if Performance.objects.filter(title=self.title).exclude(pk=self.pk).exists():
            raise ValidationError(f"Υπάρχει ήδη παράσταση με τίτλο '{self.title}'.")

    def save(self, *args, **kwargs):
        # Εκτέλεση του clean() πριν την αποθήκευση
        self.clean()
        super().save(*args, **kwargs)


# Σήμα για αυτόματη αύξηση του performance_id
@receiver(pre_save, sender=Performance)
def set_performance_id(sender, instance, **kwargs):
    if instance.performance_id is None:  # Αν το πεδίο δεν έχει ήδη τιμή
        max_id = sender.objects.aggregate(models.Max('performance_id'))['performance_id__max'] or 0
        instance.performance_id = max_id + 1
