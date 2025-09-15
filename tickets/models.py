from django.contrib.auth.models import User
from django.db import models

class TicketModel(models.Model):
    """Modelo para gerenciamento de tickets de suporte"""
    
    SETORES_CHOICES = [
        ('Diretoria', 'Diretoria'),
        ('Inteligência', 'Inteligência'),
        ('Faturamento', 'Faturamento'),
        ('Expedição', 'Expedição'),
        ('Configuração', 'Configuração'),
        ('Quality', 'Quality'),
        ('Área Técnica', 'Área Técnica'),
        ('Comercial', 'Comercial'),
    ]
    
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Em Andamento', 'Em Andamento'),
        ('Resolvido', 'Resolvido'),
        ('Fechado', 'Fechado'),
        ('Cancelado', 'Cancelado'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('Baixa', 'Baixa'),
        ('Média', 'Média'),
        ('Alta', 'Alta'),
        ('Crítica', 'Crítica'),
    ]

    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='tickets',
        verbose_name="Usuário"
    )
    setor = models.CharField(
        choices=SETORES_CHOICES, 
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name="Setor"
    )
    titulo = models.CharField(
        max_length=255, 
        verbose_name="Título do Ticket"
    )
    descricao_erro = models.TextField(
        verbose_name="Descrição do Problema"
    )
    correcao = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Correção Aplicada"
    )
    prioridade = models.CharField(
        choices=PRIORIDADE_CHOICES,
        max_length=20,
        default='Média',
        verbose_name="Prioridade"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=255, 
        default='Pendente',
        verbose_name="Status"
    )
    devolutiva = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Devolutiva"
    )
    responsavel = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_responsavel',
        verbose_name="Responsável"
    )
    data_resolucao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Resolução"
    )

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ['-data_criacao']

    def __str__(self):
        return f"Ticket #{self.id} - {self.titulo}"

    def get_status_badge_class(self):
        """Retorna a classe CSS para o badge de status"""
        status_classes = {
            'Pendente': 'bg-warning',
            'Em Andamento': 'bg-info',
            'Resolvido': 'bg-success',
            'Fechado': 'bg-secondary',
            'Cancelado': 'bg-danger',
        }
        return status_classes.get(self.status, 'bg-secondary')

    def get_prioridade_badge_class(self):
        """Retorna a classe CSS para o badge de prioridade"""
        prioridade_classes = {
            'Baixa': 'bg-success',
            'Média': 'bg-warning',
            'Alta': 'bg-danger',
            'Crítica': 'bg-dark',
        }
        return prioridade_classes.get(self.prioridade, 'bg-secondary')

    def get_setor_badge_class(self):
        """Retorna a classe CSS para o badge de setor"""
        setor_classes = {
            'Diretoria': 'bg-primary',
            'Inteligência': 'bg-info',
            'Faturamento': 'bg-success',
            'Expedição': 'bg-warning',
            'Configuração': 'bg-secondary',
            'Quality': 'bg-dark',
            'Área Técnica': 'bg-danger',
            'Comercial': 'bg-light text-dark',
        }
        return setor_classes.get(self.setor, 'bg-secondary')