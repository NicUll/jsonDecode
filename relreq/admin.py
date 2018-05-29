from django.contrib import admin
from .models import Connection, JsonDictionaryEntry, DictGroup, GetType


class JsonDictionaryEntryAdmin(admin.ModelAdmin):
    list_display = ('jsonvalue', 'displayvalue', 'parent', 'haschildren')
    ordering = ('parent', 'displayvalue',)

class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'hosturl', 'restuser')

class GetTypeAdmin(admin.ModelAdmin):
    list_display = ('resourcename', 'resourcepath')


admin.site.register(Connection, ConnectionAdmin)
admin.site.register(DictGroup)
admin.site.register(GetType, GetTypeAdmin)
admin.site.register(JsonDictionaryEntry, JsonDictionaryEntryAdmin)
