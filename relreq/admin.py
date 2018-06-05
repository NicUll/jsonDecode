from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from relreq.namegenerator import auto_gen_name
from .models import Connection, JsonDictionaryEntry, DictGroup, GetType, SimpleSetting


def auto_set_name(modeladmin, request, queryset):
    for obj in queryset:
        obj.update_display_value(auto_gen_name(obj.jsonvalue))


############################
def hide_selected_values(modeladmin, request, queryset):
    queryset.update(hide_value=True)



def hide_selected_names(modeladmin, request, queryset):
    queryset.update(hide_name=True)


def show_selected_values(modeladmin, request, queryset):
    queryset.update(hide_value=False)
    show_selected_values.short_description = "Show selected names"


def show_selected_names(modeladmin, request, queryset):
    queryset.update(hide_name=False)
    show_selected_names.short_description = "Show selected values"


#############################

class DictGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'displayvalue', 'parent', 'link_to_dictentry')
    list_editable = ('displayvalue',)

    def link_to_dictentry(self, obj):
        link = reverse('admin:relreq_jsondictionaryentry_change', args=[obj.dictentryid])
        return format_html('<a href="{}">{}</a>', link, obj.dictentryid)
    link_to_dictentry.short_description = 'Dictionary Entry'


class JsonDictionaryEntryAdmin(admin.ModelAdmin):
    list_display = ('jsonvalue', 'displayvalue', 'link_to_parent', 'haschildren', 'hide_name', 'hide_value')
    list_editable = ('displayvalue', 'hide_name', 'hide_value')
    list_filter = ('parent',)
    ordering = ('parent', 'displayvalue',)
    actions = [auto_set_name, show_selected_names, hide_selected_names, show_selected_values, hide_selected_values, ]

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
admin.site.register(SimpleSetting)
