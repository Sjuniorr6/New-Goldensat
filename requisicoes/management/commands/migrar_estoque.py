from django.core.management.base import BaseCommand
from django.db import transaction
from produtos.models import CadastroTipoProduto, EntradaProduto, MovimentacaoEstoque
from requisicoes.models import Requisicoes
from produtos.logger_config import produtos_logger

class Command(BaseCommand):
    help = 'Migra dados existentes para o sistema de movimentações de estoque'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Executa sem fazer alterações no banco de dados',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 MODO DRY-RUN - Nenhuma alteração será feita'))
        
        try:
            with transaction.atomic():
                # 1. Migrar entradas de produtos existentes
                self.migrar_entradas_produtos(dry_run)
                
                # 2. Migrar requisições existentes
                self.migrar_requisicoes(dry_run)
                
                if dry_run:
                    # Em modo dry-run, faz rollback
                    raise Exception("Dry run - rollback")
                
                self.stdout.write(self.style.SUCCESS('✅ Migração concluída com sucesso!'))
                
        except Exception as e:
            if dry_run:
                self.stdout.write(self.style.SUCCESS('✅ Dry run concluído - nenhuma alteração foi feita'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ Erro na migração: {str(e)}'))
                raise

    def migrar_entradas_produtos(self, dry_run=False):
        """Migra entradas de produtos existentes para movimentações de estoque"""
        self.stdout.write('📦 Migrando entradas de produtos...')
        
        entradas = EntradaProduto.objects.all()
        total_entradas = entradas.count()
        
        for i, entrada in enumerate(entradas, 1):
            # Verificar se já existe movimentação para esta entrada
            if not MovimentacaoEstoque.objects.filter(
                produto=entrada.codigo_produto,
                referencia=f'ENTRADA_{entrada.id}'
            ).exists():
                
                if not dry_run:
                    MovimentacaoEstoque.objects.create(
                        produto=entrada.codigo_produto,
                        tipo='entrada',
                        quantidade=entrada.quantidade,
                        motivo=f'Entrada de produto - NF: {entrada.numero_nota_fiscal}',
                        referencia=f'ENTRADA_{entrada.id}'
                    )
                
                self.stdout.write(f'  ✅ Entrada {i}/{total_entradas}: {entrada.codigo_produto.nome_produto} - {entrada.quantidade} unidades')
            else:
                self.stdout.write(f'  ⏭️ Entrada {i}/{total_entradas}: Já migrada - {entrada.codigo_produto.nome_produto}')

    def migrar_requisicoes(self, dry_run=False):
        """Migra requisições existentes para movimentações de estoque"""
        self.stdout.write('📋 Migrando requisições...')
        
        # Buscar requisições que consomem estoque
        requisicoes = Requisicoes.objects.filter(
            tipo_produto__isnull=False,
            numero_de_equipamentos__isnull=False,
            status__in=['Pendente', 'Configurado', 'Aprovado pelo CEO']
        )
        
        total_requisicoes = requisicoes.count()
        
        for i, requisicao in enumerate(requisicoes, 1):
            try:
                quantidade = int(requisicao.numero_de_equipamentos or 0)
                if quantidade > 0:
                    # Verificar se já existe movimentação para esta requisição
                    if not MovimentacaoEstoque.objects.filter(
                        produto=requisicao.tipo_produto,
                        referencia=f'REQ_{requisicao.id}'
                    ).exists():
                        
                        if not dry_run:
                            MovimentacaoEstoque.objects.create(
                                produto=requisicao.tipo_produto,
                                tipo='saida',
                                quantidade=quantidade,
                                motivo=f'Requisição criada - ID: {requisicao.id}',
                                referencia=f'REQ_{requisicao.id}',
                                usuario=None  # Não temos usuário associado às requisições antigas
                            )
                        
                        self.stdout.write(f'  ✅ Requisição {i}/{total_requisicoes}: {requisicao.tipo_produto.nome_produto} - {quantidade} unidades')
                    else:
                        self.stdout.write(f'  ⏭️ Requisição {i}/{total_requisicoes}: Já migrada - {requisicao.tipo_produto.nome_produto}')
                        
            except (ValueError, TypeError) as e:
                self.stdout.write(f'  ⚠️ Requisição {i}/{total_requisicoes}: Erro ao processar quantidade - {str(e)}')
