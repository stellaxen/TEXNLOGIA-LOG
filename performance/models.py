from django.db import models
from datetime import time
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Performance(models.Model):
    class Meta:
        permissions = [
            ("can_edit_own_or_administered_performance", "Can edit or delete own or administered performances"),
        ]


    # Συσχέτιση με το Festival
    festival = models.ForeignKey(
        'festival.Festival',  # Η πλήρης αναφορά στο μοντέλο Festival της εφαρμογής 'festival'
        on_delete=models.CASCADE,  # Αν διαγραφεί το festival, διαγράφεται και η παράσταση
        related_name='performances',  # Συσχέτιση με το όνομα της σχέσης στο Festival μοντέλο
    )

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

    technical_specs = models.FileField(
        upload_to='technical_specs/',  # Ο φάκελος όπου θα αποθηκεύονται τα αρχεία
        blank=True,  # Επιτρέπει το πεδίο να είναι κενό
        null=True    # Επιτρέπει τη μη ύπαρξη τιμής
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
            raise ValidationError(f"Η παράσταση με τίτλο '{self.title}' υπάρχει ήδη στο festival '{self.festival.title}'.")

        
        # Έλεγχος αν το festival_status του συνδεδεμένου Festival είναι "announced"
        if self.festival.festival_status == 'announced':
            raise ValidationError(f"Δεν μπορείτε να αλλάξετε το performance_status, καθώς το festival έχει ήδη ανακοινωθεί.")
        
        if self.technical_specs:
            valid_file_types = ['application/pdf', 'text/plain']
            if self.technical_specs.file.content_type not in valid_file_types:
                raise ValidationError('Το αρχείο πρέπει να είναι τύπου PDF ή TXT.')

        

    def save(self, *args, **kwargs):
        # Εκτέλεση του clean() πριν την αποθήκευση
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.festival.title}"  # Εμφανίζεται ο τίτλος της παράστασης και του festival

# Σήμα για αυτόματη αύξηση του performance_id
@receiver(pre_save, sender=Performance)
def set_performance_id(sender, instance, **kwargs):
    if instance.performance_id is None:  # Αν το πεδίο δεν έχει ήδη τιμή
        max_id = sender.objects.aggregate(models.Max('performance_id'))['performance_id__max'] or 0
        instance.performance_id = max_id + 1