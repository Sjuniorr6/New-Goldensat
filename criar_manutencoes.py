#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'int.settings')
django.setup()

from registro_manutencao.models import registrodemanutencao
from clientes.models import Clientes
from produtos.models import CadastroTipoProduto
from django.utils import timezone
from datetime import timedelta
import random

def criar_manutencoes():
    print("🚀 Criando manutenções de teste...")
    
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
    
    print("📊 Criando 10 manutenções de teste...")
    
    manutencoes_criadas = []
    
    for i in range(10):
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
                data_devolucao=timezone.now() + timedelta(days=random.randint(1, 30))
            )
            
            manutencoes_criadas.append(manutencao)
            print(f"✅ Manutenção {i+1} criada - ID: {manutencao.id} - Status: {status}")
            
        except Exception as e:
            print(f"❌ Erro ao criar manutenção {i+1}: {e}")
    
    print(f"🎉 {len(manutencoes_criadas)} manutenções criadas com sucesso!")
    
    # Mostrar estatísticas
    print("\n📈 Estatísticas do Sistema:")
    
    total_manutencoes = registrodemanutencao.objects.count()
    print(f"📊 Total de manutenções: {total_manutencoes}")
    
    # Estatísticas por status
    for status in ['Pendente', 'Aprovado', 'Aprovado pela Diretoria', 'Expedição', 'expedido']:
        count = registrodemanutencao.objects.filter(status=status).count()
        print(f"📊 Status '{status}': {count}")
    
    # Manutenções recentes
    recentes = registrodemanutencao.objects.order_by('-data_criacao')[:5]
    print(f"\n🕒 Últimas 5 manutenções:")
    for manutencao in recentes:
        print(f"   ID: {manutencao.id} - {manutencao.nome.nome_fantasia} - {manutencao.status} - {manutencao.data_criacao.strftime('%d/%m/%Y %H:%M')}")
    
    return manutencoes_criadas

if __name__ == "__main__":
    criar_manutencoes()
