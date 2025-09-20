// JavaScript específico para o sidebar

class SidebarManager {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.sidebarToggle = document.getElementById('sidebarToggle');
        this.sidebarCloseBtn = document.getElementById('sidebarCloseBtn');
        this.sidebarOverlay = document.getElementById('sidebarOverlay');
        this.mainContent = document.querySelector('.main-content');
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupResponsive();
        this.setupActiveMenuItem();
        this.restoreActiveItem();
    }

    setupEventListeners() {
        // Toggle button
        if (this.sidebarToggle) {
            this.sidebarToggle.addEventListener('click', () => {
                this.toggle();
            });
        }

        // Close button
        if (this.sidebarCloseBtn) {
            this.sidebarCloseBtn.addEventListener('click', () => {
                this.hide();
            });
        }

        // Overlay click
        if (this.sidebarOverlay) {
            this.sidebarOverlay.addEventListener('click', () => {
                this.hide();
            });
        }

        // Submenu toggles
        document.querySelectorAll('.submenu-toggle').forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleSubmenu(toggle);
            });
        });

        // Menu item clicks
        document.querySelectorAll('.nav-link:not(.submenu-toggle)').forEach(link => {
            link.addEventListener('click', () => {
                this.setActiveMenuItem(link);
                
                // Close sidebar on mobile
                if (window.innerWidth <= 768) {
                    this.hide();
                }
            });
        });

        // Submenu link clicks
        document.querySelectorAll('.nav-submenu-link').forEach(link => {
            link.addEventListener('click', () => {
                this.setActiveMenuItem(link);
                
                // Close sidebar on mobile
                if (window.innerWidth <= 768) {
                    this.hide();
                }
            });
        });

        // Window resize
        window.addEventListener('resize', () => {
            this.handleResize();
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isVisible()) {
                this.hide();
            }
        });
    }

    setupResponsive() {
        this.handleResize();
    }

    setupActiveMenuItem() {
        // Set active menu item based on current URL
        const currentPath = window.location.pathname;
        const menuLinks = document.querySelectorAll('.nav-link, .nav-submenu-link');
        
        menuLinks.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                this.setActiveMenuItem(link);
            }
        });
    }

    toggle() {
        if (this.isVisible()) {
            this.hide();
        } else {
            this.show();
        }
    }

    show() {
        if (this.sidebar) {
            this.sidebar.classList.add('show');
        }
        if (this.sidebarOverlay) {
            this.sidebarOverlay.classList.add('show');
        }
        document.body.style.overflow = 'hidden';
    }

    hide() {
        if (this.sidebar) {
            this.sidebar.classList.remove('show');
        }
        if (this.sidebarOverlay) {
            this.sidebarOverlay.classList.remove('show');
        }
        document.body.style.overflow = '';
    }

    collapse() {
        if (this.sidebar) {
            this.sidebar.classList.toggle('collapsed');
            this.updateMainContentMargin();
        }
    }

    toggleSubmenu(toggle) {
        const navItem = toggle.closest('.nav-item');
        const targetId = toggle.getAttribute('data-target');
        const submenu = document.getElementById(targetId.replace('#', ''));
        
        if (navItem && submenu) {
            // Close other submenus
            this.closeOtherSubmenus(navItem);
            
            // Toggle current submenu
            navItem.classList.toggle('expanded');
            
            if (navItem.classList.contains('expanded')) {
                submenu.classList.add('show');
            } else {
                submenu.classList.remove('show');
            }
        }
    }

    closeOtherSubmenus(currentItem) {
        document.querySelectorAll('.nav-item.expanded').forEach(item => {
            if (item !== currentItem) {
                item.classList.remove('expanded');
                const submenu = item.querySelector('.nav-submenu');
                if (submenu) {
                    submenu.classList.remove('show');
                }
            }
        });
    }

    setActiveMenuItem(link) {
        // Remove active from all items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Add active to clicked item's parent
        const navItem = link.closest('.nav-item');
        if (navItem) {
            navItem.classList.add('active');
            
            // Store active item in localStorage
            localStorage.setItem('activeMenuItem', link.getAttribute('href'));
        }
    }

    restoreActiveItem() {
        const activeItem = localStorage.getItem('activeMenuItem');
        if (activeItem) {
            const link = document.querySelector(`[href="${activeItem}"]`);
            if (link) {
                this.setActiveMenuItem(link);
            }
        }
    }

    updateMainContentMargin() {
        if (this.mainContent) {
            if (this.sidebar && this.sidebar.classList.contains('collapsed')) {
                this.mainContent.style.marginLeft = '70px';
            } else {
                this.mainContent.style.marginLeft = '280px';
            }
        }
    }

    handleResize() {
        if (window.innerWidth > 768) {
            // Desktop
            this.hide();
            this.updateMainContentMargin();
        } else {
            // Mobile
            if (this.mainContent) {
                this.mainContent.style.marginLeft = '0';
            }
        }
    }

    isVisible() {
        return this.sidebar && this.sidebar.classList.contains('show');
    }

    isCollapsed() {
        return this.sidebar && this.sidebar.classList.contains('collapsed');
    }

    // Public methods for external use
    addMenuItem(config) {
        const { section, title, href, icon, badge } = config;
        
        const sectionElement = document.querySelector(`.nav-section:has(.nav-section-title:contains("${section}"))`);
        if (sectionElement) {
            const menu = sectionElement.querySelector('.nav-menu');
            if (menu) {
                const li = document.createElement('li');
                li.className = 'nav-item';
                li.innerHTML = `
                    <a href="${href}" class="nav-link">
                        <i class="${icon} nav-icon"></i>
                        <span class="nav-text">${title}</span>
                        ${badge ? `<span class="nav-badge">${badge}</span>` : ''}
                    </a>
                `;
                
                menu.appendChild(li);
                this.bindMenuItemEvents(li);
            }
        }
    }

    bindMenuItemEvents(menuItem) {
        const link = menuItem.querySelector('.nav-link');
        if (link) {
            link.addEventListener('click', () => {
                this.setActiveMenuItem(link);
                
                if (window.innerWidth <= 768) {
                    this.hide();
                }
            });
        }
    }

    // Animation methods
    animateMenuItems() {
        const items = document.querySelectorAll('.nav-item');
        items.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.05}s`;
        });
    }

    // Utility methods
    dispatchEvent(eventName, detail = {}) {
        const event = new CustomEvent(eventName, { detail });
        document.dispatchEvent(event);
    }
}

// Funções globais para compatibilidade
function toggleSidebar() {
    if (window.sidebarManager) {
        window.sidebarManager.toggle();
    }
}

function closeSidebar() {
    if (window.sidebarManager) {
        window.sidebarManager.hide();
    }
}

function toggleSubmenu(element) {
    if (window.sidebarManager) {
        window.sidebarManager.toggleSubmenu(element);
    }
}

function toggleCollapse() {
    if (window.sidebarManager) {
        window.sidebarManager.collapse();
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    window.sidebarManager = new SidebarManager();
    console.log('SidebarManager inicializado');
});

// Exportar para uso em módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SidebarManager;
}