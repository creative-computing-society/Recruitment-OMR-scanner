from django.db import models
import os

# Create your models here.

def upload_to(instance, filename):
    return f"Sheets/{filename}"

class Record(models.Model):
    roll_no = models.CharField(max_length=10, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    sheet = models.ImageField(upload_to=upload_to)

    def delete(self):
        file = self.sheet
        tpl = super().delete()
        if file is not None:
            file.delete(save=False)
        return tpl
