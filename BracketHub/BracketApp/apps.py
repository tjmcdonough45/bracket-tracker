from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BracketappConfig(AppConfig):
    name = 'BracketApp'
    verbose_name = _('BracketApp')

    def ready(self):
        import BracketApp.signals
