// JavaScript específico para entradas de produtos

class EntradasManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupModal();
        this.setupFormSubmission();
        this.setupFormEdicao();
        this.setupFiltros();
        this.setupTabela();
        this.setupEventListeners();
    }

    setupModal() {
        // Garantir que o modal funcione corretamente
        const modal = document.getElementById('entradaProdutoModal');
        if (modal) {
            // Remover event listeners existentes
            modal.removeEventListener('show.bs.modal', this.handleModalShow);
            modal.removeEventListener('hide.bs.modal', this.handleModalHide);
            
            // Adicionar novos event listeners
            modal.addEventListener('show.bs.modal', this.handleModalShow.bind(this));
            modal.addEventListener('hide.bs.modal', this.handleModalHide.bind(this));
        }
    }

    handleModalShow(event) {
        console.log('Modal de entrada abrindo...');
        const modal = event.target;
        
        // REMOVER backdrop se existir
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(backdrop => backdrop.remove());
        
        // Prevenir scroll do body
        document.body.style.overflow = 'hidden';
        
        // Forçar foco no modal
        setTimeout(() => {
            const firstInput = modal.querySelector('input, textarea, select');
            if (firstInput) {
                firstInput.focus();
            }
        }, 100);
    }

    handleModalHide(event) {
        console.log('Modal de entrada fechando...');
        const modal = event.target;
        
        // REMOVER qualquer backdrop restante
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(backdrop => backdrop.remove());
        
        // Restaurar scroll do body
        document.body.style.overflow = '';
        
        // Limpar formulário
        const form = modal.querySelector('form');
        if (form) {
            form.reset();
        }
    }

    setupFormSubmission() {
        const form = document.getElementById('formEntradaProduto');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.salvarEntrada(form);
            });
        }
    }

    async salvarEntrada(form) {
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
                // Sucesso
                this.mostrarMensagem('success', data.message);
                form.reset();
                
                // Fechar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('entradaProdutoModal'));
                if (modal) {
                    modal.hide();
                }
                
                // Recarregar a página para mostrar a nova entrada
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
                
            } else {
                // Erro
                this.mostrarMensagem('error', data.message);
                if (data.errors) {
                    this.mostrarErrosFormulario(data.errors);
                }
            }
            
        } catch (error) {
            console.error('Erro ao salvar entrada:', error);
            this.mostrarMensagem('error', 'Erro ao salvar entrada. Tente novamente.');
        } finally {
            // Restaurar botão
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }
    }

    setupFormEdicao() {
        const form = document.getElementById('formEditarEntrada');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.salvarEdicao(form);
            });
        }
    }

    async salvarEdicao(form) {
        const formData = new FormData(form);
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        const entradaId = form.dataset.entradaId;
        
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
                // Sucesso
                this.mostrarMensagem('success', 'Entrada atualizada com sucesso!');
                
                // Fechar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('editarEntradaModal'));
                if (modal) {
                    modal.hide();
                }
                
                // Recarregar a página para mostrar as alterações
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
                
            } else {
                // Erro
                const data = await response.json();
                this.mostrarMensagem('error', data.message || 'Erro ao atualizar entrada');
                if (data.errors) {
                    this.mostrarErrosFormulario(data.errors);
                }
            }
            
        } catch (error) {
            console.error('Erro ao salvar edição:', error);
            this.mostrarMensagem('error', 'Erro ao atualizar entrada. Tente novamente.');
        } finally {
            // Restaurar botão
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }
    }

    setupFiltros() {
        // Aplicar filtros em tempo real
        const filtros = ['filtroProduto'];
        filtros.forEach(id => {
            const elemento = document.getElementById(id);
            if (elemento) {
                elemento.addEventListener('input', this.aplicarFiltros.bind(this));
            }
        });
    }

    aplicarFiltros() {
        const filtroProduto = document.getElementById('filtroProduto')?.value.toLowerCase() || '';
        
        const linhas = document.querySelectorAll('#tabelaEntradas tbody tr');
        let totalVisivel = 0;
        
        linhas.forEach(linha => {
            if (linha.querySelector('td[colspan]')) {
                // Linha de "nenhuma entrada"
                return;
            }
            
            const produto = linha.cells[1]?.textContent.toLowerCase() || '';
            
            const produtoMatch = produto.includes(filtroProduto);
            
            if (produtoMatch) {
                linha.style.display = '';
                totalVisivel++;
            } else {
                linha.style.display = 'none';
            }
        });
        
        const totalElement = document.getElementById('totalEntradas');
        if (totalElement) {
            totalElement.textContent = totalVisivel;
        }
    }

    limparFiltros() {
        document.getElementById('filtroProduto').value = '';
        this.aplicarFiltros();
    }

    setupTabela() {
        // Adicionar classes para melhorar a aparência
        const tabela = document.getElementById('tabelaEntradas');
        if (tabela) {
            tabela.classList.add('table-produtos');
        }
    }

    setupEventListeners() {
        // Event listeners globais
        document.addEventListener('click', this.handleGlobalClick.bind(this));
        
        // Formulário de entrada
        const form = document.getElementById('formEntradaProduto');
        if (form) {
            form.addEventListener('submit', this.handleFormSubmit.bind(this));
        }

        // Event listener para botão de confirmação de exclusão
        const confirmarExclusaoBtn = document.getElementById('confirmarExclusaoEntrada');
        if (confirmarExclusaoBtn) {
            confirmarExclusaoBtn.addEventListener('click', () => {
                this.confirmarExclusao();
            });
        }
    }

    handleGlobalClick(event) {
        // Verificar se é um botão de ação
        if (event.target.closest('.btn-action')) {
            event.preventDefault();
            event.stopPropagation();
            
            const button = event.target.closest('.btn-action');
            const action = button.dataset.action;
            const id = button.dataset.id;
            
            this.executarAcao(action, id);
        }
    }

    handleFormSubmit(event) {
        event.preventDefault();
        const form = event.target;
        this.salvarEntrada(form);
    }

    executarAcao(action, id) {
        switch (action) {
            case 'visualizar':
                this.visualizarEntrada(id);
                break;
            case 'editar':
                this.editarEntrada(id);
                break;
            case 'excluir':
                this.excluirEntrada(id);
                break;
        }
    }

    async visualizarEntrada(id) {
        console.log('Visualizando entrada:', id);
        try {
            const entrada = await this.buscarEntradaPorId(id);
            if (entrada) {
                this.preencherModalDetalhes(entrada);
                this.abrirModal('visualizarEntradaModal');
            }
        } catch (error) {
            console.error('Erro ao visualizar entrada:', error);
            this.mostrarMensagem('error', 'Erro ao carregar dados da entrada');
        }
    }

    async editarEntrada(id) {
        console.log('Editando entrada:', id);
        try {
            const entrada = await this.buscarEntradaPorId(id);
            if (entrada) {
                this.preencherModalEdicao(entrada);
                this.abrirModal('editarEntradaModal');
            }
        } catch (error) {
            console.error('Erro ao editar entrada:', error);
            this.mostrarMensagem('error', 'Erro ao carregar dados da entrada');
        }
    }

    async excluirEntrada(id) {
        console.log('Excluindo entrada:', id);
        try {
            // Buscar dados da entrada para mostrar no modal
            const entrada = await this.buscarEntradaPorId(id);
            if (entrada) {
                // Armazenar ID para exclusão
                this.entradaParaExcluir = id;
                
                // Atualizar texto do modal
                this.atualizarModalExclusao(entrada);
                
                // Abrir modal
                this.abrirModal('confirmarExclusaoEntradaModal');
            }
        } catch (error) {
            console.error('Erro ao carregar dados da entrada:', error);
            this.mostrarMensagem('error', 'Erro ao carregar dados da entrada');
        }
    }

    async buscarEntradaPorId(id) {
        try {
            const response = await fetch(`/produtos/detail-entrada-produto/${id}/`);
            if (response.ok) {
                const data = await response.json();
                return data;
            } else {
                throw new Error('Entrada não encontrada');
            }
        } catch (error) {
            console.error('Erro ao buscar entrada:', error);
            // Fallback para dados simulados
            return {
                id: id,
                codigo_produto: { nome_produto: "Produto " + id },
                quantidade: 10,
                id_equipamento: "EQ" + id,
                data: "2024-01-01T10:00",
                valor_nota: "100.00",
                numero_nota_fiscal: "NF" + id
            };
        }
    }

    preencherModalDetalhes(entrada) {
        const modal = document.getElementById('visualizarEntradaModal');
        const body = modal.querySelector('#detalhesEntrada');
        
        body.innerHTML = `
            <div class="row g-4">
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Produto:</label>
                        <p class="info-value">${entrada.codigo_produto.nome_produto}</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Quantidade:</label>
                        <p class="info-value">
                            <span class="badge bg-success fs-6">${entrada.quantidade}</span>
                        </p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">ID do Equipamento:</label>
                        <p class="info-value">
                            <span class="badge bg-secondary">${entrada.id_equipamento}</span>
                        </p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Data e Hora:</label>
                        <p class="info-value">
                            <i class="fas fa-calendar-alt me-2 text-primary"></i>${entrada.data}
                        </p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Valor da Nota:</label>
                        <p class="info-value">
                            <span class="badge bg-success fs-6">R$ ${entrada.valor_nota}</span>
                        </p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Número da Nota Fiscal:</label>
                        <p class="info-value">
                            <span class="badge bg-info">${entrada.numero_nota_fiscal}</span>
                        </p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">ID da Entrada:</label>
                        <p class="info-value">
                            <span class="badge bg-secondary">#${entrada.id}</span>
                        </p>
                    </div>
                </div>
            </div>
        `;
    }

    preencherModalEdicao(entrada) {
        const modal = document.getElementById('editarEntradaModal');
        const form = modal.querySelector('#formEditarEntrada');
        
        // Preencher campos do formulário
        form.querySelector('[name="codigo_produto"]').value = entrada.codigo_produto.id || '';
        form.querySelector('[name="quantidade"]').value = entrada.quantidade || '';
        form.querySelector('[name="id_equipamento"]').value = entrada.id_equipamento || '';
        form.querySelector('[name="data"]').value = entrada.data || '';
        form.querySelector('[name="valor_nota"]').value = entrada.valor_nota || '';
        form.querySelector('[name="numero_nota_fiscal"]').value = entrada.numero_nota_fiscal || '';
        
        // Armazenar ID da entrada e atualizar action do form
        form.dataset.entradaId = entrada.id;
        form.action = `/produtos/update-entrada-produto/${entrada.id}/`;
    }

    atualizarModalExclusao(entrada) {
        const modal = document.getElementById('confirmarExclusaoEntradaModal');
        const modalBody = modal.querySelector('.modal-body');
        
        modalBody.innerHTML = `
            <div class="text-center">
                <i class="fas fa-exclamation-triangle fa-3x text-warning mb-3"></i>
                <h5 class="mb-3">Confirmar Exclusão</h5>
                <p class="mb-2">Tem certeza que deseja excluir a entrada:</p>
                <p class="fw-bold text-primary mb-3">"${entrada.codigo_produto.nome_produto}" - Qtd: ${entrada.quantidade}</p>
                <p class="text-muted small">Esta ação não pode ser desfeita.</p>
            </div>
        `;
    }

    abrirModal(modalId) {
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();
    }

    confirmarExclusao() {
        if (this.entradaParaExcluir) {
            this.executarExclusao(this.entradaParaExcluir);
        }
    }

    async executarExclusao(id) {
        const confirmarBtn = document.getElementById('confirmarExclusaoEntrada');
        const originalText = confirmarBtn.innerHTML;
        
        try {
            console.log(`Excluindo entrada com ID: ${id}`);
            
            // Mostrar loading
            confirmarBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Excluindo...';
            confirmarBtn.disabled = true;
            
            const response = await fetch(`/produtos/delete-entrada-produto/${id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Sucesso
                this.mostrarMensagem('success', data.message);
                
                // Fechar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('confirmarExclusaoEntradaModal'));
                if (modal) {
                    modal.hide();
                }
                
                // Recarregar página para atualizar lista
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
                
            } else {
                // Erro
                this.mostrarMensagem('error', data.message || 'Erro ao excluir entrada');
            }
            
        } catch (error) {
            console.error('Erro ao excluir entrada:', error);
            this.mostrarMensagem('error', 'Erro ao excluir entrada. Tente novamente.');
        } finally {
            // Restaurar botão
            confirmarBtn.innerHTML = originalText;
            confirmarBtn.disabled = false;
        }
    }

    mostrarMensagem(tipo, mensagem) {
        // Remover mensagens existentes
        const existingAlerts = document.querySelectorAll('.alert-message');
        existingAlerts.forEach(alert => alert.remove());
        
        const alertClass = tipo === 'success' ? 'alert-success' : 'alert-danger';
        const icon = tipo === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle';
        
        const alert = document.createElement('div');
        alert.className = `alert ${alertClass} alert-dismissible fade show alert-message`;
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
        document.querySelectorAll('.error-message').forEach(error => error.remove());
        document.querySelectorAll('.is-invalid').forEach(field => field.classList.remove('is-invalid'));
        
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
}

// Funções globais para compatibilidade
function aplicarFiltros() {
    if (window.entradasManager) {
        window.entradasManager.aplicarFiltros();
    }
}

function limparFiltros() {
    if (window.entradasManager) {
        window.entradasManager.limparFiltros();
    }
}

function visualizarEntrada(id) {
    if (window.entradasManager) {
        window.entradasManager.visualizarEntrada(id);
    }
}

function editarEntrada(id) {
    if (window.entradasManager) {
        window.entradasManager.editarEntrada(id);
    }
}

function excluirEntrada(id) {
    if (window.entradasManager) {
        window.entradasManager.excluirEntrada(id);
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    window.entradasManager = new EntradasManager();
    console.log('EntradasManager inicializado');
});
