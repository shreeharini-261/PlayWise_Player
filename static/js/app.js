// PlayWise Music Player JavaScript functionality

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('PlayWise Music Player initialized');
    
    // Initialize tooltips
    initializeTooltips();
    
    // Setup form validations
    setupFormValidations();
    
    // Setup keyboard shortcuts
    setupKeyboardShortcuts();
    
    // Setup auto-refresh for dashboard
    if (window.location.pathname === '/dashboard') {
        setupDashboardRefresh();
    }
});

/**
 * Initialize Bootstrap tooltips for all elements with title attributes
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Setup form validations for better UX
 */
function setupFormValidations() {
    // Duration validation for add song form
    const durationInput = document.querySelector('input[name="duration"]');
    if (durationInput) {
        durationInput.addEventListener('input', function() {
            const value = parseInt(this.value);
            if (value && value > 0) {
                const minutes = Math.floor(value / 60);
                const seconds = value % 60;
                const formatted = `${minutes}:${seconds.toString().padStart(2, '0')}`;
                this.title = `Duration: ${formatted}`;
            }
        });
    }
    
    // Rating form validation
    const ratingSelects = document.querySelectorAll('select[name="rating"]');
    ratingSelects.forEach(select => {
        select.addEventListener('change', function() {
            const rating = parseInt(this.value);
            if (rating > 0) {
                const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);
                this.title = `${rating} stars: ${stars}`;
            }
        });
    });
    
    // Search form validation
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchType = this.querySelector('select[name="search_type"]').value;
            const query = this.querySelector('input[name="query"]').value.trim();
            
            if (searchType === 'rating') {
                const rating = parseInt(query);
                if (isNaN(rating) || rating < 1 || rating > 5) {
                    e.preventDefault();
                    alert('Please enter a rating between 1 and 5');
                    return false;
                }
            }
            
            if (!query) {
                e.preventDefault();
                alert('Please enter a search query');
                return false;
            }
        });
    }
}

/**
 * Setup keyboard shortcuts for common actions
 */
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to add song (when in title field)
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const titleInput = document.querySelector('input[name="title"]');
            if (titleInput && document.activeElement === titleInput) {
                const addForm = titleInput.closest('form');
                if (addForm) {
                    addForm.submit();
                }
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(modal => {
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) {
                    bsModal.hide();
                }
            });
        }
        
        // Arrow keys for playlist navigation (when focused on playlist)
        const playlistTable = document.querySelector('.table tbody');
        if (playlistTable && playlistTable.contains(document.activeElement)) {
            if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
                e.preventDefault();
                navigatePlaylist(e.key === 'ArrowUp' ? -1 : 1);
            }
            
            // Space to play selected song
            if (e.key === ' ') {
                e.preventDefault();
                const selectedRow = document.activeElement.closest('tr');
                if (selectedRow) {
                    const playButton = selectedRow.querySelector('a[href*="play_song"]');
                    if (playButton) {
                        playButton.click();
                    }
                }
            }
        }
    });
}

/**
 * Navigate playlist with keyboard
 */
function navigatePlaylist(direction) {
    const rows = document.querySelectorAll('.table tbody tr');
    const currentRow = document.activeElement.closest('tr');
    
    if (!currentRow) {
        if (rows.length > 0) {
            focusRow(rows[0]);
        }
        return;
    }
    
    const currentIndex = Array.from(rows).indexOf(currentRow);
    let newIndex = currentIndex + direction;
    
    if (newIndex < 0) newIndex = rows.length - 1;
    if (newIndex >= rows.length) newIndex = 0;
    
    focusRow(rows[newIndex]);
}

/**
 * Focus on a playlist row
 */
function focusRow(row) {
    const firstButton = row.querySelector('a, button');
    if (firstButton) {
        firstButton.focus();
    }
}

/**
 * Setup auto-refresh functionality for dashboard
 */
function setupDashboardRefresh() {
    let refreshInterval;
    
    // Start auto-refresh
    function startAutoRefresh() {
        refreshInterval = setInterval(() => {
            refreshDashboardData();
        }, 30000); // Refresh every 30 seconds
    }
    
    // Stop auto-refresh
    function stopAutoRefresh() {
        if (refreshInterval) {
            clearInterval(refreshInterval);
        }
    }
    
    // Refresh dashboard data
    function refreshDashboardData() {
        const refreshButton = document.querySelector('button[onclick="refreshData()"]');
        if (refreshButton) {
            const originalText = refreshButton.innerHTML;
            refreshButton.innerHTML = '<i data-feather="loader" class="me-2"></i>Refreshing...';
            refreshButton.disabled = true;
            
            fetch('/api/snapshot')
                .then(response => response.json())
                .then(data => {
                    updateDashboardElements(data);
                    showRefreshSuccess();
                })
                .catch(error => {
                    console.error('Dashboard refresh failed:', error);
                    showRefreshError();
                })
                .finally(() => {
                    refreshButton.innerHTML = originalText;
                    refreshButton.disabled = false;
                    feather.replace(); // Re-initialize feather icons
                });
        }
    }
    
    // Update dashboard elements with new data
    function updateDashboardElements(data) {
        // Update total songs
        const totalSongsElement = document.querySelector('.stat-item h3.text-primary');
        if (totalSongsElement) {
            totalSongsElement.textContent = data.total_songs;
        }
        
        // Update total duration
        const totalDurationElement = document.querySelector('.stat-item h3.text-info');
        if (totalDurationElement) {
            const minutes = Math.floor(data.total_duration / 60);
            const seconds = data.total_duration % 60;
            totalDurationElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }
        
        // Update rating distribution progress bars
        if (data.rating_distribution) {
            for (let rating = 1; rating <= 5; rating++) {
                const progressBar = document.querySelector(`.rating-chart .progress:nth-child(${rating * 2}) .progress-bar`);
                if (progressBar) {
                    const percentage = data.total_songs > 0 ? 
                        (data.rating_distribution[rating] || 0) / data.total_songs * 100 : 0;
                    progressBar.style.width = `${percentage}%`;
                }
                
                const badge = document.querySelector(`.rating-chart .d-flex:nth-child(${rating * 2 - 1}) .badge`);
                if (badge) {
                    const count = data.rating_distribution[rating] || 0;
                    badge.textContent = `${count} song${count !== 1 ? 's' : ''}`;
                }
            }
        }
    }
    
    // Show refresh success indicator
    function showRefreshSuccess() {
        showToast('Dashboard updated successfully', 'success');
    }
    
    // Show refresh error indicator
    function showRefreshError() {
        showToast('Failed to refresh dashboard', 'error');
    }
    
    // Start auto-refresh when page loads
    startAutoRefresh();
    
    // Stop auto-refresh when page is hidden
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            stopAutoRefresh();
        } else {
            startAutoRefresh();
        }
    });
    
    // Stop auto-refresh when user navigates away
    window.addEventListener('beforeunload', stopAutoRefresh);
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : 'success'} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i data-feather="${type === 'error' ? 'alert-circle' : 'check-circle'}" class="me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    // Add to toast container (create if doesn't exist)
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.appendChild(toast);
    
    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 3000
    });
    bsToast.show();
    
    // Replace feather icons
    feather.replace();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

/**
 * Format duration from seconds to MM:SS
 */
function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

/**
 * Confirm deletion with custom message
 */
function confirmDelete(songTitle) {
    return confirm(`Are you sure you want to delete "${songTitle}"?\n\nThis action cannot be undone.`);
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard', 'success');
    }).catch(() => {
        showToast('Failed to copy to clipboard', 'error');
    });
}

/**
 * Export playlist data as JSON
 */
function exportPlaylist() {
    fetch('/api/snapshot')
        .then(response => response.json())
        .then(data => {
            const blob = new Blob([JSON.stringify(data, null, 2)], {
                type: 'application/json'
            });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `playlist-${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            showToast('Playlist exported successfully', 'success');
        })
        .catch(error => {
            console.error('Export failed:', error);
            showToast('Failed to export playlist', 'error');
        });
}

/**
 * Global function for manual dashboard refresh (called by button)
 */
window.refreshData = function() {
    fetch('/api/snapshot')
        .then(response => response.json())
        .then(data => {
            console.log('Dashboard data refreshed:', data);
            location.reload(); // Simple refresh for now
        })
        .catch(error => {
            console.error('Error refreshing data:', error);
            showToast('Failed to refresh data', 'error');
        });
};

// Performance monitoring
let performanceStart = performance.now();

window.addEventListener('load', () => {
    const loadTime = performance.now() - performanceStart;
    console.log(`PlayWise loaded in ${loadTime.toFixed(2)}ms`);
});

// Enhanced error handling for fetch requests
window.addEventListener('unhandledrejection', event => {
    console.error('Unhandled promise rejection:', event.reason);
    showToast('An unexpected error occurred', 'error');
});
