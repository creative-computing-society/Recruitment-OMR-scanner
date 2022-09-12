from django.db import models

# Create your models here.

def upload_to(instance, filename):
    return f"Sheets/{instance.id}_{filename}"

class Record(models.Model):
    roll_no = models.CharField(max_length=10, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    sheet = models.ImageField(upload_to=upload_to)
