/**
 * Blue's Book - Main Application JavaScript
 * Handles core application logic and initialization
 */

class BluesBookApp {
    constructor() {
        this.apiBaseUrl = 'http://localhost:5000/api/v1';
        this.players = [];
        this.currentPlayer = null;
        this.isLoading = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadInitialData();
    }
    
    setupEventListeners() {
        // Search input
        const searchInput = document.getElementById('playerSearch');
        if (searchInput) {
            searchInput.addEventListener('input', this.handleSearch.bind(this));
            searchInput.addEventListener('focus', this.showSearchSuggestions.bind(this));
            searchInput.addEventListener('blur', this.hideSearchSuggestions.bind(this));
        }
        
        // Filters
        const positionFilter = document.getElementById('positionFilter');
        const sortBy = document.getElementById('sortBy');
        
        if (positionFilter) {
            positionFilter.addEventListener('change', this.handleFilterChange.bind(this));
        }
        
        if (sortBy) {
            sortBy.addEventListener('change', this.handleSortChange.bind(this));
        }
        
        // Modal
        const closeModal = document.getElementById('closeModal');
        const playerModal = document.getElementById('playerModal');
        
        if (closeModal) {
            closeModal.addEventListener('click', this.closeModal.bind(this));
        }
        
        if (playerModal) {
            playerModal.addEventListener('click', (e) => {
                if (e.target === playerModal) {
                    this.closeModal();
                }
            });
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyboardShortcuts.bind(this));
    }
    
    async loadInitialData() {
        try {
            this.showLoading();
            
            // Load random player
            await this.loadRandomPlayer();
            
            // Load squad
            await this.loadSquad();
            
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showError('Failed to load data. Please try again.');
        } finally {
            this.hideLoading();
        }
    }
    
    async loadRandomPlayer() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/players/random`);
            const data = await response.json();
            
            if (data.success) {
                this.displayRandomPlayer(data.data);
            }
        } catch (error) {
            console.error('Error loading random player:', error);
        }
    }
    
    async loadSquad(filters = {}) {
        try {
            const queryParams = new URLSearchParams();
            
            if (filters.position) {
                queryParams.append('position', filters.position);
            }
            
            if (filters.sortBy) {
                queryParams.append('sort_by', filters.sortBy);
            }
            
            const response = await fetch(`${this.apiBaseUrl}/players?${queryParams}`);
            const data = await response.json();
            
            if (data.success) {
                this.players = data.data;
                this.displaySquad(data.data);
            }
        } catch (error) {
            console.error('Error loading squad:', error);
            this.showError('Failed to load squad data.');
        }
    }
    
    displayRandomPlayer(player) {
        const container = document.getElementById('randomPlayer');
        if (!container || !player) return;
        
        container.innerHTML = `
            <div class="flex items-center space-x-4 cursor-pointer" onclick="app.showPlayerModal('${player.player_id}')">
                <img src="${player.image_url}" alt="${player.name}" class="w-16 h-16 rounded-lg object-cover">
                <div>
                    <h4 class="text-xl font-bold">${player.name}</h4>
                    <p class="text-blue-200">${player.position} • #${player.jersey_number}</p>
                </div>
            </div>
        `;
    }
    
    displaySquad(players) {
        const container = document.getElementById('squadGrid');
        if (!container) return;
        
        if (players.length === 0) {
            container.innerHTML = `
                <div class="col-span-full text-center py-12">
                    <div class="text-gray-500 text-lg">No players found</div>
                </div>
            `;
            return;
        }
        
        container.innerHTML = players.map(player => this.createPlayerCard(player)).join('');
    }
    
    createPlayerCard(player) {
        const positionClass = this.getPositionClass(player.position);
        
        return `
            <div class="player-card p-6" onclick="app.showPlayerModal('${player.player_id}')">
                <div class="flex items-center space-x-4 mb-4">
                    <img src="${player.image_url}" alt="${player.name}" class="w-16 h-16 rounded-lg object-cover">
                    <div class="flex-1">
                        <h3 class="text-lg font-bold text-gray-800">${player.name}</h3>
                        <div class="flex items-center space-x-2">
                            <span class="jersey-number">${player.jersey_number}</span>
                            <span class="position-badge ${positionClass}">${player.position}</span>
                        </div>
                    </div>
                </div>
                <div class="text-sm text-gray-600">
                    <p>Age: ${player.age}</p>
                    <p>Nationality: ${player.nationality}</p>
                </div>
            </div>
        `;
    }
    
    getPositionClass(position) {
        const classes = {
            'GK': 'position-gk',
            'DEF': 'position-def',
            'MID': 'position-mid',
            'FWD': 'position-fwd'
        };
        return classes[position] || 'position-mid';
    }
    
    async handleSearch(event) {
        const query = event.target.value.trim();
        
        if (query.length < 2) {
            this.hideSearchSuggestions();
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/players/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.success) {
                this.displaySearchSuggestions(data.data);
            }
        } catch (error) {
            console.error('Error searching players:', error);
        }
    }
    
    displaySearchSuggestions(suggestions) {
        const container = document.getElementById('searchSuggestions');
        if (!container) return;
        
        if (suggestions.length === 0) {
            container.innerHTML = `
                <div class="px-4 py-3 text-gray-500 text-center">
                    No players found
                </div>
            `;
        } else {
            container.innerHTML = suggestions.map(player => `
                <div class="search-suggestion" onclick="app.selectPlayer('${player.player_id}')">
                    <div class="flex items-center space-x-3">
                        <img src="${player.image_url}" alt="${player.name}" class="w-8 h-8 rounded-full object-cover">
                        <div>
                            <div class="font-medium">${player.name}</div>
                            <div class="text-sm text-gray-500">${player.position} • #${player.jersey_number}</div>
                        </div>
                    </div>
                </div>
            `).join('');
        }
        
        container.classList.remove('hidden');
    }
    
    showSearchSuggestions() {
        const container = document.getElementById('searchSuggestions');
        if (container) {
            container.classList.remove('hidden');
        }
    }
    
    hideSearchSuggestions() {
        // Delay hiding to allow clicks on suggestions
        setTimeout(() => {
            const container = document.getElementById('searchSuggestions');
            if (container) {
                container.classList.add('hidden');
            }
        }, 200);
    }
    
    selectPlayer(playerId) {
        this.showPlayerModal(playerId);
        this.hideSearchSuggestions();
        
        // Clear search input
        const searchInput = document.getElementById('playerSearch');
        if (searchInput) {
            searchInput.value = '';
        }
    }
    
    async showPlayerModal(playerId) {
        try {
            this.showLoading();
            
            const response = await fetch(`${this.apiBaseUrl}/players/${playerId}`);
            const data = await response.json();
            
            if (data.success) {
                this.currentPlayer = data.data;
                this.displayPlayerModal(data.data);
                this.openModal();
            } else {
                this.showError('Player not found');
            }
        } catch (error) {
            console.error('Error loading player:', error);
            this.showError('Failed to load player data');
        } finally {
            this.hideLoading();
        }
    }
    
    displayPlayerModal(player) {
        const nameElement = document.getElementById('modalPlayerName');
        const contentElement = document.getElementById('modalContent');
        
        if (nameElement) {
            nameElement.textContent = player.name;
        }
        
        if (contentElement) {
            contentElement.innerHTML = this.createPlayerModalContent(player);
        }
    }
    
    createPlayerModalContent(player) {
        const positionClass = this.getPositionClass(player.position);
        
        return `
            <div class="space-y-6">
                <!-- Player Header -->
                <div class="flex items-center space-x-6">
                    <img src="${player.image_url}" alt="${player.name}" class="w-24 h-24 rounded-lg object-cover">
                    <div>
                        <div class="flex items-center space-x-3 mb-2">
                            <span class="jersey-number text-lg">${player.jersey_number}</span>
                            <span class="position-badge ${positionClass} text-sm">${player.position}</span>
                        </div>
                        <h4 class="text-xl font-bold text-gray-800">${player.name}</h4>
                        <p class="text-gray-600">${player.nationality} • Age ${player.age}</p>
                    </div>
                </div>
                
                <!-- Player Details -->
                <div class="grid grid-cols-2 gap-4">
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <h5 class="font-semibold text-gray-700 mb-2">Club Information</h5>
                        <p class="text-sm text-gray-600">Years at Club: ${player.years_at_club || 'Unknown'}</p>
                        <p class="text-sm text-gray-600">Signing Fee: ${player.signing_fee || 'Unknown'}</p>
                        <p class="text-sm text-gray-600">Weekly Salary: ${player.weekly_salary || 'Unknown'}</p>
                    </div>
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <h5 class="font-semibold text-gray-700 mb-2">Personal Details</h5>
                        <p class="text-sm text-gray-600">Birth Date: ${player.birth_date || 'Unknown'}</p>
                        <p class="text-sm text-gray-600">Nationality: ${player.nationality}</p>
                        <p class="text-sm text-gray-600">Position: ${player.position}</p>
                    </div>
                </div>
                
                <!-- Fun Facts -->
                ${player.fun_facts && player.fun_facts.length > 0 ? `
                    <div>
                        <h5 class="font-semibold text-gray-700 mb-3">Fun Facts</h5>
                        <div class="space-y-2">
                            ${player.fun_facts.map(fact => `
                                <div class="fun-fact">
                                    <p class="text-sm text-gray-700">${fact}</p>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}
                
                <!-- Last Updated -->
                <div class="text-xs text-gray-500 text-center">
                    Last updated: ${new Date(player.last_updated).toLocaleDateString()}
                </div>
            </div>
        `;
    }
    
    openModal() {
        const modal = document.getElementById('playerModal');
        if (modal) {
            modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }
    }
    
    closeModal() {
        const modal = document.getElementById('playerModal');
        if (modal) {
            modal.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
    }
    
    handleFilterChange(event) {
        const position = event.target.value;
        this.loadSquad({ position, sortBy: document.getElementById('sortBy').value });
    }
    
    handleSortChange(event) {
        const sortBy = event.target.value;
        this.loadSquad({ 
            position: document.getElementById('positionFilter').value, 
            sortBy 
        });
    }
    
    handleKeyboardShortcuts(event) {
        // Escape key to close modal
        if (event.key === 'Escape') {
            this.closeModal();
        }
        
        // Ctrl/Cmd + K to focus search
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
            event.preventDefault();
            const searchInput = document.getElementById('playerSearch');
            if (searchInput) {
                searchInput.focus();
            }
        }
    }
    
    showLoading() {
        this.isLoading = true;
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.classList.remove('hidden');
        }
    }
    
    hideLoading() {
        this.isLoading = false;
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.classList.add('hidden');
        }
    }
    
    showError(message) {
        // Simple error display - could be enhanced with a toast notification
        console.error(message);
        alert(message);
    }
}

// Initialize the application
const app = new BluesBookApp();

