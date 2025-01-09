from django.contrib import admin
from .models import Entry, Advice, AdviceFeedback
# Register your models here.

admin.site.register(Entry)
admin.site.register(Advice)
admin.site.register(AdviceFeedback)