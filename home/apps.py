from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
    def ready(self) -> None:
        from jobs import updater
        updater.start_job1()
        updater.start_job2()