from django.contrib import admin
from .models import Connection, JsonDictionaryEntry, DictGroup, GetType





admin.site.register(Connection)
admin.site.register(GetType)
admin.site.register(JsonDictionaryEntry)
admin.site.register(DictGroup)