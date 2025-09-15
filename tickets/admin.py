from django.contrib import admin
from .models import TicketModel

@admin.register(TicketModel)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'titulo', 'usuario', 'setor', 'status', 
        'prioridade', 'data_criacao', 'responsavel'
    ]
    list_filter = [
        'status', 'setor', 'prioridade', 'data_criacao'
    ]
    search_fields = [
        'titulo', 'descricao_erro', 'usuario__username', 
        'usuario__first_name', 'usuario__last_name'
    ]
    readonly_fields = ['data_criacao', 'data_atualizacao']
    list_editable = ['status', 'prioridade', 'responsavel']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'setor', 'titulo', 'prioridade')
        }),
        ('Descrição do Problema', {
            'fields': ('descricao_erro',)
        }),
        ('Resolução', {
            'fields': ('status', 'responsavel', 'correcao', 'devolutiva', 'data_resolucao')
        }),
        ('Metadados', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Otimizar consultas"""
        return super().get_queryset(request).select_related('usuario', 'responsavel')