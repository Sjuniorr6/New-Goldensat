from django import forms
from .models import registrodemanutencao, ImagemRegistro, retorno
from clientes.models import Clientes
from produtos.models import CadastroTipoProduto


class RegistroManutencaoForm(forms.ModelForm):
    """Formulário para registro de manutenção"""
    
    class Meta:
        model = registrodemanutencao
        fields = '__all__'
        widgets = {
            'nome': forms.Select(attrs={'class': 'form-control'}),
            'tipo_entrada': forms.Select(attrs={'class': 'form-control'}),
            'tipo_produto': forms.Select(attrs={'class': 'form-control'}),
            'motivo': forms.Select(attrs={'class': 'form-control'}),
            'tipo_customizacao': forms.Select(attrs={'class': 'form-control'}),
            'recebimento': forms.Select(attrs={'class': 'form-control'}),
            'entregue_por_retirado_por': forms.Select(attrs={'class': 'form-control'}),
            'id_equipamentos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'tipo_contrato': forms.Select(attrs={'class': 'form-control'}),
            'customizacaoo': forms.Select(attrs={'class': 'form-control'}),
            'numero_equipamento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tratativa': forms.Select(attrs={'class': 'form-control'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imagem2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'status_tratativa': forms.Select(attrs={'class': 'form-control'}),
            'data_devolucao': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        labels = {
            'nome': 'Cliente',
            'tipo_entrada': 'Tipo de Entrada',
            'tipo_produto': 'Tipo de Produto',
            'motivo': 'Motivo',
            'tipo_customizacao': 'Tipo de Customização',
            'recebimento': 'Recebimento',
            'entregue_por_retirado_por': 'Entregue/Retirado Por',
            'id_equipamentos': 'IDs dos Equipamentos',
            'quantidade': 'Quantidade',
            'tipo_contrato': 'Tipo de Contrato',
            'customizacaoo': 'Customização',
            'numero_equipamento': 'Número do Equipamento',
            'observacoes': 'Observações',
            'tratativa': 'Tratativa',
            'imagem': 'Imagem 1',
            'imagem2': 'Imagem 2',
            'status': 'Status',
            'status_tratativa': 'Status da Tratativa',
            'data_devolucao': 'Data de Devolução',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].queryset = Clientes.objects.all().order_by('nome_fantasia')
        self.fields['tipo_produto'].queryset = CadastroTipoProduto.objects.all().order_by('nome_produto')
        self.fields['status'].required = False
        self.fields['status_tratativa'].required = False
        self.fields['data_devolucao'].required = False
        self.fields['quantidade'].initial = 0


class ImagemRegistroForm(forms.ModelForm):
    """Formulário para imagens de registro"""
    
    class Meta:
        model = ImagemRegistro
        fields = [
            'registro', 'tipo_problema', 'imagem', 'imagem2', 'id_equipamento',
            'faturamento', 'observacao2'
        ]
        widgets = {
            'registro': forms.Select(attrs={'class': 'form-control'}),
            'tipo_problema': forms.Select(attrs={'class': 'form-control'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'imagem2': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'id_equipamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID do equipamento'}),
            'faturamento': forms.Select(attrs={'class': 'form-control'}),
            'observacao2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Observação'}),
        }
        labels = {
            'registro': 'Registro',
            'tipo_problema': 'Tipo de Problema',
            'imagem': 'Imagem 1',
            'imagem2': 'Imagem 2',
            'id_equipamento': 'ID do Equipamento',
            'faturamento': 'Faturamento',
            'observacao2': 'Observação',
        }


class RetornoForm(forms.ModelForm):
    """Formulário para retorno"""
    
    class Meta:
        model = retorno
        fields = [
            'cliente', 'produto', 'tipo_problema', 'imagem', 'id_equipamentos'
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'tipo_problema': forms.Select(attrs={'class': 'form-control'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'id_equipamentos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'IDs dos equipamentos separados por vírgula'}),
        }
        labels = {
            'cliente': 'Cliente',
            'produto': 'Produto',
            'tipo_problema': 'Tipo de Problema',
            'imagem': 'Imagem',
            'id_equipamentos': 'IDs dos Equipamentos',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Clientes.objects.all()
        self.fields['produto'].queryset = CadastroTipoProduto.objects.all()


class FiltroManutencaoForm(forms.Form):
    """Formulário para filtrar registros de manutenção"""
    
    # Campos de busca como na imagem
    buscar_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por ID'
        })
    )
    
    buscar_nome = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por Nome'
        })
    )
    
    buscar_equipamento = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por Equipamento'
        })
    )
    
    status = forms.ChoiceField(
        choices=[
            ('', 'Selecione o Status'),
            ('Pendente', 'Pendente'),
            ('Aprovado', 'Aprovado'),
            ('Reprovado pela Diretoria', 'Reprovado pela Diretoria'),
            ('Aprovado pela Diretoria', 'Aprovado pela Diretoria'),
            ('Expedição', 'Expedição'),
            ('expedido', 'Expedido'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar classes CSS para campos
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'attrs'):
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'