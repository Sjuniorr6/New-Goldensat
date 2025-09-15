# acompanhamento/forms.py
from django import forms
from .models import Clientes

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes

        fields = ['nome', 'nome_fantasia','quantidade_em_contrato','endereco', 'cnpj','comercial','tipo_contrato','inicio_de_contrato','vigencia','termino','status','equipamento','quantidade','gr','corretora','seguradora','data_treinamento']

       

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'comercial': forms.TextInput(attrs={'class': 'form-control'}),
            'inicio_de_contrato': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade_em_contrato': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_contrato': forms.Select(attrs={'class': 'form-control'}),
            'vigencia': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'termino': forms.Textarea(attrs={'class' : 'form-control', 'rows':1}),
            'equipamento': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.Textarea(attrs={'class' : 'form-control', 'rows':1}),
            'gr': forms.Textarea(attrs={'class' : 'form-control', 'rows':1}),
            'corretora': forms.Textarea(attrs={'class' : 'form-control', 'rows':1}),
            'seguradora': forms.Textarea(attrs={'class' : 'form-control', 'rows':1}),
            'data_treinamento': forms.TextInput(attrs={'class': 'form-control'}),
        }
