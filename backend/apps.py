from django.apps import AppConfig
import sys
sys.path.append('..')


class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'
    
    def ready(self):
        from mailing_service import updater
        updater.start()
