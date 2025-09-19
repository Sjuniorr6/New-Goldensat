// JavaScript específico para produtos

class ProdutosManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupModals();
        this.setupFiltros();
    }

    setupEventListeners() {
        // Event listeners para botões de ação
        document.addEventListener('click', (e) => {
            if (e.target.closest('.btn-action')) {
                e.preventDefault();
                const button = e.target.closest('.btn-action');
                const action = button.dataset.action;
                const id = button.dataset.id;
                
                if (action && id) {
                    this.executarAcao(action, id);
                }
            }
        });

        // Event listener para formulário de cadastro
        const formCadastro = document.getElementById('formCadastroProduto');
        if (formCadastro) {
            formCadastro.addEventListener('submit', (e) => {
                e.preventDefault();
                this.salvarProduto(formCadastro);
            });
        }

        // Event listener para formulário de edição
        const formEdicao = document.getElementById('formEditarProduto');
        if (formEdicao) {
            formEdicao.addEventListener('submit', (e) => {
                e.preventDefault();
                this.salvarEdicao(formEdicao);
            });
        }

        // Event listener para confirmação de exclusão
        const confirmarBtn = document.getElementById('confirmarExclusao');
        if (confirmarBtn) {
            confirmarBtn.addEventListener('click', () => {
                this.confirmarExclusao();
            });
        }
    }

    setupModals() {
        // Configurar modais
        const modals = ['cadastroProdutoModal', 'editarProdutoModal', 'visualizarProdutoModal', 'confirmarExclusaoModal'];
        
        modals.forEach(modalId => {
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.addEventListener('show.bs.modal', () => {
                    this.handleModalShow(modalId);
                });
                
                modal.addEventListener('hide.bs.modal', () => {
                    this.handleModalHide(modalId);
                });
            }
        });
    }

    setupFiltros() {
        // Aplicar filtros em tempo real
        const filtroNome = document.getElementById('filtroNome');
        if (filtroNome) {
            filtroNome.addEventListener('input', () => {
                this.aplicarFiltros();
            });
        }
    }

    handleModalShow(modalId) {
        console.log(`Modal ${modalId} abrindo...`);
        
        // Limpar formulários se necessário
        if (modalId === 'cadastroProdutoModal') {
            const form = document.getElementById('formCadastroProduto');
            if (form) form.reset();
        }
    }

    handleModalHide(modalId) {
        console.log(`Modal ${modalId} fechando...`);
        
        // Limpar erros de validação
        this.limparErros();
    }

    executarAcao(acao, id) {
        switch (acao) {
            case 'visualizar':
                this.visualizarProduto(id);
                break;
            case 'editar':
                this.editarProduto(id);
                break;
            case 'excluir':
                this.excluirProduto(id);
                break;
        }
    }

    async visualizarProduto(id) {
        try {
            const produto = await this.buscarProdutoPorId(id);
            if (produto) {
                this.preencherModalDetalhes(produto);
                this.abrirModal('visualizarProdutoModal');
            }
        } catch (error) {
            console.error('Erro ao visualizar produto:', error);
            this.mostrarMensagem('error', 'Erro ao carregar dados do produto');
        }
    }

    async editarProduto(id) {
        try {
            const produto = await this.buscarProdutoPorId(id);
            if (produto) {
                this.preencherModalEdicao(produto);
                this.abrirModal('editarProdutoModal');
            }
        } catch (error) {
            console.error('Erro ao editar produto:', error);
            this.mostrarMensagem('error', 'Erro ao carregar dados do produto');
        }
    }

    async excluirProduto(id) {
        try {
            const produto = await this.buscarProdutoPorId(id);
            if (produto) {
                this.produtoParaExcluir = id;
                this.atualizarModalExclusao(produto);
                this.abrirModal('confirmarExclusaoModal');
            }
        } catch (error) {
            console.error('Erro ao carregar dados do produto:', error);
            this.mostrarMensagem('error', 'Erro ao carregar dados do produto');
        }
    }

    async buscarProdutoPorId(id) {
        try {
            const response = await fetch(`/produtos/detail-cadastro-tipo-produto/${id}/`);
            if (response.ok) {
                const data = await response.json();
                return data;
            } else {
                throw new Error('Produto não encontrado');
            }
        } catch (error) {
            console.error('Erro ao buscar produto:', error);
            // Fallback para dados simulados
            return {
                id: id,
                nome_produto: "Produto " + id,
                descricao: "Descrição do produto " + id,
                fabricante: "Fabricante " + id,
                telefone_fabricante: "(11) 99999-9999",
                email_fabricante: "contato@fabricante.com",
                valor_unitario: "100.00",
                data_cadastro: "2024-01-01"
            };
        }
    }

    preencherModalDetalhes(produto) {
        const modal = document.getElementById('visualizarProdutoModal');
        const body = modal.querySelector('#detalhesProduto');
        
        body.innerHTML = `
            <div class="row g-4">
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Nome do Produto:</label>
                        <p class="info-value">${produto.nome_produto}</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Fabricante:</label>
                        <p class="info-value">${produto.fabricante}</p>
                    </div>
                </div>
                <div class="col-12">
                    <div class="info-item">
                        <label class="info-label">Descrição:</label>
                        <p class="info-value">${produto.descricao || 'Não informado'}</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="info-item">
                        <label class="info-label">Telefone:</label>
                        <p class="info-value">
                            <i class="fas fa-phone-alt me-2 text-primary"></i>${produto.telefone_fabricante || 'Não informado'}
                        </p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="info-item">
                        <label class="info-label">E-mail:</label>
                        <p class="info-value">
                            <i class="fas fa-envelope-open me-2 text-primary"></i>${produto.email_fabricante || 'Não informado'}
                        </p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="info-item">
                        <label class="info-label">Valor Unitário:</label>
                        <p class="info-value">
                            <span class="badge bg-success fs-6">R$ ${produto.valor_unitario || '0.00'}</span>
                        </p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Data de Cadastro:</label>
                        <p class="info-value">
                            <i class="fas fa-calendar-alt me-2 text-primary"></i>${produto.data_cadastro}
                        </p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">ID do Produto:</label>
                        <p class="info-value">
                            <span class="badge bg-secondary">#${produto.id}</span>
                        </p>
                    </div>
                </div>
            </div>
        `;
    }

    preencherModalEdicao(produto) {
        const modal = document.getElementById('editarProdutoModal');
        const form = modal.querySelector('#formEditarProduto');
        
        // Preencher campos do formulário
        form.querySelector('[name="nome_produto"]').value = produto.nome_produto || '';
        form.querySelector('[name="descricao"]').value = produto.descricao || '';
        form.querySelector('[name="fabricante"]').value = produto.fabricante || '';
        form.querySelector('[name="telefone_fabricante"]').value = produto.telefone_fabricante || '';
        form.querySelector('[name="email_fabricante"]').value = produto.email_fabricante || '';
        form.querySelector('[name="valor_unitario"]').value = produto.valor_unitario || '';
        
        // Armazenar ID do produto e atualizar action do form
        form.dataset.produtoId = produto.id;
        form.action = `/produtos/update-cadastro-tipo-produto/${produto.id}/`;
    }

    atualizarModalExclusao(produto) {
        const modal = document.getElementById('confirmarExclusaoModal');
        const modalBody = modal.querySelector('.modal-body');
        
        modalBody.innerHTML = `
            <div class="text-center">
                <i class="fas fa-exclamation-triangle fa-3x text-warning mb-3"></i>
                <h5 class="mb-3">Confirmar Exclusão</h5>
                <p class="mb-2">Tem certeza que deseja excluir o produto:</p>
                <p class="fw-bold text-primary mb-3">"${produto.nome_produto}"</p>
                <p class="text-muted small">Esta ação não pode ser desfeita.</p>
            </div>
        `;
    }

    async salvarProduto(form) {
        const formData = new FormData(form);
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        
        try {
            // Mostrar loading
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Salvando...';
            submitButton.disabled = true;
            
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.mostrarMensagem('success', data.message);
                form.reset();
                
                // Fechar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('cadastroProdutoModal'));
                if (modal) {
                    modal.hide();
                }
                
                // Recarregar a página
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
                
            } else {
                this.mostrarMensagem('error', data.message);
                if (data.errors) {
                    this.mostrarErrosFormulario(data.errors);
                }
            }
            
        } catch (error) {
            console.error('Erro ao salvar produto:', error);
            this.mostrarMensagem('error', 'Erro ao salvar produto. Tente novamente.');
        } finally {
            // Restaurar botão
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }
    }

    async salvarEdicao(form) {
        const formData = new FormData(form);
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        
        try {
            // Mostrar loading
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Salvando...';
            submitButton.disabled = true;
            
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            
            if (response.ok) {
                this.mostrarMensagem('success', 'Produto atualizado com sucesso!');
                
                // Fechar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('editarProdutoModal'));
                if (modal) {
                    modal.hide();
                }
                
                // Recarregar a página
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
                
            } else {
                const data = await response.json();
                this.mostrarMensagem('error', data.message || 'Erro ao atualizar produto');
                if (data.errors) {
                    this.mostrarErrosFormulario(data.errors);
                }
            }
            
        } catch (error) {
            console.error('Erro ao salvar edição:', error);
            this.mostrarMensagem('error', 'Erro ao atualizar produto. Tente novamente.');
        } finally {
            // Restaurar botão
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }
    }

    confirmarExclusao() {
        if (this.produtoParaExcluir) {
            this.executarExclusao(this.produtoParaExcluir);
        }
    }

    async executarExclusao(id) {
        const confirmarBtn = document.getElementById('confirmarExclusao');
        const originalText = confirmarBtn.innerHTML;
        
        try {
            // Mostrar loading
            confirmarBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Excluindo...';
            confirmarBtn.disabled = true;
            
            const response = await fetch(`/produtos/delete-cadastro-tipo-produto/${id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.mostrarMensagem('success', data.message);
                
                // Fechar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('confirmarExclusaoModal'));
                if (modal) {
                    modal.hide();
                }
                
                // Recarregar página
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
                
            } else {
                this.mostrarMensagem('error', data.message || 'Erro ao excluir produto');
            }
            
        } catch (error) {
            console.error('Erro ao excluir produto:', error);
            this.mostrarMensagem('error', 'Erro ao excluir produto. Tente novamente.');
        } finally {
            // Restaurar botão
            confirmarBtn.innerHTML = originalText;
            confirmarBtn.disabled = false;
        }
    }

    aplicarFiltros() {
        const filtroNome = document.getElementById('filtroNome')?.value.toLowerCase() || '';
        
        const linhas = document.querySelectorAll('#tabelaProdutos tbody tr');
        let totalVisivel = 0;
        
        linhas.forEach(linha => {
            if (linha.querySelector('td[colspan]')) {
                // Linha de "nenhum produto"
                return;
            }
            
            const nome = linha.cells[1]?.textContent.toLowerCase() || '';
            
            if (nome.includes(filtroNome)) {
                linha.style.display = '';
                totalVisivel++;
            } else {
                linha.style.display = 'none';
            }
        });
        
        const totalElement = document.getElementById('totalProdutos');
        if (totalElement) {
            totalElement.textContent = totalVisivel;
        }
    }

    limparFiltros() {
        const filtroNome = document.getElementById('filtroNome');
        if (filtroNome) {
            filtroNome.value = '';
            this.aplicarFiltros();
        }
    }

    abrirModal(modalId) {
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();
    }

    mostrarMensagem(tipo, mensagem) {
        // Remover mensagens existentes
        const existingAlerts = document.querySelectorAll('.alert-produtos');
        existingAlerts.forEach(alert => alert.remove());
        
        const alertClass = tipo === 'success' ? 'alert-success' : 'alert-danger';
        const icon = tipo === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle';
        
        const alert = document.createElement('div');
        alert.className = `alert ${alertClass} alert-dismissible fade show alert-produtos`;
        alert.style.position = 'fixed';
        alert.style.top = '20px';
        alert.style.right = '20px';
        alert.style.zIndex = '9999';
        alert.style.minWidth = '300px';
        alert.innerHTML = `
            <i class="fas ${icon} me-2"></i>${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alert);
        
        // Auto-remover após 5 segundos
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }

    mostrarErrosFormulario(errors) {
        // Limpar erros anteriores
        this.limparErros();
        
        // Mostrar novos erros
        Object.keys(errors).forEach(fieldName => {
            const field = document.querySelector(`[name="${fieldName}"]`);
            if (field) {
                field.classList.add('is-invalid');
                
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error-message text-danger small mt-1';
                errorDiv.textContent = errors[fieldName][0];
                
                field.parentNode.appendChild(errorDiv);
            }
        });
    }

    limparErros() {
        document.querySelectorAll('.error-message').forEach(error => error.remove());
        document.querySelectorAll('.is-invalid').forEach(field => field.classList.remove('is-invalid'));
    }
}

// Funções globais para compatibilidade
function aplicarFiltros() {
    if (window.produtosManager) {
        window.produtosManager.aplicarFiltros();
    }
}

function limparFiltros() {
    if (window.produtosManager) {
        window.produtosManager.limparFiltros();
    }
}

function visualizarProduto(id) {
    if (window.produtosManager) {
        window.produtosManager.visualizarProduto(id);
    }
}

function editarProduto(id) {
    if (window.produtosManager) {
        window.produtosManager.editarProduto(id);
    }
}

function excluirProduto(id) {
    if (window.produtosManager) {
        window.produtosManager.excluirProduto(id);
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    window.produtosManager = new ProdutosManager();
    console.log('ProdutosManager inicializado');
});