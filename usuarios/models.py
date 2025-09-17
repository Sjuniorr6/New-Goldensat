from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from PIL import Image
import os

class Setor(models.Model):
    """Modelo para definir os setores da empresa"""
    SETOR_CHOICES = [
        ('configuracao', 'Configuração'),
        ('expedicao', 'Expedição'),
        ('comercial', 'Comercial'),
        ('inteligencia', 'Inteligência'),
        ('faturamento', 'Faturamento'),
        ('ceo', 'CEO'),
        ('tecnico', 'Técnico'),
    ]
    
    nome = models.CharField(max_length=50, choices=SETOR_CHOICES, unique=True)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'
        ordering = ['nome']
    
    def __str__(self):
        return self.get_nome_display()

class PerfilUsuario(models.Model):
    """Modelo para estender informações do usuário"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True, blank=True)
    foto = models.ImageField(
        upload_to='usuarios/fotos/',
        default='usuarios/fotos/default.png',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        blank=True,
        null=True
    )
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    data_admissao = models.DateField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'
        ordering = ['user__first_name', 'user__last_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.setor.get_nome_display() if self.setor else 'Sem setor'}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Redimensionar foto se existir
        if self.foto:
            try:
                img = Image.open(self.foto.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.foto.path)
            except Exception as e:
                print(f"Erro ao redimensionar imagem: {e}")
    
    @property
    def nome_completo(self):
        return self.user.get_full_name() or self.user.username
    
    @property
    def email(self):
        return self.user.email
    
    @property
    def is_active(self):
        return self.user.is_active and self.ativo

class PermissaoSetor(models.Model):
    """Modelo para definir permissões específicas por setor"""
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='permissoes')
    nome_permissao = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Permissão de Setor'
        verbose_name_plural = 'Permissões de Setores'
        unique_together = ['setor', 'nome_permissao']
        ordering = ['setor', 'nome_permissao']
    
    def __str__(self):
        return f"{self.setor.get_nome_display()} - {self.nome_permissao}"
