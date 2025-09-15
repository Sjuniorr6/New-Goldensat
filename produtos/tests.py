from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import json
from datetime import datetime, timedelta

from .models import CadastroTipoProduto, EntradaProduto
from .forms import CadastroTipoProdutoForm, EntradaProdutoForm


class CadastroTipoProdutoModelTest(TestCase):
    """Testes para o modelo CadastroTipoProduto"""
    
    def setUp(self):
        self.produto = CadastroTipoProduto.objects.create(
            nome_produto="Cabo HDMI",
            descricao="Cabo HDMI 2 metros",
            fabricante="TechCorp",
            telefone_fabricante="11999999999",
            email_fabricante="contato@techcorp.com",
            valor_unitario=Decimal('25.50')
        )
    
    def test_criacao_produto(self):
        """Testa a criação de um produto"""
        self.assertEqual(self.produto.nome_produto, "Cabo HDMI")
        self.assertEqual(self.produto.fabricante, "TechCorp")
        self.assertEqual(self.produto.valor_unitario, Decimal('25.50'))
        self.assertIsNotNone(self.produto.data_cadastro)
    
    def test_str_representation(self):
        """Testa a representação string do modelo"""
        expected = "Cabo HDMI - TechCorp"
        self.assertEqual(str(self.produto), expected)
    
    def test_ordering(self):
        """Testa se os produtos são ordenados por data de cadastro decrescente"""
        produto2 = CadastroTipoProduto.objects.create(
            nome_produto="Adaptador USB",
            fabricante="USB Corp"
        )
        
        produtos = CadastroTipoProduto.objects.all()
        self.assertEqual(produtos[0], produto2)  # Mais recente primeiro
        self.assertEqual(produtos[1], self.produto)
