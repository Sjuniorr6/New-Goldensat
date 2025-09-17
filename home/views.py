from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
import json

# Importar todos os modelos
from clientes.models import Clientes
from produtos.models import CadastroTipoProduto, EntradaProduto
from requisicoes.models import Requisicoes
from usuarios.models import Setor, PerfilUsuario
from django.contrib.auth.models import User

# Create your views here.
class HomeView(View):
    template_name = 'home/home.html'
    
    def get(self, request):
        return render(request, self.template_name)

class LoginView(View):
    template_name = 'home/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:home')
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home:home')
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
        
        return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home:login')

@login_required
@require_http_methods(["GET"])
def busca_global(request):
    """View para busca global no sistema"""
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({
            'success': False,
            'message': 'Digite pelo menos 2 caracteres para buscar'
        })
    
    resultados = {
        'clientes': [],
        'produtos': [],
        'requisicoes': [],
        'usuarios': [],
        'setores': []
    }
    
    try:
        # Buscar clientes
        clientes = Clientes.objects.filter(
            Q(nome__icontains=query) |
            Q(cnpj__icontains=query) |
            Q(endereco__icontains=query) |
            Q(telefone__icontains=query) |
            Q(email__icontains=query)
        )[:5]
        
        for cliente in clientes:
            resultados['clientes'].append({
                'id': cliente.id,
                'nome': cliente.nome,
                'cnpj': cliente.cnpj,
                'endereco': cliente.endereco,
                'tipo': 'Cliente',
                'url': f'/clientes/detalhes/{cliente.id}/'
            })
        
        # Buscar produtos
        produtos = CadastroTipoProduto.objects.filter(
            Q(descricao__icontains=query) |
            Q(codigo__icontains=query) |
            Q(categoria__icontains=query)
        )[:5]
        
        for produto in produtos:
            resultados['produtos'].append({
                'id': produto.id,
                'nome': produto.descricao,
                'codigo': produto.codigo,
                'categoria': produto.categoria,
                'tipo': 'Produto',
                'url': f'/produtos/detalhes/{produto.id}/'
            })
        
        # Buscar requisições
        requisicoes = Requisicoes.objects.filter(
            Q(id__icontains=query) |
            Q(nome__nome__icontains=query) |
            Q(tipo_produto__descricao__icontains=query) |
            Q(observacoes__icontains=query)
        ).select_related('nome', 'tipo_produto')[:5]
        
        for requisicao in requisicoes:
            resultados['requisicoes'].append({
                'id': requisicao.id,
                'nome': f"Requisição #{requisicao.id}",
                'cliente': requisicao.nome.nome if requisicao.nome else 'N/A',
                'produto': requisicao.tipo_produto.descricao if requisicao.tipo_produto else 'N/A',
                'status': requisicao.status,
                'tipo': 'Requisição',
                'url': f'/requisicoes/detail/{requisicao.id}/'
            })
        
        # Buscar usuários
        usuarios = User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )[:5]
        
        for usuario in usuarios:
            resultados['usuarios'].append({
                'id': usuario.id,
                'nome': usuario.get_full_name() or usuario.username,
                'username': usuario.username,
                'email': usuario.email,
                'tipo': 'Usuário',
                'url': f'/usuarios/detalhes/{usuario.id}/'
            })
        
        # Buscar setores
        setores = Setor.objects.filter(
            Q(nome__icontains=query) |
            Q(descricao__icontains=query)
        )[:5]
        
        for setor in setores:
            resultados['setores'].append({
                'id': setor.id,
                'nome': setor.nome,
                'descricao': setor.descricao,
                'tipo': 'Setor',
                'url': f'/usuarios/setores/detalhes/{setor.id}/'
            })
        
        # Contar total de resultados
        total_resultados = sum(len(resultados[key]) for key in resultados)
        
        return JsonResponse({
            'success': True,
            'query': query,
            'resultados': resultados,
            'total': total_resultados,
            'message': f'Encontrados {total_resultados} resultados para "{query}"'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro na busca: {str(e)}'
        })

@login_required
def pagina_busca(request):
    """Página de resultados da busca global"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return render(request, 'home/busca.html', {
            'query': '',
            'resultados': {},
            'total': 0
        })
    
    # Executar a mesma lógica da busca global
    resultados = {
        'clientes': [],
        'produtos': [],
        'requisicoes': [],
        'usuarios': [],
        'setores': []
    }
    
    try:
        # Buscar clientes
        clientes = Clientes.objects.filter(
            Q(nome__icontains=query) |
            Q(cnpj__icontains=query) |
            Q(endereco__icontains=query) |
            Q(telefone__icontains=query) |
            Q(email__icontains=query)
        )
        
        for cliente in clientes:
            resultados['clientes'].append({
                'id': cliente.id,
                'nome': cliente.nome,
                'cnpj': cliente.cnpj,
                'endereco': cliente.endereco,
                'tipo': 'Cliente',
                'url': f'/clientes/detalhes/{cliente.id}/'
            })
        
        # Buscar produtos
        produtos = CadastroTipoProduto.objects.filter(
            Q(descricao__icontains=query) |
            Q(codigo__icontains=query) |
            Q(categoria__icontains=query)
        )
        
        for produto in produtos:
            resultados['produtos'].append({
                'id': produto.id,
                'nome': produto.descricao,
                'codigo': produto.codigo,
                'categoria': produto.categoria,
                'tipo': 'Produto',
                'url': f'/produtos/detalhes/{produto.id}/'
            })
        
        # Buscar requisições
        requisicoes = Requisicoes.objects.filter(
            Q(id__icontains=query) |
            Q(nome__nome__icontains=query) |
            Q(tipo_produto__descricao__icontains=query) |
            Q(observacoes__icontains=query)
        ).select_related('nome', 'tipo_produto')
        
        for requisicao in requisicoes:
            resultados['requisicoes'].append({
                'id': requisicao.id,
                'nome': f"Requisição #{requisicao.id}",
                'cliente': requisicao.nome.nome if requisicao.nome else 'N/A',
                'produto': requisicao.tipo_produto.descricao if requisicao.tipo_produto else 'N/A',
                'status': requisicao.status,
                'tipo': 'Requisição',
                'url': f'/requisicoes/detail/{requisicao.id}/'
            })
        
        # Buscar usuários
        usuarios = User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )
        
        for usuario in usuarios:
            resultados['usuarios'].append({
                'id': usuario.id,
                'nome': usuario.get_full_name() or usuario.username,
                'username': usuario.username,
                'email': usuario.email,
                'tipo': 'Usuário',
                'url': f'/usuarios/detalhes/{usuario.id}/'
            })
        
        # Buscar setores
        setores = Setor.objects.filter(
            Q(nome__icontains=query) |
            Q(descricao__icontains=query)
        )
        
        for setor in setores:
            resultados['setores'].append({
                'id': setor.id,
                'nome': setor.nome,
                'descricao': setor.descricao,
                'tipo': 'Setor',
                'url': f'/usuarios/setores/detalhes/{setor.id}/'
            })
        
        # Contar total de resultados
        total_resultados = sum(len(resultados[key]) for key in resultados)
        
    except Exception as e:
        total_resultados = 0
    
    return render(request, 'home/busca.html', {
        'query': query,
        'resultados': resultados,
        'total': total_resultados
    })