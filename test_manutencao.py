#!/usr/bin/env python
"""
Script para testar e estressar o sistema de manutenção
Cria múltiplas manutenções e testa alteração de status
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'int.settings')
django.setup()

from registro_manutencao.models import registrodemanutencao, ImagemRegistro, retorno
from clientes.models import Clientes
from produtos.models import CadastroTipoProduto
from django.contrib.auth.models import User

def criar_manutencoes_teste():
    """Cria múltiplas manutenções para testar o sistema"""
    
    print("🚀 Iniciando testes de estresse do sistema de manutenção...")
    
    # Verificar se existem clientes e produtos
    clientes = Clientes.objects.all()
    produtos = CadastroTipoProduto.objects.all()
    
    if not clientes.exists():
        print("❌ Nenhum cliente encontrado. Criando cliente de teste...")
        cliente_teste = Clientes.objects.create(
            nome_fantasia="Cliente Teste",
            razao_social="Cliente Teste LTDA",
            cnpj="12345678000199",
            email="teste@cliente.com"
        )
        clientes = [cliente_teste]
    else:
        clientes = list(clientes)
    
    if not produtos.exists():
        print("❌ Nenhum produto encontrado. Criando produto de teste...")
        produto_teste = CadastroTipoProduto.objects.create(
            nome_produto="GS410 (2G) - Teste",
            descricao="Produto de teste para manutenção"
        )
        produtos = [produto_teste]
    else:
        produtos = list(produtos)
    
    # Status possíveis
    status_options = [
        'Pendente',
        'Aprovado',
        'Reprovado pela Diretoria',
        'Aprovado pela Diretoria',
        'Expedição',
        'expedido'
    ]
    
    # Tipos de entrada
    tipos_entrada = [
        'Devolução / Estoque',
        'Garantia',
        'Manutenção Preventiva',
        'Manutenção Corretiva'
    ]
    
    # Motivos
    motivos = [
        'Defeito de Fábrica',
        'Desgaste Natural',
        'Danos por Uso',
        'Problema de Software',
        'Falha de Hardware'
    ]
    
    # Customizações
    customizacoes = [
        'Padrão',
        'Personalizada',
        'Especial',
        'Industrial'
    ]
    
    # Tipos de contrato
    tipos_contrato = [
        'Garantia',
        'Pós-Venda',
        'Contrato Anual',
        'Avulso'
    ]
    
    print(f"📊 Criando 20 manutenções de teste...")
    
    manutencoes_criadas = []
    
    for i in range(20):
        try:
            # Dados aleatórios
            cliente = random.choice(clientes)
            produto = random.choice(produtos)
            status = random.choice(status_options)
            tipo_entrada = random.choice(tipos_entrada)
            motivo = random.choice(motivos)
            customizacao = random.choice(customizacoes)
            tipo_contrato = random.choice(tipos_contrato)
            
            # Criar manutenção
            manutencao = registrodemanutencao.objects.create(
                nome=cliente,
                tipo_entrada=tipo_entrada,
                tipo_produto=produto,
                motivo=motivo,
                tipo_customizacao=customizacao,
                recebimento='Recebido',
                entregue_por_retirado_por='Cliente',
                id_equipamentos=f"ID{i+1:03d}, ID{i+2:03d}, ID{i+3:03d}",
                quantidade=random.randint(1, 10),
                tipo_contrato=tipo_contrato,
                customizacaoo=customizacao,
                numero_equipamento=f"EQ{i+1:04d}, EQ{i+2:04d}",
                observacoes=f"Observações de teste para manutenção {i+1}. Sistema funcionando corretamente.",
                tratativa='Análise Técnica',
                status=status,
                status_tratativa='Em Andamento',
                data_devolucao=datetime.now() + timedelta(days=random.randint(1, 30))
            )
            
            manutencoes_criadas.append(manutencao)
            print(f"✅ Manutenção {i+1} criada - ID: {manutencao.id} - Status: {status}")
            
        except Exception as e:
            print(f"❌ Erro ao criar manutenção {i+1}: {e}")
    
    print(f"\n🎉 {len(manutencoes_criadas)} manutenções criadas com sucesso!")
    return manutencoes_criadas

def testar_alteracao_status():
    """Testa a alteração de status das manutenções"""
    
    print("\n🔄 Testando alteração de status...")
    
    manutencoes = registrodemanutencao.objects.all()
    
    if not manutencoes.exists():
        print("❌ Nenhuma manutenção encontrada para testar.")
        return
    
    status_sequence = [
        'Pendente',
        'Aprovado',
        'Aprovado pela Diretoria',
        'Expedição',
        'expedido'
    ]
    
    print(f"📋 Testando alteração de status em {manutencoes.count()} manutenções...")
    
    for i, manutencao in enumerate(manutencoes[:10]):  # Testar apenas 10
        try:
            # Alterar status sequencialmente
            for status in status_sequence:
                manutencao.status = status
                manutencao.save()
                print(f"✅ Manutenção {manutencao.id}: Status alterado para '{status}'")
                
                # Simular delay
                import time
                time.sleep(0.1)
            
            print(f"🎯 Manutenção {manutencao.id} - Ciclo completo de status testado")
            
        except Exception as e:
            print(f"❌ Erro ao alterar status da manutenção {manutencao.id}: {e}")
    
    print("✅ Teste de alteração de status concluído!")

def testar_filtros():
    """Testa os filtros da lista de manutenções"""
    
    print("\n🔍 Testando filtros...")
    
    # Testar filtro por status
    status_teste = 'Pendente'
    manutencoes_pendentes = registrodemanutencao.objects.filter(status=status_teste)
    print(f"📊 Manutenções com status '{status_teste}': {manutencoes_pendentes.count()}")
    
    # Testar filtro por cliente
    if manutencoes_pendentes.exists():
        cliente_teste = manutencoes_pendentes.first().nome
        manutencoes_cliente = registrodemanutencao.objects.filter(nome=cliente_teste)
        print(f"📊 Manutenções do cliente '{cliente_teste.nome_fantasia}': {manutencoes_cliente.count()}")
    
    # Testar filtro por equipamento
    manutencoes_equipamento = registrodemanutencao.objects.filter(
        id_equipamentos__icontains='ID001'
    )
    print(f"📊 Manutenções com equipamento 'ID001': {manutencoes_equipamento.count()}")
    
    print("✅ Teste de filtros concluído!")

def testar_estatisticas():
    """Mostra estatísticas do sistema"""
    
    print("\n📈 Estatísticas do Sistema:")
    
    total_manutencoes = registrodemanutencao.objects.count()
    print(f"📊 Total de manutenções: {total_manutencoes}")
    
    # Estatísticas por status
    for status in ['Pendente', 'Aprovado', 'Aprovado pela Diretoria', 'Expedição', 'expedido']:
        count = registrodemanutencao.objects.filter(status=status).count()
        print(f"📊 Status '{status}': {count}")
    
    # Estatísticas por tipo de entrada
    tipos = registrodemanutencao.objects.values_list('tipo_entrada', flat=True).distinct()
    for tipo in tipos:
        count = registrodemanutencao.objects.filter(tipo_entrada=tipo).count()
        print(f"📊 Tipo '{tipo}': {count}")
    
    # Manutenções recentes
    recentes = registrodemanutencao.objects.order_by('-data_criacao')[:5]
    print(f"\n🕒 Últimas 5 manutenções:")
    for manutencao in recentes:
        print(f"   ID: {manutencao.id} - {manutencao.nome.nome_fantasia} - {manutencao.status} - {manutencao.data_criacao.strftime('%d/%m/%Y %H:%M')}")

def main():
    """Função principal para executar todos os testes"""
    
    print("🧪 SISTEMA DE TESTES DE MANUTENÇÃO")
    print("=" * 50)
    
    try:
        # 1. Criar manutenções de teste
        manutencoes = criar_manutencoes_teste()
        
        # 2. Testar alteração de status
        testar_alteracao_status()
        
        # 3. Testar filtros
        testar_filtros()
        
        # 4. Mostrar estatísticas
        testar_estatisticas()
        
        print("\n🎉 TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ ERRO DURANTE OS TESTES: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

