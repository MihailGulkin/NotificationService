from django.contrib import admin

from .models import Message, Mailing, Filter

admin.site.register(Mailing)
admin.site.register(Message)
admin.site.register(Filter)
