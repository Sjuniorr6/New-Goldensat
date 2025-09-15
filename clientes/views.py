from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.db import models
import json
import traceback
from .models import Clientes
from .forms import ClienteForm
from produtos.logger_config import produtos_logger

class ListClientesView(ListView):
    model = Clientes
    template_name = 'clientes/listagem_clientes.html'
    context_object_name = 'object_list'
    paginate_by = 20
    
    def get(self, request, *args, **kwargs):
        produtos_logger.info("=" * 50)
        produtos_logger.info("GET - ListClientesView (Lista) iniciado")
        produtos_logger.info(f"GET - Request path: {request.path}")
        produtos_logger.info(f"GET - User: {request.user}")
        produtos_logger.info(f"GET - AJAX Request: {request.headers.get('X-Requested-With')}")
        
        try:
            response = super().get(request, *args, **kwargs)
            produtos_logger.info(f"GET - Lista de clientes carregada com {len(response.context_data['object_list'])} clientes")
            
            # Se for uma requisição AJAX, retornar apenas a tabela
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                produtos_logger.info("GET - Requisição AJAX detectada, retornando HTML da tabela")
                produtos_logger.info(f"GET - Context data keys: {list(response.context_data.keys())}")
                produtos_logger.info(f"GET - Object list count: {len(response.context_data.get('object_list', []))}")
                
                # Renderizar apenas a tabela para AJAX
                from django.template.loader import render_to_string
                html = render_to_string('clientes/tabela_clientes.html', response.context_data)
                produtos_logger.info(f"GET - HTML renderizado para AJAX: {len(html)} caracteres")
                produtos_logger.info("=" * 50)
                return HttpResponse(html)
            
            produtos_logger.info("=" * 50)
            return response
        except Exception as e:
            produtos_logger.error(f"GET - Erro ao carregar lista de clientes: {e}")
            produtos_logger.info("=" * 50)
            raise

@method_decorator(csrf_exempt, name='dispatch')
class ClienteModalView(CreateView):
    model = Clientes
    form_class = ClienteForm
    
    def post(self, request, *args, **kwargs):
        produtos_logger.info("=" * 50)
        produtos_logger.info("POST - ClienteModalView iniciado")
        produtos_logger.info(f"POST - Dados recebidos: {len(request.POST)} campos")
        
        try:
            form = self.form_class(request.POST)
            produtos_logger.info(f"POST - Formulário validado: {form.is_valid()}")
            if not form.is_valid():
                produtos_logger.warning(f"POST - Formulário inválido: {form.errors}")
            
            if form.is_valid():
                cliente = form.save()
                produtos_logger.info(f"POST - Cliente criado: ID {cliente.id}")
                produtos_logger.info(f"POST - Nome: {cliente.nome}")
                produtos_logger.info(f"POST - CNPJ: {cliente.cnpj}")
                produtos_logger.info("POST - Cliente salvo com sucesso")
                
                return JsonResponse({
                    'success': True,
                    'message': 'Cliente cadastrado com sucesso!',
                    'cliente': {
                        'id': cliente.id,
                        'nome': cliente.nome,
                        'nome_fantasia': cliente.nome_fantasia,
                        'cnpj': cliente.cnpj,
                        'status': cliente.status
                    }
                })
            else:
                produtos_logger.warning(f"POST - Formulário inválido: {form.errors}")
                return JsonResponse({
                    'success': False,
                    'message': 'Erro no formulário',
                    'errors': form.errors
                })
        except Exception as e:
            produtos_logger.error(f"POST - Erro na ClienteModalView: {e}")
            produtos_logger.error(f"POST - Tipo do erro: {type(e)}")
            produtos_logger.error(f"POST - Traceback: {traceback.format_exc()}")
            produtos_logger.info("=" * 50)
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            })

class DetailClienteView(DetailView):
    model = Clientes
    
    def get(self, request, *args, **kwargs):
        produtos_logger.info("=" * 50)
        produtos_logger.info("GET - DetailClienteView iniciado")
        produtos_logger.info(f"GET - Request path: {request.path}")
        produtos_logger.info(f"GET - Cliente ID solicitado: {kwargs.get('pk')}")
        
        try:
            self.object = self.get_object()
            produtos_logger.info(f"GET - Cliente encontrado: ID {self.object.id}")
            produtos_logger.info(f"GET - Nome: {self.object.nome}")
            produtos_logger.info(f"GET - CNPJ: {self.object.cnpj}")
            produtos_logger.info(f"GET - Status: {self.object.status}")
            
            response_data = {
                'id': self.object.id,
                'nome': self.object.nome,
                'nome_fantasia': self.object.nome_fantasia,
                'endereco': self.object.endereco,
                'cnpj': self.object.cnpj,
                'comercial': self.object.comercial,
                'tipo_contrato': self.object.tipo_contrato,
                'inicio_de_contrato': self.object.inicio_de_contrato.strftime('%Y-%m-%d') if self.object.inicio_de_contrato else None,
                'quantidade_em_contrato': self.object.quantidade_em_contrato,
                'vigencia': self.object.vigencia,
                'status': self.object.status,
                'termino': self.object.termino,
                'equipamento': self.object.equipamento,
                'quantidade': self.object.quantidade,
                'gr': self.object.gr,
                'corretora': self.object.corretora,
                'seguradora': self.object.seguradora,
                'data_treinamento': self.object.data_treinamento.strftime('%Y-%m-%d') if self.object.data_treinamento else None
            }
            
            produtos_logger.info(f"GET - Response preparada com sucesso")
            produtos_logger.info("=" * 50)
            
            return JsonResponse(response_data)
            
        except Exception as e:
            produtos_logger.error(f"GET - Erro geral na view: {e}")
            produtos_logger.error(f"GET - Tipo do erro: {type(e)}")
            produtos_logger.error(f"GET - Traceback: {traceback.format_exc()}")
            produtos_logger.info("=" * 50)
            
            return JsonResponse({
                'error': True,
                'message': f'Erro ao carregar detalhes: {str(e)}',
                'debug_info': {
                    'error_type': str(type(e)),
                    'error_message': str(e)
                }
            }, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateClienteView(UpdateView):
    model = Clientes
    form_class = ClienteForm
    
    def post(self, request, *args, **kwargs):
        produtos_logger.info("=" * 50)
        produtos_logger.info("POST - UpdateClienteView iniciado")
        produtos_logger.info(f"POST - Cliente ID: {kwargs.get('pk')}")
        
        try:
            self.object = self.get_object()
            form = self.form_class(request.POST, instance=self.object)
            
            if form.is_valid():
                cliente = form.save()
                produtos_logger.info(f"POST - Cliente atualizado: ID {cliente.id}")
                produtos_logger.info(f"POST - Nome: {cliente.nome}")
                
                return JsonResponse({
                    'success': True,
                    'message': 'Cliente atualizado com sucesso!',
                    'cliente': {
                        'id': cliente.id,
                        'nome': cliente.nome,
                        'nome_fantasia': cliente.nome_fantasia,
                        'cnpj': cliente.cnpj,
                        'status': cliente.status
                    }
                })
            else:
                produtos_logger.warning(f"POST - Formulário inválido: {form.errors}")
                return JsonResponse({
                    'success': False,
                    'message': 'Erro no formulário',
                    'errors': form.errors
                })
        except Exception as e:
            produtos_logger.error(f"POST - Erro na UpdateClienteView: {e}")
            produtos_logger.error(f"POST - Traceback: {traceback.format_exc()}")
            produtos_logger.info("=" * 50)
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            })

class DeleteClienteView(DeleteView):
    model = Clientes
    success_url = reverse_lazy('listagem_clientes')
    
    def delete(self, request, *args, **kwargs):
        produtos_logger.info("=" * 50)
        produtos_logger.info(f"DELETE - Request recebido para cliente {kwargs.get('pk')}")
        produtos_logger.info(f"DELETE - Method: {request.method}")
        
        try:
            self.object = self.get_object()
            produtos_logger.info(f"DELETE - Cliente encontrado: ID {self.object.id}")
            produtos_logger.info(f"DELETE - Nome: {self.object.nome}")
            produtos_logger.info(f"DELETE - CNPJ: {self.object.cnpj}")
            
            cliente_info = f"{self.object.nome} - CNPJ: {self.object.cnpj}"
            
            self.object.delete()
            produtos_logger.info("DELETE - Cliente deletado com sucesso")
            
            mensagem = f'Cliente "{cliente_info}" excluído com sucesso!'
            
            response_data = {
                'success': True,
                'message': mensagem
            }
            
            produtos_logger.info(f"DELETE - Response preparada com sucesso")
            produtos_logger.info("=" * 50)
            return JsonResponse(response_data)
            
        except Exception as e:
            produtos_logger.error(f"DELETE - Erro ao excluir cliente: {str(e)}")
            produtos_logger.error(f"DELETE - Tipo do erro: {type(e)}")
            produtos_logger.error(f"DELETE - Traceback: {traceback.format_exc()}")
            produtos_logger.info("=" * 50)
            return JsonResponse({
                'success': False,
                'message': f'Erro ao excluir cliente: {str(e)}'
            })

class ApiClientesView(View):
    """API para listar todos os clientes cadastrados"""
    
    def get(self, request):
        produtos_logger.info("=" * 50)
        produtos_logger.info("GET - ApiClientesView iniciado")
        produtos_logger.info(f"GET - Request path: {request.path}")
        
        try:
            # Buscar todos os clientes
            clientes = Clientes.objects.all().order_by('nome')
            produtos_logger.info(f"GET - {clientes.count()} clientes encontrados")
            
            # Preparar dados para JSON
            clientes_data = []
            for cliente in clientes:
                clientes_data.append({
                    'id': cliente.id,
                    'cliente': cliente.nome,
                    'nome_fantasia': cliente.nome_fantasia,
                    'cnpj': cliente.cnpj,
                    'status': cliente.status
                })
            
            response_data = {
                'success': True,
                'clientes': clientes_data,
                'total': len(clientes_data)
            }
            
            produtos_logger.info(f"GET - Response preparada com {len(clientes_data)} clientes")
            produtos_logger.info("=" * 50)
            
            return JsonResponse(response_data)
            
        except Exception as e:
            produtos_logger.error(f"GET - Erro na ApiClientesView: {e}")
            produtos_logger.error(f"GET - Traceback: {traceback.format_exc()}")
            produtos_logger.info("=" * 50)
            
            return JsonResponse({
                'success': False,
                'message': f'Erro ao carregar clientes: {str(e)}',
                'clientes': []
            }, status=500)
