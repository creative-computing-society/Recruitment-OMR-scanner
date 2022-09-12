from django.contrib import admin
from .models import Record

# Register your models here.

class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'roll_no', 'score', 'sheet']
    list_display_links = ['id', 'roll_no']

admin.site.register(Record, RecordAdmin)
