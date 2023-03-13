from django.contrib import admin
from .models import Record

# Register your models here.

class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'roll_no', 'score', 'sheet']
    list_display_links = ['id', 'roll_no']

    def delete_queryset(self, request, queryset):
        files = []
        for instance in queryset:
            files.append(instance.sheet)
        temp = super().delete_queryset(request, queryset)
        for file in files:
            if file is not None:
                file.delete(save=False)
        return temp

admin.site.register(Record, RecordAdmin)
