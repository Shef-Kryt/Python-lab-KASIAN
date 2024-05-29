from django.contrib import admin
from .models import Record
admin.site.site_header = "Kursova"

admin.site.register(Record)
