// JavaScript específico para entrada de produtos

class EntradaProdutosManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupModal();
        this.setupFormSubmission();
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
                // Verificar se é atualização de quantidade ou nova entrada
                if (data.quantity_updated) {
                    // Quantidade foi atualizada em entrada existente
                    this.mostrarMensagem('success', data.message);
                    
                    // Mostrar detalhes da atualização
                    if (data.entrada) {
                        const infoDiv = document.createElement('div');
                        infoDiv.className = 'alert alert-success mt-2';
                        infoDiv.innerHTML = `
                            <strong><i class="fas fa-sync-alt me-2"></i>Quantidade Atualizada:</strong><br>
                            <div class="mt-2">
                                <small>
                                    <strong>Produto:</strong> ${data.entrada.produto}<br>
                                    <strong>Quantidade Anterior:</strong> ${data.entrada.quantidade_anterior}<br>
                                    <strong>Quantidade Adicionada:</strong> ${data.entrada.quantidade_adicionada}<br>
                                    <strong>Total Atual:</strong> <span class="badge bg-success">${data.entrada.quantidade_total}</span><br>
                                    <strong>Total de IDs:</strong> <span class="badge bg-info">${data.entrada.total_ids_equipamentos}</span>
                                </small>
                            </div>
                        `;
                        form.appendChild(infoDiv);
                        
                        // Remover após 7 segundos
                        setTimeout(() => {
                            if (infoDiv.parentNode) {
                                infoDiv.parentNode.removeChild(infoDiv);
                            }
                        }, 7000);
                    }
                } else {
                    // Nova entrada criada
                    this.mostrarMensagem('success', data.message);
                }
                
                form.reset();
                
                // Fechar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('entradaProdutoModal'));
                if (modal) {
                    modal.hide();
                }
                
                // Recarregar a página para mostrar as mudanças
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

    setupFiltros() {
        // Aplicar filtros em tempo real
        const filtros = ['filtroProduto'];
        filtros.forEach(id => {
            const elemento = document.getElementById(id);
            if (elemento) {
                elemento.addEventListener('input', this.aplicarFiltros.bind(this));
            }
        });
        
        // Event listener para busca por equipamento
        const filtroIdEquipamento = document.getElementById('filtroIdEquipamento');
        if (filtroIdEquipamento) {
            filtroIdEquipamento.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.buscarEquipamento();
                }
            });
        }
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
    
    async buscarEquipamento() {
        console.log('Manager.buscarEquipamento chamado');
        const idEquipamento = document.getElementById('filtroIdEquipamento')?.value.trim();
        console.log('ID do equipamento:', idEquipamento);
        
        if (!idEquipamento) {
            console.log('ID vazio, mostrando mensagem de aviso');
            this.mostrarMensagem('warning', 'Digite um ID de equipamento para buscar');
            return;
        }
        
        try {
            const response = await fetch(`/produtos/buscar-equipamento/?id_equipamento=${encodeURIComponent(idEquipamento)}`);
            const data = await response.json();
            
            if (data.success) {
                this.mostrarResultadoBusca(data);
            } else {
                this.mostrarMensagem('error', data.message);
            }
        } catch (error) {
            console.error('Erro ao buscar equipamento:', error);
            this.mostrarMensagem('error', 'Erro ao buscar equipamento. Tente novamente.');
        }
    }
    
    mostrarResultadoBusca(data) {
        const resultadoDiv = document.getElementById('resultadoBuscaEquipamento');
        const conteudoDiv = document.getElementById('conteudoResultadoBusca');
        
        if (data.encontrado) {
            // Equipamento encontrado
            conteudoDiv.innerHTML = `
                <div class="alert alert-success mb-3">
                    <i class="fas fa-check-circle me-2"></i>
                    <strong>Equipamento Encontrado!</strong><br>
                    <small>${data.message}</small>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <h6 class="card-title">ID do Equipamento</h6>
                                <span class="badge bg-primary fs-6">${data.id_equipamento}</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <h6 class="card-title">Total de Entradas</h6>
                                <span class="badge bg-info fs-6">${data.total_entradas}</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <h6 class="card-title">Quantidade Total</h6>
                                <span class="badge bg-success fs-6">${data.total_quantidade}</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="mt-3">
                    <h6>Detalhes das Entradas:</h6>
                    <div class="table-responsive">
                        <table class="table table-sm table-striped">
                            <thead>
                                <tr>
                                    <th>Produto</th>
                                    <th>Quantidade</th>
                                    <th>Data Entrada</th>
                                    <th>Nota Fiscal</th>
                                    <th>Total IDs</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.equipamento_info.map(entrada => `
                                    <tr>
                                        <td>${entrada.produto}</td>
                                        <td><span class="badge bg-success">${entrada.quantidade}</span></td>
                                        <td>${entrada.data_entrada}</td>
                                        <td>${entrada.numero_nota_fiscal}</td>
                                        <td><span class="badge bg-info">${entrada.total_ids}</span></td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;
        } else {
            // Equipamento não encontrado
            conteudoDiv.innerHTML = `
                <div class="alert alert-warning">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    <strong>Equipamento Não Encontrado</strong><br>
                    <small>${data.message}</small>
                </div>
                <div class="text-center">
                    <i class="fas fa-search fa-3x text-muted mb-3"></i>
                    <p class="text-muted">O equipamento <strong>${data.id_equipamento}</strong> não foi encontrado no estoque.</p>
                </div>
            `;
        }
        
        resultadoDiv.style.display = 'block';
        resultadoDiv.scrollIntoView({ behavior: 'smooth' });
    }
    
    limparBusca() {
        document.getElementById('filtroIdEquipamento').value = '';
        document.getElementById('filtroProduto').value = '';
        document.getElementById('resultadoBuscaEquipamento').style.display = 'none';
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
        
        // Select de produto
        const selectProduto = document.getElementById('id_codigo_produto');
        if (selectProduto) {
            selectProduto.addEventListener('change', this.handleProdutoChange.bind(this));
        }
        
        // Campo de data - definir data atual
        const campoData = document.getElementById('id_data');
        if (campoData && !campoData.value) {
            const agora = new Date();
            const dataFormatada = agora.toISOString().slice(0, 16);
            campoData.value = dataFormatada;
        }
    }

    handleGlobalClick(event) {
        // Verificar se é um botão de ação
        if (event.target.closest('.btn-action')) {
            console.log('Botão de ação clicado');
            event.preventDefault();
            event.stopPropagation();
            
            const button = event.target.closest('.btn-action');
            const action = button.dataset.action;
            const id = button.dataset.id;
            const nome = button.dataset.nome;
            
            console.log('Dados do botão:', { action, id, nome });
            
            this.executarAcao(action, id, nome);
        }
    }

    handleFormSubmit(event) {
        event.preventDefault();
        const form = event.target;
        this.salvarEntrada(form);
    }

    executarAcao(action, id, nome) {
        console.log('Executando ação:', action, 'ID:', id, 'Nome:', nome);
        
        switch (action) {
            case 'visualizar':
                console.log('Chamando visualizarEntrada');
                this.visualizarEntrada(id);
                break;
            case 'editar':
                console.log('Chamando editarEntrada');
                this.editarEntrada(id);
                break;
            case 'excluir':
                console.log('Chamando excluirEntrada');
                this.excluirEntrada(id);
                break;
            default:
                console.log('Ação não reconhecida:', action);
        }
    }

    handleProdutoChange(event) {
        const select = event.target;
        const optionSelecionada = select.options[select.selectedIndex];
        
        if (optionSelecionada.value) {
            const fabricante = optionSelecionada.dataset.fabricante;
            const valor = optionSelecionada.dataset.valor;
            
            // Mostrar informações do produto selecionado
            this.mostrarInfoProduto(optionSelecionada.textContent, fabricante, valor);
        } else {
            this.ocultarInfoProduto();
        }
    }

    mostrarInfoProduto(nome, fabricante, valor) {
        // Remover info anterior se existir
        this.ocultarInfoProduto();
        
        // Criar elemento de informação
        const infoDiv = document.createElement('div');
        infoDiv.id = 'info-produto-selecionado';
        infoDiv.className = 'alert alert-success mt-3';
        infoDiv.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-check-circle me-2 fs-5"></i>
                <div>
                    <strong>Produto Selecionado:</strong>
                    <div class="small">
                        <span class="badge bg-primary me-2">${nome}</span>
                        <span class="badge bg-info me-2">Fabricante: ${fabricante}</span>
                        <span class="badge bg-success">Valor: R$ ${valor}</span>
                    </div>
                </div>
            </div>
        `;
        
        // Inserir após o select
        const selectProduto = document.getElementById('id_codigo_produto');
        selectProduto.parentNode.appendChild(infoDiv);
    }

    ocultarInfoProduto() {
        const infoDiv = document.getElementById('info-produto-selecionado');
        if (infoDiv) {
            infoDiv.remove();
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
            console.log('Dados da entrada carregados:', entrada);
            
            if (entrada) {
                // Armazenar ID para exclusão
                this.entradaParaExcluir = id;
                console.log('ID armazenado para exclusão:', this.entradaParaExcluir);
                
                // Atualizar texto do modal
                this.atualizarModalExclusao(entrada);
                
                // Abrir modal
                this.abrirModal('confirmarExclusaoEntradaModal');
            } else {
                console.error('Entrada não encontrada');
                this.mostrarMensagem('error', 'Entrada não encontrada');
            }
        } catch (error) {
            console.error('Erro ao carregar dados da entrada:', error);
            this.mostrarMensagem('error', 'Erro ao carregar dados da entrada');
        }
    }

    async buscarEntradaPorId(id) {
        try {
            console.log('DEBUG - Buscando entrada ID:', id);
            const response = await fetch(`/produtos/detail-entrada-produto/${id}/`);
            console.log('DEBUG - Response status:', response.status);
            
            if (response.ok) {
                const data = await response.json();
                console.log('DEBUG - Dados recebidos:', data);
                return data;
            } else {
                console.error('DEBUG - Erro na resposta:', response.status, response.statusText);
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
                numero_nota_fiscal: "NF" + id,
                total_ids: 1,
                historico_ids: []
            };
        }
    }

    preencherModalDetalhes(entrada) {
        console.log('DEBUG - Preenchendo modal com dados:', entrada);
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
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Total de IDs:</label>
                        <p class="info-value">
                            <span class="badge bg-info">${entrada.total_ids || 1}</span>
                        </p>
                    </div>
                </div>
            </div>
            ${entrada.historico_ids && entrada.historico_ids.length > 0 ? `
                <div class="row mt-4">
                    <div class="col-12">
                        <h6><i class="fas fa-history me-2 text-primary"></i>Histórico de IDs de Equipamentos</h6>
                        <div class="table-responsive">
                            <table class="table table-sm table-striped">
                                <thead>
                                    <tr>
                                        <th><i class="fas fa-tag me-1"></i>ID do Equipamento</th>
                                        <th><i class="fas fa-clock me-1"></i>Data de Entrada</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${entrada.historico_ids.map(item => `
                                        <tr>
                                            <td><span class="badge bg-primary">${item.id}</span></td>
                                            <td><small class="text-muted"><i class="fas fa-calendar me-1"></i>${item.data_formatada}</small></td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            ` : ''}
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
        console.log('Atualizando modal de exclusão com entrada:', entrada);
        
        const modal = document.getElementById('confirmarExclusaoEntradaModal');
        if (!modal) {
            console.error('Modal de confirmação não encontrado');
            return;
        }
        
        const modalBody = modal.querySelector('.modal-body');
        if (!modalBody) {
            console.error('Modal body não encontrado');
            return;
        }
        
        modalBody.innerHTML = `
            <div class="text-center">
                <i class="fas fa-exclamation-triangle fa-3x text-warning mb-3"></i>
                <h5 class="mb-3">Confirmar Exclusão</h5>
                <p class="mb-2">Tem certeza que deseja excluir a entrada:</p>
                <p class="fw-bold text-primary mb-3">"${entrada.codigo_produto.nome_produto}" - Qtd: ${entrada.quantidade} - ID: ${entrada.id_equipamento}</p>
                <p class="text-muted small">Esta ação não pode ser desfeita.</p>
            </div>
        `;
        
        // Configurar botão de confirmação
        const confirmarBtn = document.getElementById('confirmarExclusaoEntrada');
        console.log('Botão de confirmação encontrado:', confirmarBtn);
        
        if (confirmarBtn) {
            // Remover event listeners anteriores
            confirmarBtn.onclick = null;
            // Adicionar novo event listener
            confirmarBtn.onclick = () => {
                console.log('Botão de confirmação clicado');
                this.executarExclusaoEntrada();
            };
            console.log('Event listener configurado no botão');
        } else {
            console.error('Botão de confirmação não encontrado');
        }
    }
    
    async executarExclusaoEntrada() {
        console.log('Executando exclusão, ID:', this.entradaParaExcluir);
        
        if (!this.entradaParaExcluir) {
            console.error('ID da entrada não encontrado');
            this.mostrarMensagem('error', 'ID da entrada não encontrado');
            return;
        }
        
        const confirmarBtn = document.getElementById('confirmarExclusaoEntrada');
        if (!confirmarBtn) {
            console.error('Botão de confirmação não encontrado');
            this.mostrarMensagem('error', 'Botão de confirmação não encontrado');
            return;
        }
        
        const originalText = confirmarBtn.innerHTML;
        
        try {
            // Mostrar loading
            confirmarBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Excluindo...';
            confirmarBtn.disabled = true;
            
            const url = `/produtos/delete-entrada-produto/${this.entradaParaExcluir}/`;
            console.log('Fazendo requisição DELETE para:', url);
            
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
            if (!csrfToken) {
                console.error('CSRF token não encontrado');
                this.mostrarMensagem('error', 'Token de segurança não encontrado');
                return;
            }
            
            const response = await fetch(url, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken.value,
                    'Content-Type': 'application/json'
                }
            });
            
            console.log('Resposta recebida:', response.status, response.statusText);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('Dados recebidos:', data);
            
            if (data.success) {
                this.mostrarMensagem('success', data.message);
                
                // Fechar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('confirmarExclusaoEntradaModal'));
                if (modal) {
                    modal.hide();
                }
                
                // Recarregar página
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                this.mostrarMensagem('error', data.message);
            }
        } catch (error) {
            console.error('Erro ao excluir entrada:', error);
            this.mostrarMensagem('error', `Erro ao excluir entrada: ${error.message}`);
        } finally {
            // Restaurar botão
            confirmarBtn.innerHTML = originalText;
            confirmarBtn.disabled = false;
        }
    }

    abrirModal(modalId) {
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();
    }

    mostrarMensagem(tipo, mensagem) {
        // Remover mensagens existentes
        const existingAlerts = document.querySelectorAll('.alert-message');
        existingAlerts.forEach(alert => alert.remove());
        
        const alertClass = tipo === 'success' ? 'alert-success' : 
                          tipo === 'error' ? 'alert-danger' : 
                          tipo === 'warning' ? 'alert-warning' : 'alert-info';
        const icon = tipo === 'success' ? 'fa-check-circle' : 
                    tipo === 'error' ? 'fa-exclamation-triangle' : 
                    tipo === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle';
        
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
    if (window.entradaProdutosManager) {
        window.entradaProdutosManager.aplicarFiltros();
    }
}

function limparFiltros() {
    if (window.entradaProdutosManager) {
        window.entradaProdutosManager.limparFiltros();
    }
}

function buscarEquipamento() {
    console.log('Função buscarEquipamento chamada');
    console.log('Manager disponível:', !!window.entradaProdutosManager);
    
    if (window.entradaProdutosManager) {
        console.log('Chamando buscarEquipamento do manager');
        window.entradaProdutosManager.buscarEquipamento();
    } else {
        console.error('EntradaProdutosManager não está disponível');
        alert('Erro: Sistema não inicializado. Recarregue a página.');
    }
}

function limparBusca() {
    if (window.entradaProdutosManager) {
        window.entradaProdutosManager.limparBusca();
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM carregado, inicializando EntradaProdutosManager...');
    try {
        window.entradaProdutosManager = new EntradaProdutosManager();
        console.log('EntradaProdutosManager inicializado com sucesso');
        
        // Teste do botão de busca
        const botaoBusca = document.querySelector('button[onclick="buscarEquipamento()"]');
        console.log('Botão de busca encontrado:', !!botaoBusca);
        
        if (botaoBusca) {
            console.log('Adicionando event listener adicional ao botão de busca');
            botaoBusca.addEventListener('click', function(e) {
                console.log('Botão de busca clicado via event listener');
                e.preventDefault();
                buscarEquipamento();
            });
        }
    } catch (error) {
        console.error('Erro ao inicializar EntradaProdutosManager:', error);
    }
});

// ========================================
// SCRIPT DE CONTAGEM AUTOMÁTICA DE EQUIPAMENTOS
// ========================================

// Bloquear tecla Enter
document.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
        e.preventDefault(); // Bloqueia a tecla Enter
    }
});

// Monitorar input para contagem automática
document.addEventListener("input", function (e) {
    var input = e.target;
    var value = input.value;
    var patterns = ["35154", "35642", "86590", "86325", "35196", "35643", "03G01"]; // Padrões a serem encontrados

    // Determina qual campo de quantidade usar baseado no contexto
    var quantidadeCampo = null;
    var isEditModal = input.closest('#editarEntradaModal');
    
    if (isEditModal) {
        quantidadeCampo = document.getElementById("id_quantidade_edit");
    } else {
        quantidadeCampo = document.getElementById("id_quantidade");
    }
    
    if (!quantidadeCampo) return; // Se não encontrar o campo, sai da função
    
    var quantidadeAtual = parseInt(quantidadeCampo.value || "0", 10); // Valor atual do campo
    var quantidadeEncontrada = 0; // Contador para padrões encontrados

    // Itera pelos padrões e substitui cada ocorrência
    patterns.forEach(function (pattern) {
        var regex = new RegExp(pattern, "g"); // Regex global para encontrar o padrão
        value = value.replace(regex, function () {
            quantidadeEncontrada += 1; // Incrementa a quantidade para cada correspondência encontrada
            return "     "; // Substitui o padrão por 5 espaços
        });
    });

    // Atualiza o valor do campo de entrada sem os padrões
    input.value = value;

    // Incrementa a quantidade total e atualiza o campo do formulário
    var novaQuantidade = quantidadeAtual + quantidadeEncontrada;
    quantidadeCampo.value = novaQuantidade; // Atualiza o campo do formulário diretamente

    console.log(`Quantidade encontrada nesta entrada: ${quantidadeEncontrada}`);
    console.log(`Quantidade total acumulada: ${novaQuantidade}`);
    
    // Mostrar feedback visual quando códigos são detectados
    if (quantidadeEncontrada > 0) {
        mostrarFeedbackContagem(quantidadeEncontrada, novaQuantidade);
    }
});

// Função para mostrar feedback visual da contagem
function mostrarFeedbackContagem(encontrados, total) {
    // Remover feedback anterior se existir
    const feedbackAnterior = document.getElementById('feedback-contagem');
    if (feedbackAnterior) {
        feedbackAnterior.remove();
    }
    
    // Criar elemento de feedback
    const feedback = document.createElement('div');
    feedback.id = 'feedback-contagem';
    feedback.className = 'alert alert-success alert-dismissible fade show';
    feedback.style.position = 'fixed';
    feedback.style.top = '80px';
    feedback.style.right = '20px';
    feedback.style.zIndex = '9999';
    feedback.style.minWidth = '300px';
    feedback.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-barcode me-2 fs-4"></i>
            <div>
                <strong>Códigos Detectados!</strong>
                <div class="small">
                    <span class="badge bg-primary me-2">+${encontrados} equipamentos</span>
                    <span class="badge bg-success">Total: ${total}</span>
                </div>
            </div>
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(feedback);
    
    // Auto-remover após 3 segundos
    setTimeout(() => {
        if (feedback.parentNode) {
            feedback.remove();
        }
    }, 3000);
}

// Função para resetar quantidade
function resetarQuantidade(campoId) {
    const campo = document.getElementById(campoId);
    if (campo) {
        campo.value = '';
        
        // Atualizar o modal se estiver aberto
        const modal = document.querySelector('.modal.show');
        if (modal) {
            // Adicionar efeito visual de atualização
            modal.style.transition = 'all 0.3s ease';
            modal.style.transform = 'scale(0.98)';
            modal.style.opacity = '0.8';
            
            setTimeout(() => {
                // Restaurar estado normal do modal
                modal.style.transform = 'scale(1)';
                modal.style.opacity = '1';
                
                // Forçar re-renderização do campo
                campo.style.background = '#f8f9fa';
                setTimeout(() => {
                    campo.style.background = '';
                }, 200);
                
                // Focar no campo resetado
                campo.focus();
                
                // Atualizar qualquer feedback visual
                const feedback = document.getElementById('feedback-contagem');
                if (feedback) {
                    feedback.remove();
                }
                
            }, 150);
        }
        
        // Mostrar mensagem de sucesso
        mostrarMensagem('success', 'Contagem resetada com sucesso!');
        
        // Log para debug
        console.log(`Campo ${campoId} resetado com sucesso`);
    }
}

// Adicionar indicador visual no campo de quantidade
document.addEventListener('DOMContentLoaded', function() {
    // Aplicar para o campo principal
    const quantidadeCampo = document.getElementById('id_quantidade');
    if (quantidadeCampo) {
        // Adicionar ícone de scanner
        const label = quantidadeCampo.previousElementSibling;
        if (label && label.tagName === 'LABEL') {
            label.innerHTML = `
                <i class="fas fa-hashtag me-2 text-success"></i>
                <i class="fas fa-barcode me-1 text-info"></i>Quantidade *
            `;
        }
        
        // Adicionar texto de ajuda
        const formText = quantidadeCampo.parentNode.nextElementSibling;
        if (formText && formText.classList.contains('form-text')) {
            formText.innerHTML = `
                <small class="text-muted">
                    <i class="fas fa-lock me-1 text-warning"></i>
                    Campo automático - digite códigos em qualquer campo para contagem
                    <br>
                    <i class="fas fa-qrcode me-1"></i>
                    Códigos suportados: 35154, 35642, 86590, 86325, 35196, 35643, 03G01
                </small>
            `;
        }
    }
    
    // Aplicar para o campo de edição (quando o modal for aberto)
    const editarModal = document.getElementById('editarEntradaModal');
    if (editarModal) {
        editarModal.addEventListener('shown.bs.modal', function() {
            const quantidadeEditCampo = document.getElementById('id_quantidade_edit');
            if (quantidadeEditCampo) {
                // Adicionar ícone de scanner
                const label = quantidadeEditCampo.previousElementSibling;
                if (label && label.tagName === 'LABEL') {
                    label.innerHTML = `
                        <i class="fas fa-hashtag me-2 text-success"></i>
                        <i class="fas fa-barcode me-1 text-info"></i>Quantidade *
                    `;
                }
                
                // Adicionar texto de ajuda
                const formText = quantidadeEditCampo.parentNode.nextElementSibling;
                if (formText && formText.classList.contains('form-text')) {
                    formText.innerHTML = `
                        <small class="text-muted">
                            <i class="fas fa-lock me-1 text-warning"></i>
                            Campo automático - digite códigos em qualquer campo para contagem
                            <br>
                            <i class="fas fa-qrcode me-1"></i>
                            Códigos suportados: 35154, 35642, 86590, 86325, 35196, 35643, 03G01
                        </small>
                    `;
                }
            }
        });
    }
    
    // Event listeners para botões de reset
    const resetBtn = document.getElementById('resetQuantidade');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            resetarQuantidade('id_quantidade');
        });
    }
    
    const resetEditBtn = document.getElementById('resetQuantidadeEdit');
    if (resetEditBtn) {
        resetEditBtn.addEventListener('click', function() {
            resetarQuantidade('id_quantidade_edit');
        });
    }
    
    // Adicionar efeito visual nos botões de reset
    const resetButtons = document.querySelectorAll('[id^="resetQuantidade"]');
    resetButtons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
        
        btn.addEventListener('click', function() {
            // Efeito de clique
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 100);
        });
    });
});

// Funções globais para exportar e imprimir
function exportarDados() {
    console.log('Exportando dados...');
    
    // Criar dados para exportação
    const tabela = document.getElementById('tabelaEntradas');
    const linhas = tabela.querySelectorAll('tbody tr');
    
    let dadosCSV = 'ID,Produto,Quantidade,ID Equipamento,Data,Nota Fiscal,Valor\n';
    
    linhas.forEach(linha => {
        const colunas = linha.querySelectorAll('td');
        if (colunas.length > 0) {
            const id = colunas[0]?.textContent?.trim() || '';
            const produto = colunas[1]?.querySelector('strong')?.textContent?.trim() || '';
            const quantidade = colunas[2]?.textContent?.trim() || '';
            const idEquipamento = colunas[3]?.textContent?.trim() || '';
            const data = colunas[4]?.textContent?.trim() || '';
            const notaFiscal = colunas[5]?.textContent?.trim() || '';
            const valor = colunas[6]?.textContent?.trim() || '';
            
            dadosCSV += `"${id}","${produto}","${quantidade}","${idEquipamento}","${data}","${notaFiscal}","${valor}"\n`;
        }
    });
    
    // Criar e baixar arquivo
    const blob = new Blob([dadosCSV], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `estoque_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    console.log('Dados exportados com sucesso!');
}

function imprimirTabela() {
    console.log('Preparando para impressão...');
    
    // Criar janela de impressão
    const janelaImpressao = window.open('', '_blank');
    const tabela = document.getElementById('tabelaEntradas');
    const titulo = document.querySelector('.card-title').textContent;
    
    janelaImpressao.document.write(`
        <html>
            <head>
                <title>Relatório de Estoque - ${new Date().toLocaleDateString()}</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1 { color: #333; text-align: center; }
                    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; font-weight: bold; }
                    .badge { padding: 2px 6px; border-radius: 3px; font-size: 12px; }
                    .bg-success { background-color: #28a745; color: white; }
                    .bg-secondary { background-color: #6c757d; color: white; }
                    .bg-info { background-color: #17a2b8; color: white; }
                    .bg-warning { background-color: #ffc107; color: black; }
                    @media print { body { margin: 0; } }
                </style>
            </head>
            <body>
                <h1>Relatório de Estoque</h1>
                <p><strong>Data:</strong> ${new Date().toLocaleDateString()}</p>
                <p><strong>Total de Entradas:</strong> ${document.getElementById('totalEntradas').textContent}</p>
                ${tabela.outerHTML}
            </body>
        </html>
    `);
    
    janelaImpressao.document.close();
    janelaImpressao.print();
    
    console.log('Impressão iniciada!');
}
