from django.contrib import admin
from .models import Connection, JsonDictionaryEntry, DictGroup, GetType


def auto_set_name(modeladmin, request, queryset):
   for obj in queryset:
       obj.update_display_value(obj.auto_gen_name())


class JsonDictionaryEntryAdmin(admin.ModelAdmin):
    list_display = ('jsonvalue', 'displayvalue', 'parent', 'haschildren')
    list_editable = ('displayvalue',)
    ordering = ('parent', 'displayvalue',)
    actions = [auto_set_name]

class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'hosturl', 'restuser')

class GetTypeAdmin(admin.ModelAdmin):
    list_display = ('resourcename', 'resourcepath')


admin.site.register(Connection, ConnectionAdmin)
admin.site.register(DictGroup)
admin.site.register(GetType, GetTypeAdmin)
admin.site.register(JsonDictionaryEntry, JsonDictionaryEntryAdmin)
