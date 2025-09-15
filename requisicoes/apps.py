from django.apps import AppConfig


class RequisicoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'requisicoes'
    
    def ready(self):
        import requisicoes.signals