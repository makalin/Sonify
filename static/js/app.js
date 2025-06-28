// Sonify - Spotify Data Visualizer JavaScript

// Global variables
let currentTheme = localStorage.getItem('theme') || 'light';
let charts = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    initializeCharts();
    initializeAnimations();
    initializeQuickActions();
});

// Theme management
function initializeTheme() {
    const html = document.documentElement;
    const savedTheme = localStorage.getItem('theme') || 'light';
    
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    
    // Update charts when theme changes
    updateAllCharts(savedTheme);
}

function updateThemeIcon(theme) {
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

function updateAllCharts(theme) {
    const chartIds = ['top-tracks-chart', 'top-artists-chart', 'heatmap-chart', 'mood-radar-chart'];
    
    chartIds.forEach(chartId => {
        const chart = document.getElementById(chartId);
        if (chart && chart.data) {
            Plotly.relayout(chartId, {
                template: theme === 'dark' ? 'plotly_dark' : 'plotly_white'
            });
        }
    });
}

// Chart initialization and management
function initializeCharts() {
    // Initialize any existing charts
    const chartElements = document.querySelectorAll('[id$="-chart"]');
    
    chartElements.forEach(element => {
        if (element.dataset.chartData) {
            try {
                const chartData = JSON.parse(element.dataset.chartData);
                Plotly.newPlot(element.id, chartData.data, chartData.layout, {
                    responsive: true,
                    displayModeBar: false
                });
                
                // Store chart reference
                charts[element.id] = element;
            } catch (error) {
                console.error('Error initializing chart:', error);
            }
        }
    });
}

// Animation system
function initializeAnimations() {
    // Add scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animateElements = document.querySelectorAll('.card, .stats-card, .track-card');
    animateElements.forEach(el => {
        observer.observe(el);
    });
    
    // Add pulse animation to stats cards
    const statsCards = document.querySelectorAll('.stats-card');
    statsCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.classList.add('pulse');
        });
        
        card.addEventListener('mouseleave', () => {
            card.classList.remove('pulse');
        });
    });
}

// Quick actions functionality
function initializeQuickActions() {
    const fab = document.getElementById('fab');
    if (fab) {
        fab.addEventListener('click', showQuickActionsMenu);
    }
}

function showQuickActionsMenu() {
    // Remove existing menu
    const existingMenu = document.querySelector('.quick-actions-menu');
    if (existingMenu) {
        existingMenu.remove();
    }
    
    // Create menu
    const menu = document.createElement('div');
    menu.className = 'quick-actions-menu';
    menu.style.cssText = `
        position: fixed;
        bottom: 5rem;
        right: 2rem;
        background: var(--card-bg);
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        padding: 1rem;
        z-index: 999;
        min-width: 200px;
        border: 1px solid var(--border-color);
        animation: slideIn 0.3s ease;
    `;
    
    const actions = [
        { icon: 'fas fa-chart-bar', text: 'View Charts', url: '/visualizations' },
        { icon: 'fas fa-brain', text: 'Mood Analysis', url: '/mood-analysis' },
        { icon: 'fas fa-chart-pie', text: 'Music Insights', url: '/insights' },
        { icon: 'fas fa-download', text: 'Export Data', action: 'export' },
        { icon: 'fas fa-sync', text: 'Refresh Data', action: 'refresh' }
    ];
    
    actions.forEach(action => {
        const item = createQuickActionItem(action);
        menu.appendChild(item);
    });
    
    document.body.appendChild(menu);
    
    // Close menu when clicking outside
    setTimeout(() => {
        document.addEventListener('click', function closeMenu(e) {
            if (!menu.contains(e.target) && !document.getElementById('fab').contains(e.target)) {
                menu.remove();
                document.removeEventListener('click', closeMenu);
            }
        });
    }, 100);
}

function createQuickActionItem(action) {
    const item = document.createElement('div');
    item.className = 'quick-action-item';
    item.style.cssText = `
        display: flex;
        align-items: center;
        padding: 0.75rem;
        cursor: pointer;
        border-radius: 8px;
        transition: all 0.2s ease;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    `;
    
    item.innerHTML = `
        <i class="${action.icon} me-3" style="width: 20px; text-align: center;"></i>
        <span>${action.text}</span>
    `;
    
    item.addEventListener('mouseenter', () => {
        item.style.backgroundColor = 'var(--bg-secondary)';
        item.style.transform = 'translateX(5px)';
    });
    
    item.addEventListener('mouseleave', () => {
        item.style.backgroundColor = 'transparent';
        item.style.transform = 'translateX(0)';
    });
    
    item.addEventListener('click', () => {
        if (action.url) {
            window.location.href = action.url;
        } else if (action.action === 'export') {
            exportAllCharts();
        } else if (action.action === 'refresh') {
            window.location.reload();
        }
        
        // Close menu
        const menu = document.querySelector('.quick-actions-menu');
        if (menu) menu.remove();
    });
    
    return item;
}

// Export functionality
function exportAllCharts() {
    const chartIds = ['top-tracks-chart', 'top-artists-chart', 'heatmap-chart', 'mood-radar-chart'];
    const chartsToExport = [];
    
    chartIds.forEach(chartId => {
        const chart = document.getElementById(chartId);
        if (chart && chart.data) {
            chartsToExport.push({
                id: chartId,
                data: chart.data,
                layout: chart.layout
            });
        }
    });
    
    if (chartsToExport.length > 0) {
        // Create a zip file with all charts
        const data = {
            charts: chartsToExport,
            exportDate: new Date().toISOString(),
            theme: currentTheme
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `sonify_charts_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showNotification('Charts exported successfully!', 'success');
    } else {
        showNotification('No charts available to export', 'warning');
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        background: var(--card-bg);
        color: var(--text-primary);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        border-left: 4px solid var(--spotify-green);
        animation: slideInRight 0.3s ease;
    `;
    
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Interactive features
function initializeInteractiveFeatures() {
    // Add click to copy functionality
    const copyElements = document.querySelectorAll('[data-copy]');
    copyElements.forEach(element => {
        element.addEventListener('click', () => {
            const textToCopy = element.dataset.copy;
            navigator.clipboard.writeText(textToCopy).then(() => {
                showNotification('Copied to clipboard!', 'success');
            });
        });
    });
    
    // Add hover effects to track cards
    const trackCards = document.querySelectorAll('.track-card');
    trackCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Data visualization helpers
function createCustomChart(containerId, data, options = {}) {
    const defaultOptions = {
        responsive: true,
        displayModeBar: false,
        template: currentTheme === 'dark' ? 'plotly_dark' : 'plotly_white'
    };
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
        Plotly.newPlot(containerId, data, finalOptions);
        return true;
    } catch (error) {
        console.error('Error creating chart:', error);
        return false;
    }
}

// Utility functions
function formatDuration(ms) {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to toggle theme
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.click();
        }
    }
    
    // Ctrl/Cmd + E to export
    if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
        e.preventDefault();
        exportAllCharts();
    }
    
    // Escape to close quick actions menu
    if (e.key === 'Escape') {
        const menu = document.querySelector('.quick-actions-menu');
        if (menu) {
            menu.remove();
        }
    }
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(100%); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideOutRight {
        from { opacity: 1; transform: translateX(0); }
        to { opacity: 0; transform: translateX(100%); }
    }
    
    .animate-in {
        animation: slideIn 0.6s ease forwards;
    }
    
    .card, .stats-card, .track-card {
        opacity: 0;
        transform: translateY(20px);
    }
    
    .card.animate-in, .stats-card.animate-in, .track-card.animate-in {
        opacity: 1;
        transform: translateY(0);
    }
`;
document.head.appendChild(style);

// Initialize interactive features when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeInteractiveFeatures();
});

// Export functions for global access
window.Sonify = {
    exportAllCharts,
    showNotification,
    createCustomChart,
    formatDuration,
    formatNumber
}; 