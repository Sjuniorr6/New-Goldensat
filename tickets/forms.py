from django import forms
from django.contrib.auth.models import User
from .models import TicketModel

class TicketForm(forms.ModelForm):
    class Meta:
        model = TicketModel
        fields = [
            'setor', 'titulo', 'descricao_erro', 'prioridade'
        ]
        widgets = {
            'setor': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite um título descritivo para o ticket',
                'required': True
            }),
            'descricao_erro': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva detalhadamente o problema encontrado...',
                'required': True
            }),
            'prioridade': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Adicionar classes CSS aos labels
        for field_name, field in self.fields.items():
            field.label = field.label or field_name.replace('_', ' ').title()

class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = TicketModel
        fields = [
            'status', 'correcao', 'devolutiva', 'responsavel'
        ]
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'correcao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva a correção aplicada...'
            }),
            'devolutiva': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Adicione uma devolutiva para o usuário...'
            }),
            'responsavel': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar usuários que podem ser responsáveis (staff)
        self.fields['responsavel'].queryset = User.objects.filter(is_staff=True)
        
        # Adicionar classes CSS aos labels
        for field_name, field in self.fields.items():
            field.label = field.label or field_name.replace('_', ' ').title()
