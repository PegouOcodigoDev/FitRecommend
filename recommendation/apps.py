from django.apps import AppConfig
from django.contrib.auth import get_user_model


class RecommendationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recommendation"

    def ready(self):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', '', 'admin')
