// JavaScript específico para registro de manutenção

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar componentes
    initializeManutencao();
    initializeFilters();
    initializeModals();
    initializeStatusUpdates();
    initializeImageUpload();
});

function initializeManutencao() {
    console.log('Inicializando sistema de manutenção...');
    
    // Adicionar animações aos cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.classList.add('fade-in');
    });
    
    // Configurar tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializeFilters() {
    const filterForm = document.getElementById('filterForm');
    const filterBtn = document.getElementById('filterBtn');
    const clearBtn = document.getElementById('clearBtn');
    
    if (filterForm) {
        // Aplicar filtros ao submeter
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            applyFilters();
        });
        
        // Aplicar filtros em tempo real
        const filterInputs = filterForm.querySelectorAll('input, select');
        filterInputs.forEach(input => {
            input.addEventListener('change', function() {
                if (this.type === 'text') {
                    // Debounce para campos de texto
                    clearTimeout(this.searchTimeout);
                    this.searchTimeout = setTimeout(() => {
                        applyFilters();
                    }, 500);
                } else {
                    applyFilters();
                }
            });
        });
    }
    
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            clearFilters();
        });
    }
}

function applyFilters() {
    const filterForm = document.getElementById('filterForm');
    if (!filterForm) return;
    
    const formData = new FormData(filterForm);
    const params = new URLSearchParams();
    
    // Adicionar apenas campos preenchidos
    for (let [key, value] of formData.entries()) {
        if (value.trim() !== '') {
            params.append(key, value);
        }
    }
    
    // Redirecionar com filtros aplicados
    const currentUrl = new URL(window.location);
    currentUrl.search = params.toString();
    window.location.href = currentUrl.toString();
}

function clearFilters() {
    const filterForm = document.getElementById('filterForm');
    if (!filterForm) return;
    
    // Limpar todos os campos
    const inputs = filterForm.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        if (input.type === 'checkbox' || input.type === 'radio') {
            input.checked = false;
        } else {
            input.value = '';
        }
    });
    
    // Redirecionar sem filtros
    const currentUrl = new URL(window.location);
    currentUrl.search = '';
    window.location.href = currentUrl.toString();
}

function initializeModals() {
    // Modal de confirmação para exclusão
    const deleteButtons = document.querySelectorAll('[data-action="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const manutencaoId = this.dataset.id;
            const manutencaoTitle = this.dataset.title || `Manutenção #${manutencaoId}`;
            
            showConfirmModal(
                'Excluir Registro',
                `Tem certeza que deseja excluir ${manutencaoTitle}?`,
                'Esta ação não pode ser desfeita.',
                'Excluir',
                'btn-danger',
                function() {
                    deleteManutencao(manutencaoId);
                }
            );
        });
    });
    
    // Modal de confirmação para mudança de status
    const statusButtons = document.querySelectorAll('[data-action="status"]');
    statusButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const manutencaoId = this.dataset.id;
            const newStatus = this.dataset.status;
            const statusText = this.textContent.trim();
            
            showConfirmModal(
                'Alterar Status',
                `Deseja alterar o status para "${statusText}"?`,
                'Esta alteração será registrada no histórico.',
                'Confirmar',
                'btn-primary',
                function() {
                    updateStatus(manutencaoId, newStatus);
                }
            );
        });
    });
}

function showConfirmModal(title, message, subMessage, buttonText, buttonClass, callback) {
    // Criar modal se não existir
    let modal = document.getElementById('confirmModal');
    if (!modal) {
        modal = createConfirmModal();
        document.body.appendChild(modal);
    }
    
    // Configurar conteúdo
    document.getElementById('confirmTitle').textContent = title;
    document.getElementById('confirmMessage').textContent = message;
    document.getElementById('confirmSubMessage').textContent = subMessage;
    document.getElementById('confirmButton').textContent = buttonText;
    
    // Configurar classes do botão
    const confirmBtn = document.getElementById('confirmButton');
    confirmBtn.className = `btn ${buttonClass}`;
    
    // Configurar callback
    confirmBtn.onclick = function() {
        callback();
        bootstrap.Modal.getInstance(modal).hide();
    };
    
    // Mostrar modal
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
}

function createConfirmModal() {
    const modal = document.createElement('div');
    modal.id = 'confirmModal';
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-body text-center">
                    <div id="confirmIcon" class="text-warning mb-3">
                        <i class="fas fa-exclamation-triangle fa-3x"></i>
                    </div>
                    <h4 id="confirmTitle" class="mb-3"></h4>
                    <p id="confirmMessage" class="mb-2"></p>
                    <small id="confirmSubMessage" class="text-muted"></small>
                </div>
                <div class="modal-footer justify-content-center">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="button" id="confirmButton" class="btn btn-primary">Confirmar</button>
                </div>
            </div>
        </div>
    `;
    return modal;
}

function deleteManutencao(manutencaoId) {
    const button = document.querySelector(`[data-action="delete"][data-id="${manutencaoId}"]`);
    if (button) {
        button.classList.add('loading');
        button.disabled = true;
    }
    
    fetch(`/manutencao/excluir/${manutencaoId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('success', data.message);
            // Remover card da tela
            const card = document.querySelector(`[data-manutencao-id="${manutencaoId}"]`);
            if (card) {
                card.style.transition = 'all 0.3s ease';
                card.style.transform = 'scale(0.8)';
                card.style.opacity = '0';
                setTimeout(() => {
                    card.remove();
                }, 300);
            }
        } else {
            showAlert('error', data.message);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        showAlert('error', 'Erro ao excluir registro de manutenção.');
    })
    .finally(() => {
        if (button) {
            button.classList.remove('loading');
            button.disabled = false;
        }
    });
}

function updateStatus(manutencaoId, newStatus) {
    const button = document.querySelector(`[data-action="status"][data-id="${manutencaoId}"]`);
    if (button) {
        button.classList.add('loading');
        button.disabled = true;
    }
    
    fetch(`/manutencao/status/${manutencaoId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `status=${encodeURIComponent(newStatus)}`,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('success', data.message);
            // Atualizar badge de status
            const statusBadge = document.querySelector(`[data-manutencao-id="${manutencaoId}"] .badge`);
            if (statusBadge) {
                statusBadge.textContent = data.new_status;
                statusBadge.className = `badge badge-status-${data.new_status.toLowerCase().replace(/\s+/g, '-')}`;
            }
        } else {
            showAlert('error', data.message);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        showAlert('error', 'Erro ao atualizar status.');
    })
    .finally(() => {
        if (button) {
            button.classList.remove('loading');
            button.disabled = false;
        }
    });
}

function initializeStatusUpdates() {
    // Dropdown de status
    const statusDropdowns = document.querySelectorAll('.status-dropdown');
    statusDropdowns.forEach(dropdown => {
        dropdown.addEventListener('change', function() {
            const manutencaoId = this.dataset.id;
            const newStatus = this.value;
            
            if (newStatus && newStatus !== this.dataset.currentStatus) {
                updateStatus(manutencaoId, newStatus);
            }
        });
    });
}

function initializeImageUpload() {
    // Preview de imagens
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById(`${input.id}_preview`);
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

function showAlert(type, message) {
    // Remover alertas existentes
    const existingAlerts = document.querySelectorAll('.alert-manutencao');
    existingAlerts.forEach(alert => alert.remove());
    
    // Criar novo alerta
    const alert = document.createElement('div');
    alert.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show alert-manutencao`;
    alert.style.position = 'fixed';
    alert.style.top = '20px';
    alert.style.right = '20px';
    alert.style.zIndex = '9999';
    alert.style.minWidth = '300px';
    
    alert.innerHTML = `
        ${message}
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

function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

// Funções utilitárias
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Busca em tempo real
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(this.value);
            }, 300);
        });
    }
}

function performSearch(query) {
    if (query.length < 2) {
        clearSearchResults();
        return;
    }
    
    fetch(`/manutencao/busca/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displaySearchResults(data.resultados);
            } else {
                showAlert('warning', data.message);
            }
        })
        .catch(error => {
            console.error('Erro na busca:', error);
            showAlert('error', 'Erro ao realizar busca.');
        });
}

function displaySearchResults(resultados) {
    const resultsContainer = document.getElementById('searchResults');
    if (!resultsContainer) return;
    
    if (resultados.length === 0) {
        resultsContainer.innerHTML = '<div class="text-center text-muted">Nenhum resultado encontrado</div>';
        return;
    }
    
    let html = '';
    resultados.forEach(resultado => {
        html += `
            <div class="search-result-item p-2 border-bottom">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">${resultado.nome}</h6>
                        <small class="text-muted">Cliente: ${resultado.cliente}</small>
                        <br>
                        <small class="text-muted">Produto: ${resultado.produto}</small>
                    </div>
                    <div>
                        <span class="badge badge-status-${resultado.status.toLowerCase().replace(/\s+/g, '-')}">${resultado.status}</span>
                    </div>
                </div>
            </div>
        `;
    });
    
    resultsContainer.innerHTML = html;
}

function clearSearchResults() {
    const resultsContainer = document.getElementById('searchResults');
    if (resultsContainer) {
        resultsContainer.innerHTML = '';
    }
}

// Exportar funções para uso global
window.manutencaoUtils = {
    showAlert,
    formatDate,
    formatCurrency,
    deleteManutencao,
    updateStatus
};
