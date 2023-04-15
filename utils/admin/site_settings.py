from django.contrib import admin
from parler.admin import TranslatableAdmin
from solo.admin import SingletonModelAdmin

from utils.models.site_settings import SiteSettings
from utils.models.contacts_emails import EmailForContacts


admin.site.register(EmailForContacts)


@admin.register(SiteSettings)
class SiteSettingsAdmin(TranslatableAdmin, SingletonModelAdmin):
    pass
