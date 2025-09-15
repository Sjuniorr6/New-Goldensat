from django import forms
from .models import Requisicoes
from clientes.models import Clientes
from produtos.models import CadastroTipoProduto, EntradaProduto
from django.core.exceptions import ValidationError

class RequisicaoForm(forms.ModelForm):
    class Meta:
        model = Requisicoes
        fields = [
            'nome', 'endereco', 'contrato', 'cnpj', 'numero_de_equipamentos',
            'inicio_de_contrato', 'vigencia', 'tipo_customizacao', 'antenista',
            'envio', 'taxa_envio', 'comercial', 'tipo_produto', 'carregador',
            'motivo', 'cabo', 'tipo_fatura', 'valor_unitario', 'valor_total',
            'forma_pagamento', 'observacoes', 'aos_cuidados', 'TP',
            'id_equipamentos', 'faturamento', 'iccid'
        ]
        widgets = {
            'nome': forms.Select(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'contrato': forms.Select(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_de_equipamentos': forms.TextInput(attrs={'class': 'form-control'}),
            'inicio_de_contrato': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'vigencia': forms.Select(attrs={'class': 'form-control'}),
            'tipo_customizacao': forms.Select(attrs={'class': 'form-control'}),
            'antenista': forms.Select(attrs={'class': 'form-control'}),
            'envio': forms.Select(attrs={'class': 'form-control'}),
            'taxa_envio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'comercial': forms.Select(attrs={'class': 'form-control'}),
            'tipo_produto': forms.Select(attrs={'class': 'form-control'}),
            'carregador': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo': forms.Select(attrs={'class': 'form-control'}),
            'cabo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_fatura': forms.Select(attrs={'class': 'form-control'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'forma_pagamento': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'aos_cuidados': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'TP': forms.Select(attrs={'class': 'form-control'}),
            'id_equipamentos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'faturamento': forms.Select(attrs={'class': 'form-control'}),
            'iccid': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_produto'].queryset = CadastroTipoProduto.objects.all()
        self.fields['nome'].queryset = Clientes.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        tipo_produto = cleaned_data.get('tipo_produto')
        numero_equipamentos = cleaned_data.get('numero_de_equipamentos')
        
        if tipo_produto and numero_equipamentos:
            try:
                quantidade_solicitada = int(numero_equipamentos)
                
                # Usar o método do modelo para calcular estoque disponível
                estoque_disponivel = tipo_produto.get_estoque_disponivel()
                
                if quantidade_solicitada > estoque_disponivel:
                    raise ValidationError(
                        f'Estoque insuficiente! Disponível: {estoque_disponivel} unidades. '
                        f'Solicitado: {quantidade_solicitada} unidades.'
                    )
                    
            except (ValueError, TypeError):
                raise ValidationError('Número de equipamentos deve ser um valor numérico válido.')
        
        return cleaned_data
