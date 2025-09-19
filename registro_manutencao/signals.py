# signals.py

# registrodemanutencao/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import registrodemanutencao
from datetime import timedelta

def adicionar_dias_uteis(data_inicial, dias=5):
    dias_adicionados = 0
    data = data_inicial
    while dias_adicionados < dias:
        data += timedelta(days=1)
        if data.weekday() < 5:  # 0 = segunda, 6 = domingo
            dias_adicionados += 1
    return data

# Temporariamente desabilitado para debug
# @receiver(post_save, sender=registrodemanutencao)
# def set_data_devolucao(sender, instance, created, **kwargs):
#     if created and instance.data_devolucao is None:
#         # Calcula a data_devolucao adicionando 5 dias úteis a data_criacao
#         data_devolucao = adicionar_dias_uteis(instance.data_criacao, dias=5)
#         # Atualiza o campo data_devolucao sem disparar sinais novamente
#         registrodemanutencao.objects.filter(pk=instance.pk).update(data_devolucao=data_devolucao)
