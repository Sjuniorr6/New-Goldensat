from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Requisicoes
from produtos.models import MovimentacaoEstoque
from produtos.logger_config import produtos_logger
import traceback

# Temporariamente desabilitado para debug
# @receiver(post_save, sender=Requisicoes)
# def controlar_estoque_requisicao(sender, instance, created, **kwargs):
    """
    Controla o estoque quando uma requisição é criada ou seu status é alterado
    """
    try:
        if created:
            # Nova requisição criada - registrar saída de estoque
            if instance.tipo_produto and instance.numero_de_equipamentos:
                try:
                    quantidade = int(instance.numero_de_equipamentos)
                    if quantidade > 0:
                        MovimentacaoEstoque.objects.create(
                            produto=instance.tipo_produto,
                            tipo='saida',
                            quantidade=quantidade,
                            motivo=f'Requisição criada - ID: {instance.id}',
                            referencia=f'REQ_{instance.id}',
                            usuario=None  # Não temos usuário associado às requisições
                        )
                        produtos_logger.info(f'Saída de estoque registrada: {quantidade} unidades do produto {instance.tipo_produto.nome_produto} para requisição {instance.id}')
                except (ValueError, TypeError) as e:
                    produtos_logger.warning(f'Erro ao processar quantidade da requisição {instance.id}: {str(e)}')
        else:
            # Requisição atualizada - verificar mudança de status
            if hasattr(instance, '_previous_status'):
                status_anterior = instance._previous_status
                status_atual = instance.status
                
                # Se mudou de um status que consome estoque para um que não consome
                if (status_anterior in ['Pendente', 'Configurado', 'Aprovado pelo CEO'] and 
                    status_atual in ['Reprovado pelo CEO', 'Cancelado']):
                    
                    # Restaurar estoque
                    if instance.tipo_produto and instance.numero_de_equipamentos:
                        try:
                            quantidade = int(instance.numero_de_equipamentos)
                            if quantidade > 0:
                                MovimentacaoEstoque.objects.create(
                                    produto=instance.tipo_produto,
                                    tipo='entrada',
                                    quantidade=quantidade,
                                    motivo=f'Requisição {status_atual} - ID: {instance.id}',
                                    referencia=f'REQ_{instance.id}_RESTAURAR',
                                    usuario=None
                                )
                                produtos_logger.info(f'Estoque restaurado: {quantidade} unidades do produto {instance.tipo_produto.nome_produto} - requisição {instance.id} {status_atual}')
                        except (ValueError, TypeError) as e:
                            produtos_logger.warning(f'Erro ao restaurar estoque da requisição {instance.id}: {str(e)}')
                
                # Se mudou de um status que não consome para um que consome
                elif (status_anterior in ['Reprovado pelo CEO', 'Cancelado'] and 
                      status_atual in ['Pendente', 'Configurado', 'Aprovado pelo CEO']):
                    
                    # Consumir estoque novamente
                    if instance.tipo_produto and instance.numero_de_equipamentos:
                        try:
                            quantidade = int(instance.numero_de_equipamentos)
                            if quantidade > 0:
                                MovimentacaoEstoque.objects.create(
                                    produto=instance.tipo_produto,
                                    tipo='saida',
                                    quantidade=quantidade,
                                    motivo=f'Requisição {status_atual} - ID: {instance.id}',
                                    referencia=f'REQ_{instance.id}_CONSUMIR',
                                    usuario=None
                                )
                                produtos_logger.info(f'Estoque consumido: {quantidade} unidades do produto {instance.tipo_produto.nome_produto} - requisição {instance.id} {status_atual}')
                        except (ValueError, TypeError) as e:
                            produtos_logger.warning(f'Erro ao consumir estoque da requisição {instance.id}: {str(e)}')
    
    except Exception as e:
        produtos_logger.error(f'Erro no controle de estoque para requisição {instance.id}: {str(e)}')
        produtos_logger.error(traceback.format_exc())

# Temporariamente desabilitado para debug
# @receiver(post_delete, sender=Requisicoes)
# def restaurar_estoque_requisicao_excluida(sender, instance, **kwargs):
    """
    Restaura o estoque quando uma requisição é excluída
    """
    try:
        if instance.tipo_produto and instance.numero_de_equipamentos:
            try:
                quantidade = int(instance.numero_de_equipamentos)
                if quantidade > 0:
                    MovimentacaoEstoque.objects.create(
                        produto=instance.tipo_produto,
                        tipo='entrada',
                        quantidade=quantidade,
                        motivo=f'Requisição excluída - ID: {instance.id}',
                        referencia=f'REQ_{instance.id}_EXCLUIDA',
                        usuario=None
                    )
                    produtos_logger.info(f'Estoque restaurado por exclusão: {quantidade} unidades do produto {instance.tipo_produto.nome_produto} - requisição {instance.id}')
            except (ValueError, TypeError) as e:
                produtos_logger.warning(f'Erro ao restaurar estoque da requisição excluída {instance.id}: {str(e)}')
    
    except Exception as e:
        produtos_logger.error(f'Erro ao restaurar estoque da requisição excluída {instance.id}: {str(e)}')
        produtos_logger.error(traceback.format_exc())
