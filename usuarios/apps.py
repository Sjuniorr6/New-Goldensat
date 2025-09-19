from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'
    
    def ready(self):
        # Temporariamente desabilitado para debug
        # import usuarios.signals
        pass