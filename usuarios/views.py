from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .models import PerfilUsuario, Setor, PermissaoSetor
from .forms import (
    UsuarioForm, PerfilUsuarioForm, EditarUsuarioForm, 
    AlterarSenhaForm, SetorForm, PermissaoSetorForm, BuscarUsuarioForm
)

@login_required
def listar_usuarios(request):
    """Lista todos os usuários com filtros"""
    form_busca = BuscarUsuarioForm(request.GET)
    usuarios = User.objects.select_related('perfil__setor').all()
    
    if form_busca.is_valid():
        termo = form_busca.cleaned_data.get('termo')
        setor = form_busca.cleaned_data.get('setor')
        ativo = form_busca.cleaned_data.get('ativo')
        
        if termo:
            usuarios = usuarios.filter(
                Q(first_name__icontains=termo) |
                Q(last_name__icontains=termo) |
                Q(username__icontains=termo) |
                Q(email__icontains=termo) |
                Q(perfil__cargo__icontains=termo)
            )
        
        if setor:
            usuarios = usuarios.filter(perfil__setor=setor)
        
        if ativo == 'true':
            usuarios = usuarios.filter(is_active=True, perfil__ativo=True)
        elif ativo == 'false':
            usuarios = usuarios.filter(Q(is_active=False) | Q(perfil__ativo=False))
    
    # Paginação
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form_busca': form_busca,
        'setores': Setor.objects.filter(ativo=True),
    }
    return render(request, 'usuarios/listar_usuarios.html', context)

@login_required
def criar_usuario(request):
    """Cria um novo usuário"""
    if request.method == 'POST':
        form_usuario = UsuarioForm(request.POST)
        form_perfil = PerfilUsuarioForm(request.POST, request.FILES)
        
        if form_usuario.is_valid() and form_perfil.is_valid():
            user = form_usuario.save()
            perfil = form_perfil.save(commit=False)
            perfil.user = user
            perfil.save()
            
            messages.success(request, f'Usuário {user.get_full_name()} criado com sucesso!')
            return redirect('usuarios:listar_usuarios')
    else:
        form_usuario = UsuarioForm()
        form_perfil = PerfilUsuarioForm()
    
    context = {
        'form_usuario': form_usuario,
        'form_perfil': form_perfil,
    }
    return render(request, 'usuarios/criar_usuario.html', context)

@login_required
def editar_usuario(request, user_id):
    """Edita um usuário existente"""
    user = get_object_or_404(User, id=user_id)
    perfil, created = PerfilUsuario.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form_usuario = EditarUsuarioForm(request.POST, instance=user)
        form_perfil = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil)
        
        if form_usuario.is_valid() and form_perfil.is_valid():
            form_usuario.save()
            form_perfil.save()
            
            messages.success(request, f'Usuário {user.get_full_name()} atualizado com sucesso!')
            return redirect('usuarios:listar_usuarios')
    else:
        form_usuario = EditarUsuarioForm(instance=user)
        form_perfil = PerfilUsuarioForm(instance=perfil)
    
    context = {
        'form_usuario': form_usuario,
        'form_perfil': form_perfil,
        'usuario': user,
    }
    return render(request, 'usuarios/editar_usuario.html', context)

@login_required
def perfil_usuario(request):
    """Página de perfil do usuário logado"""
    user = request.user
    perfil, created = PerfilUsuario.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form_perfil = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil)
        if form_perfil.is_valid():
            form_perfil.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form_perfil = PerfilUsuarioForm(instance=perfil)
    
    context = {
        'perfil': perfil,
        'form_perfil': form_perfil,
    }
    return render(request, 'usuarios/perfil.html', context)

@login_required
def alterar_senha(request):
    """Altera a senha do usuário logado"""
    if request.method == 'POST':
        form = AlterarSenhaForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form = AlterarSenhaForm(user=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'usuarios/alterar_senha.html', context)

@login_required
def listar_setores(request):
    """Lista todos os setores"""
    setores = Setor.objects.all()
    
    context = {
        'setores': setores,
    }
    return render(request, 'usuarios/listar_setores.html', context)

@login_required
def criar_setor(request):
    """Cria um novo setor"""
    if request.method == 'POST':
        form = SetorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Setor criado com sucesso!')
            return redirect('usuarios:listar_setores')
    else:
        form = SetorForm()
    
    context = {
        'form': form,
    }
    return render(request, 'usuarios/criar_setor.html', context)

@login_required
def editar_setor(request, setor_id):
    """Edita um setor existente"""
    setor = get_object_or_404(Setor, id=setor_id)
    
    if request.method == 'POST':
        form = SetorForm(request.POST, instance=setor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Setor atualizado com sucesso!')
            return redirect('usuarios:listar_setores')
    else:
        form = SetorForm(instance=setor)
    
    context = {
        'form': form,
        'setor': setor,
    }
    return render(request, 'usuarios/editar_setor.html', context)

@login_required
def listar_permissoes(request):
    """Lista todas as permissões por setor"""
    permissoes = PermissaoSetor.objects.select_related('setor').all()
    
    context = {
        'permissoes': permissoes,
    }
    return render(request, 'usuarios/listar_permissoes.html', context)

@login_required
def criar_permissao(request):
    """Cria uma nova permissão"""
    if request.method == 'POST':
        form = PermissaoSetorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Permissão criada com sucesso!')
            return redirect('usuarios:listar_permissoes')
    else:
        form = PermissaoSetorForm()
    
    context = {
        'form': form,
    }
    return render(request, 'usuarios/criar_permissao.html', context)

@login_required
@require_http_methods(["DELETE"])
def excluir_usuario(request, user_id):
    """Exclui um usuário (soft delete)"""
    try:
        user = get_object_or_404(User, id=user_id)
        user.is_active = False
        user.save()
        
        if hasattr(user, 'perfil'):
            user.perfil.ativo = False
            user.perfil.save()
        
        return JsonResponse({'success': True, 'message': 'Usuário desativado com sucesso!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_http_methods(["POST"])
def ativar_usuario(request, user_id):
    """Ativa um usuário"""
    try:
        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save()
        
        if hasattr(user, 'perfil'):
            user.perfil.ativo = True
            user.perfil.save()
        
        return JsonResponse({'success': True, 'message': 'Usuário ativado com sucesso!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def detalhes_usuario(request, user_id):
    """Mostra detalhes de um usuário"""
    user = get_object_or_404(User, id=user_id)
    perfil, created = PerfilUsuario.objects.get_or_create(user=user)
    
    context = {
        'usuario': user,
        'perfil': perfil,
    }
    return render(request, 'usuarios/detalhes_usuario.html', context)
