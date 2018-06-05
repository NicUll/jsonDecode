from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from relreq.namegenerator import auto_gen_name
from .models import Connection, JsonDictionaryEntry, DictGroup, GetType


def auto_set_name(modeladmin, request, queryset):
    for obj in queryset:
        obj.update_display_value(auto_gen_name(obj.jsonvalue))


class DictGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'displayvalue', 'parent', 'dictentryid')

class JsonDictionaryEntryAdmin(admin.ModelAdmin):
    list_display = ('jsonvalue', 'displayvalue', 'link_to_parent', 'haschildren', 'hide_name', 'hide_value')
    list_editable = ('displayvalue', 'hide_name', 'hide_value')
    list_filter = ('parent',)
    ordering = ('parent', 'displayvalue',)
    actions = [auto_set_name]

    def link_to_parent(self, obj):
        link = reverse('admin:relreq_dictgroup_change', args=[obj.parent.pk])
        return format_html('<a href="{}">{}</a>', link, obj.parent.displayvalue)

    link_to_parent.short_description = 'Parent Group'


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'hosturl', 'restuser')


class GetTypeAdmin(admin.ModelAdmin):
    list_display = ('resourcename', 'resourcepath')


admin.site.register(Connection, ConnectionAdmin)
admin.site.register(DictGroup, DictGroupAdmin)
admin.site.register(GetType, GetTypeAdmin)
admin.site.register(JsonDictionaryEntry, JsonDictionaryEntryAdmin)
