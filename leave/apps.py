from django.apps import AppConfig


class LeaveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leave'

    def ready(self):
        from leave.scheduling import update_scheduler
        update_scheduler()
        

