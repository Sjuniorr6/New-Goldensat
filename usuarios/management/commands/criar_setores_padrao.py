from django.core.management.base import BaseCommand
from usuarios.models import Setor

class Command(BaseCommand):
    help = 'Cria os setores padrão do sistema'

    def handle(self, *args, **options):
        setores_padrao = [
            {
                'nome': 'configuracao',
                'descricao': 'Setor responsável pelas configurações gerais do sistema'
            },
            {
                'nome': 'expedicao',
                'descricao': 'Setor responsável pela expedição e logística'
            },
            {
                'nome': 'comercial',
                'descricao': 'Setor responsável pelas atividades comerciais'
            },
            {
                'nome': 'inteligencia',
                'descricao': 'Setor de inteligência e desenvolvimento'
            },
            {
                'nome': 'faturamento',
                'descricao': 'Setor responsável pelo faturamento e cobrança'
            },
            {
                'nome': 'ceo',
                'descricao': 'Diretoria executiva'
            },
            {
                'nome': 'tecnico',
                'descricao': 'Setor técnico e de manutenção'
            },
        ]

        for setor_data in setores_padrao:
            setor, created = Setor.objects.get_or_create(
                nome=setor_data['nome'],
                defaults={
                    'descricao': setor_data['descricao'],
                    'ativo': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Setor "{setor.get_nome_display()}" criado com sucesso!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Setor "{setor.get_nome_display()}" já existe.')
                )

        self.stdout.write(
            self.style.SUCCESS('Processo de criação de setores concluído!')
        )
