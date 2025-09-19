from django.apps import AppConfig


class RegistrodemanutencaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'registro_manutencao'

    def ready(self):
        # Temporariamente desabilitado para debug
        # import registro_manutencao.signals
        pass
