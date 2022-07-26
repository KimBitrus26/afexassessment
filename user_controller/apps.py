from django.apps import AppConfig


class UserControllerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_controller'

    def ready(self):
        import user_controller.signals
