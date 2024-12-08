from django.contrib.auth.models import AbstractUser
from django.db import models

class Stuff(AbstractUser):
    # Τηλεφωνο επικοινωνίας
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username