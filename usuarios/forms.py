from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import PerfilUsuario, Setor, PermissaoSetor

class UsuarioForm(UserCreationForm):
    """Formulário para criação de usuários"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Digite o email'
    }))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Digite o nome'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Digite o sobrenome'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome de usuário'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Digite a senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme a senha'})

class PerfilUsuarioForm(forms.ModelForm):
    """Formulário para perfil do usuário"""
    class Meta:
        model = PerfilUsuario
        fields = ['setor', 'foto', 'telefone', 'cargo', 'data_admissao', 'ativo']
        widgets = {
            'setor': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o telefone'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o cargo'}),
            'data_admissao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EditarUsuarioForm(forms.ModelForm):
    """Formulário para edição de dados do usuário"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AlterarSenhaForm(PasswordChangeForm):
    """Formulário para alteração de senha"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

class SetorForm(forms.ModelForm):
    """Formulário para criação/edição de setores"""
    class Meta:
        model = Setor
        fields = ['nome', 'descricao', 'ativo']
        widgets = {
            'nome': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PermissaoSetorForm(forms.ModelForm):
    """Formulário para criação/edição de permissões de setor"""
    class Meta:
        model = PermissaoSetor
        fields = ['setor', 'nome_permissao', 'descricao', 'ativo']
        widgets = {
            'setor': forms.Select(attrs={'class': 'form-control'}),
            'nome_permissao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da permissão'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Digite a descrição da permissão'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BuscarUsuarioForm(forms.Form):
    """Formulário para busca de usuários"""
    termo = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome, email ou setor...'
        })
    )
    setor = forms.ModelChoiceField(
        queryset=Setor.objects.filter(ativo=True),
        required=False,
        empty_label="Todos os setores",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    ativo = forms.ChoiceField(
        choices=[('', 'Todos'), ('true', 'Ativos'), ('false', 'Inativos')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
