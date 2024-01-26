from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from djangocms_alias.admin import AliasContentAdmin
from djangocms_alias.models import AliasContent

class AliasContentAdminExtended(AliasContentAdmin):
    def _get_references_link(self, obj, request):
        alias_content_type = ContentType.objects.get(
            app_label=obj.alias._meta.app_label,
            model=obj.alias._meta.model_name,
        )

        url = reverse_lazy(
            "djangocms_references:references-index",
            kwargs={"content_type_id": alias_content_type.id, "object_id": obj.alias.id}
        )

        return render_to_string("djangocms_references/references_icon.html", {"url": url})

    def get_list_actions(self):
        list_actions = []

        if hasattr(super(), "get_list_actions"):
            list_actions = super().get_list_actions()

        list_actions.append(self._get_references_link)

        return list_actions

admin.site.unregister(AliasContent)
admin.site.register(AliasContent, AliasContentAdminExtended)
