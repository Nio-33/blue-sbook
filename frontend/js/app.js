/**
 * Blue's Book - Main Application JavaScript
 * Handles core application logic and initialization
 */

class BluesBookApp {
    constructor() {
        this.apiBaseUrl = 'http://localhost:5000/api/v1';
        this.players = [];
        this.currentPlayer = null;
        this.featuredPlayer = null;
        this.isLoading = false;
        this.currentFilters = {
            position: '',
            nationality: '',
            sortBy: 'jersey_number'
        };
        
        // Chat state
        this.chatHistory = [];
        this.isTyping = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setDefaultNavigation();
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
        
        // Manager search input
        const managerSearchInput = document.getElementById('managerSearch');
        if (managerSearchInput) {
            managerSearchInput.addEventListener('input', this.handleManagerSearch.bind(this));
            managerSearchInput.addEventListener('focus', this.showManagerSearchSuggestions.bind(this));
            managerSearchInput.addEventListener('blur', this.hideManagerSearchSuggestions.bind(this));
        }
        
        // Filters
        const positionFilter = document.getElementById('positionFilter');
        const sortBy = document.getElementById('sortBy');
        const nationalityFilter = document.getElementById('nationalityFilter');
        const clearFilters = document.getElementById('clearFilters');
        
        if (positionFilter) {
            positionFilter.addEventListener('change', this.handleFilterChange.bind(this));
        }
        
        if (sortBy) {
            sortBy.addEventListener('change', this.handleFilterChange.bind(this));
        }
        
        if (nationalityFilter) {
            nationalityFilter.addEventListener('change', this.handleFilterChange.bind(this));
        }
        
        if (clearFilters) {
            clearFilters.addEventListener('click', this.clearAllFilters.bind(this));
        }
        
        // Random Player Button
        const randomPlayerBtn = document.getElementById('randomPlayerBtn');
        if (randomPlayerBtn) {
            randomPlayerBtn.addEventListener('click', this.loadRandomPlayer.bind(this));
        }
        
        // Featured Player Profile Button
        const featuredPlayerProfile = document.getElementById('featuredPlayerProfile');
        if (featuredPlayerProfile) {
            featuredPlayerProfile.addEventListener('click', () => {
                if (this.featuredPlayer) {
                    this.showPlayerModal(this.featuredPlayer.player_id);
                }
            });
        }
        
        // Load More Button
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', this.loadMorePlayers.bind(this));
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
        
        // Navigation
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', this.handleNavigation.bind(this));
        });
        
        // Chat functionality
        this.setupChatEventListeners();
        
        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyboardShortcuts.bind(this));
    }
    
    setDefaultNavigation() {
        // Set Players as the default active navigation
        const playersNavItem = document.querySelector('[data-section="players"]');
        if (playersNavItem) {
            playersNavItem.classList.add('active');
        }
        
        // Ensure player-specific sections are visible by default
        const playerSpecificSections = ['searchSection', 'filtersSection', 'featuredSection', 'playersSection'];
        playerSpecificSections.forEach(sectionId => {
            const element = document.getElementById(sectionId);
            if (element) {
                element.classList.remove('hidden');
            }
        });
        
        // Hide other sections by default
        const otherSections = ['managerSection', 'statisticsSection', 'chatSection', 'aboutSection'];
        otherSections.forEach(sectionId => {
            const element = document.getElementById(sectionId);
            if (element) {
                element.classList.add('hidden');
            }
        });
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
                this.featuredPlayer = data.data;
                this.displayFeaturedPlayer(data.data);
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
                let players = data.data;
                
                // Apply nationality filter on frontend
                if (filters.nationality) {
                    players = players.filter(player => 
                        player.nationality === filters.nationality
                    );
                }
                
                this.players = players;
                this.displaySquad(players);
            }
        } catch (error) {
            console.error('Error loading squad:', error);
            this.showError('Failed to load squad data.');
        }
    }
    
    displayFeaturedPlayer(player) {
        if (!player) return;
        
        const positionClass = this.getPositionClass(player.position);
        
        // Update featured player elements
        document.getElementById('featuredPlayerName').textContent = player.name;
        document.getElementById('featuredPlayerPosition').className = `position-badge ${positionClass} mr-2`;
        document.getElementById('featuredPlayerPosition').textContent = player.position;
        document.getElementById('featuredPlayerDetails').textContent = `Age ${player.age} • ${player.nationality}`;
        document.getElementById('featuredPlayerJersey').textContent = `#${player.jersey_number}`;
        document.getElementById('featuredPlayerFee').textContent = player.signing_fee || 'Unknown';
        document.getElementById('featuredPlayerYears').textContent = player.years_at_club || 'Unknown';
        document.getElementById('featuredPlayerSalary').textContent = player.weekly_salary || 'Unknown';
        document.getElementById('featuredPlayerFact').textContent = 
            player.fun_facts && player.fun_facts.length > 0 ? player.fun_facts[0] : 'No fun facts available';
        
        // Show player image if available
        const image = document.getElementById('featuredPlayerImage');
        const placeholder = document.getElementById('featuredPlayerPlaceholder');
        if (player.image_url && player.image_url !== 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=300&fit=crop&crop=face') {
            image.src = player.image_url;
            image.style.display = 'block';
            placeholder.style.display = 'none';
        } else {
            image.style.display = 'none';
            placeholder.style.display = 'flex';
        }
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
            <div class="player-card bg-white rounded-xl shadow-md overflow-hidden fade-in" onclick="app.showPlayerModal('${player.player_id}')">
                <div class="h-48 bg-gray-300 relative">
                    <div class="absolute top-4 right-4 bg-white rounded-full w-10 h-10 flex items-center justify-center shadow">
                        <span class="font-bold text-blue-800">${player.jersey_number}</span>
                    </div>
                    <div class="absolute inset-0 flex items-center justify-center">
                        <i class="fas fa-user text-6xl text-gray-400"></i>
                    </div>
                </div>
                <div class="p-5">
                    <h3 class="text-xl font-bold text-gray-800">${player.name}</h3>
                    <div class="flex items-center mt-1">
                        <span class="position-badge ${positionClass} mr-2">${player.position}</span>
                        <span class="text-sm text-gray-600">Age ${player.age}</span>
                    </div>
                    <div class="mt-4 grid grid-cols-2 gap-2">
                        <div>
                            <p class="text-gray-500 text-xs">Signing Fee</p>
                            <p class="text-sm font-semibold">${player.signing_fee || 'Unknown'}</p>
                        </div>
                        <div>
                            <p class="text-gray-500 text-xs">Nationality</p>
                            <p class="text-sm font-semibold">${player.nationality}</p>
                        </div>
                    </div>
                    <button class="mt-4 w-full bg-blue-100 text-blue-800 py-2 rounded-md font-medium hover:bg-blue-200 transition">
                        View Profile
                    </button>
                </div>
            </div>
        `;
    }
    
    getPositionClass(position) {
        const classes = {
            'GK': 'position-gk',
            'DEF': 'position-df',
            'MID': 'position-mf',
            'FWD': 'position-fw'
        };
        return classes[position] || 'position-mf';
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
                <div class="p-2 border-b border-gray-200 hover:bg-gray-50 cursor-pointer last:border-b-0" onclick="app.selectPlayer('${player.player_id}')">
                    <div class="flex items-center">
                        <div class="w-10 h-10 bg-gray-200 rounded-full mr-3 flex items-center justify-center">
                            <i class="fas fa-user text-gray-400"></i>
                        </div>
                        <div>
                            <p class="font-semibold">${player.name}</p>
                            <p class="text-sm text-gray-600">${player.position} • #${player.jersey_number}</p>
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
    
    async handleManagerSearch(event) {
        const query = event.target.value.trim();
        
        if (query.length < 2) {
            this.hideManagerSearchSuggestions();
            this.hideManagerSearchResults();
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/managers/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.success) {
                this.displayManagerSearchSuggestions(data.data);
                this.displayManagerSearchResults(data.data);
            }
        } catch (error) {
            console.error('Error searching managers:', error);
        }
    }
    
    displayManagerSearchSuggestions(suggestions) {
        const container = document.getElementById('managerSearchSuggestions');
        if (!container) return;
        
        if (suggestions.length === 0) {
            container.innerHTML = `
                <div class="px-4 py-3 text-gray-500 text-center">
                    No managers found
                </div>
            `;
        } else {
            container.innerHTML = suggestions.map(manager => `
                <div class="p-2 border-b border-gray-200 hover:bg-gray-50 cursor-pointer last:border-b-0" onclick="app.selectManager('${manager.manager_id}')">
                    <div class="flex items-center">
                        <div class="w-10 h-10 bg-gray-200 rounded-full mr-3 flex items-center justify-center">
                            <i class="fas fa-user-tie text-gray-400"></i>
                        </div>
                        <div>
                            <p class="font-semibold">${manager.name}</p>
                            <p class="text-sm text-gray-600">${manager.nationality} • ${manager.years_at_club}</p>
                        </div>
                    </div>
                </div>
            `).join('');
        }
        
        container.classList.remove('hidden');
    }
    
    displayManagerSearchResults(managers) {
        const container = document.getElementById('managerSearchContainer');
        const resultsSection = document.getElementById('managerSearchResults');
        
        if (!container || !resultsSection) return;
        
        if (managers.length === 0) {
            resultsSection.classList.add('hidden');
            return;
        }
        
        container.innerHTML = managers.map(manager => this.createManagerCard(manager)).join('');
        resultsSection.classList.remove('hidden');
    }
    
    createManagerCard(manager) {
        return `
            <div class="bg-white rounded-xl shadow-lg overflow-hidden mb-6 fade-in">
                <div class="md:flex">
                    <div class="md:flex-shrink-0 md:w-1/3">
                        <div class="h-64 md:h-full bg-gray-300 relative">
                            <img class="w-full h-full object-cover manager-image" style="display: none;" alt="${manager.name}">
                            <div class="manager-image-placeholder absolute inset-0 flex items-center justify-center">
                                <i class="fas fa-user-tie text-6xl text-gray-400"></i>
                            </div>
                        </div>
                    </div>
                    <div class="p-8 md:w-2/3">
                        <h4 class="text-3xl font-bold text-gray-800 mb-2">${manager.name}</h4>
                        <p class="text-lg text-gray-600 mb-4">${manager.nationality} • Age ${manager.age}</p>
                        
                        <div class="grid grid-cols-2 gap-6 mb-6">
                            <div>
                                <h5 class="font-semibold text-gray-700 mb-2">Career Information</h5>
                                <p class="text-sm text-gray-600 mb-1">Age: ${manager.age}</p>
                                <p class="text-sm text-gray-600 mb-1">Nationality: ${manager.nationality}</p>
                                <p class="text-sm text-gray-600">Years at Club: ${manager.years_at_club}</p>
                            </div>
                            <div>
                                <h5 class="font-semibold text-gray-700 mb-2">Previous Clubs</h5>
                                <div class="text-sm text-gray-600">
                                    ${manager.previous_clubs ? manager.previous_clubs.map(club => `<p class="mb-1">• ${club}</p>`).join('') : '<p>No previous clubs listed</p>'}
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-6">
                            <h5 class="font-semibold text-gray-700 mb-2">Achievements</h5>
                            <div class="space-y-1">
                                ${manager.achievements ? manager.achievements.map(achievement => `
                                    <div class="flex items-center text-sm text-gray-600 mb-1">
                                        <i class="fas fa-trophy text-yellow-500 mr-2"></i>
                                        ${achievement}
                                    </div>
                                `).join('') : '<p class="text-sm text-gray-600">No achievements listed</p>'}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    selectManager(managerId) {
        // For now, just scroll to the selected manager
        const managerCards = document.querySelectorAll('#managerSearchContainer > div');
        managerCards.forEach(card => {
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
        
        this.hideManagerSearchSuggestions();
        
        // Clear search input
        const searchInput = document.getElementById('managerSearch');
        if (searchInput) {
            searchInput.value = '';
        }
    }
    
    showManagerSearchSuggestions() {
        const container = document.getElementById('managerSearchSuggestions');
        if (container) {
            container.classList.remove('hidden');
        }
    }
    
    hideManagerSearchSuggestions() {
        // Delay hiding to allow clicks on suggestions
        setTimeout(() => {
            const container = document.getElementById('managerSearchSuggestions');
            if (container) {
                container.classList.add('hidden');
            }
        }, 200);
    }
    
    hideManagerSearchResults() {
        const resultsSection = document.getElementById('managerSearchResults');
        if (resultsSection) {
            resultsSection.classList.add('hidden');
        }
    }
    
    clearManagerSearch() {
        // Clear search input
        const searchInput = document.getElementById('managerSearch');
        if (searchInput) {
            searchInput.value = '';
        }
        
        // Hide search suggestions and results
        this.hideManagerSearchSuggestions();
        this.hideManagerSearchResults();
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
        // Update current filters
        this.currentFilters.position = document.getElementById('positionFilter').value;
        this.currentFilters.nationality = document.getElementById('nationalityFilter').value;
        this.currentFilters.sortBy = document.getElementById('sortBy').value;
        
        // Reload squad with new filters
        this.loadSquad(this.currentFilters);
    }
    
    clearAllFilters() {
        // Reset filter form
        document.getElementById('positionFilter').value = '';
        document.getElementById('nationalityFilter').value = '';
        document.getElementById('sortBy').value = 'jersey_number';
        
        // Reset internal filters
        this.currentFilters = {
            position: '',
            nationality: '',
            sortBy: 'jersey_number'
        };
        
        // Reload squad
        this.loadSquad(this.currentFilters);
    }
    
    loadMorePlayers() {
        // This would typically load more players from API
        // For now, just show an alert
        const button = document.getElementById('loadMoreBtn');
        const originalText = button.textContent;
        
        button.textContent = 'Loading...';
        button.disabled = true;
        
        setTimeout(() => {
            alert('All players are already loaded!');
            button.textContent = originalText;
            button.disabled = false;
        }, 1000);
    }
    
    handleNavigation(event) {
        event.preventDefault();
        const section = event.target.dataset.section;
        
        // Update navigation active states
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        event.target.classList.add('active');
        
        // Hide all main sections
        const sections = ['playersSection', 'managerSection', 'statisticsSection', 'chatSection', 'aboutSection'];
        sections.forEach(sectionId => {
            const element = document.getElementById(sectionId);
            if (element) {
                element.classList.add('hidden');
            }
        });
        
        // Hide/show player-specific sections based on navigation
        const playerSpecificSections = ['searchSection', 'filtersSection', 'featuredSection'];
        playerSpecificSections.forEach(sectionId => {
            const element = document.getElementById(sectionId);
            if (element) {
                if (section === 'players') {
                    element.classList.remove('hidden');
                } else {
                    element.classList.add('hidden');
                }
            }
        });
        
        // Show selected section and load data
        switch(section) {
            case 'players':
                this.showSection('playersSection');
                // Players data is already loaded
                break;
            case 'manager':
                this.showSection('managerSection');
                this.loadManagerData();
                this.clearManagerSearch();
                break;
            case 'statistics':
                this.showSection('statisticsSection');
                this.loadStatisticsData();
                break;
            case 'chat':
                this.showSection('chatSection');
                this.loadChatData();
                break;
            case 'about':
                this.showSection('aboutSection');
                // About section is static, no data loading needed
                break;
        }
    }
    
    showSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.classList.remove('hidden');
            section.classList.add('fade-in');
        }
    }
    
    async loadManagerData() {
        try {
            // Show loading state
            this.showSectionLoading('managerSection');
            
            const response = await fetch(`${this.apiBaseUrl}/managers/current`);
            const data = await response.json();
            
            if (data.success) {
                this.displayManagerData(data.data);
            } else {
                console.error('Failed to load manager data:', data.error);
                this.showSectionError('managerSection', 'Failed to load manager data');
            }
        } catch (error) {
            console.error('Error loading manager data:', error);
            this.showSectionError('managerSection', 'Error connecting to server');
        } finally {
            this.hideSectionLoading('managerSection');
        }
    }
    
    displayManagerData(manager) {
        if (!manager) return;
        
        // Update manager information
        document.getElementById('managerName').textContent = manager.name || 'Unknown';
        document.getElementById('managerDetails').textContent = `${manager.nationality || 'Unknown'} • Age ${manager.age || 'Unknown'}`;
        document.getElementById('managerAge').textContent = manager.age || 'Unknown';
        document.getElementById('managerNationality').textContent = manager.nationality || 'Unknown';
        document.getElementById('managerYears').textContent = manager.years_at_club || 'Unknown';
        
        // Display previous clubs
        const previousClubsContainer = document.getElementById('managerPreviousClubs');
        if (manager.previous_clubs && manager.previous_clubs.length > 0) {
            previousClubsContainer.innerHTML = manager.previous_clubs.map(club => 
                `<p class="mb-1">• ${club}</p>`
            ).join('');
        } else {
            previousClubsContainer.innerHTML = '<p>No previous clubs listed</p>';
        }
        
        // Display achievements
        const achievementsContainer = document.getElementById('managerAchievements');
        if (manager.achievements && manager.achievements.length > 0) {
            achievementsContainer.innerHTML = manager.achievements.map(achievement => 
                `<div class="flex items-center text-sm text-gray-600 mb-1">
                    <i class="fas fa-trophy text-yellow-500 mr-2"></i>
                    ${achievement}
                </div>`
            ).join('');
        } else {
            achievementsContainer.innerHTML = '<p class="text-sm text-gray-600">No achievements listed</p>';
        }
        
        // Handle manager image
        const image = document.getElementById('managerImage');
        const placeholder = document.getElementById('managerImagePlaceholder');
        if (manager.image_url && manager.image_url !== 'https://images.unsplash.com/photo-1542909168-82c3e7fdca5c?w=300&h=300&fit=crop&crop=face') {
            image.src = manager.image_url;
            image.style.display = 'block';
            placeholder.style.display = 'none';
        } else {
            image.style.display = 'none';
            placeholder.style.display = 'flex';
        }
    }
    
    async loadStatisticsData() {
        try {
            // Show loading state
            this.showSectionLoading('statisticsSection');
            
            // Load advanced statistics from API
            const response = await fetch(`${this.apiBaseUrl}/players/statistics/advanced`);
            const data = await response.json();
            
            if (data.success) {
                this.displayAdvancedStatistics(data.data);
            } else {
                this.showSectionError('statisticsSection', 'Failed to load statistics');
            }
        } catch (error) {
            console.error('Error loading statistics data:', error);
            this.showSectionError('statisticsSection', 'Error calculating statistics');
        } finally {
            this.hideSectionLoading('statisticsSection');
        }
    }
    
    displayAdvancedStatistics(stats) {
        if (!stats) return;
        
        // Update basic metrics
        const basic = stats.basic_metrics;
        document.getElementById('totalPlayers').textContent = basic.total_players;
        document.getElementById('averageAge').textContent = basic.average_age;
        document.getElementById('totalValue').textContent = `£${basic.total_value}M`;
        document.getElementById('totalNationalities').textContent = basic.nationalities;
        document.getElementById('academyGraduates').textContent = basic.academy_graduates;
        document.getElementById('internationalPlayers').textContent = basic.international_players;
        document.getElementById('weeklyWageBill').textContent = `£${(basic.weekly_wage_bill / 1000).toFixed(0)}k`;
        document.getElementById('avgMarketValue').textContent = `£${basic.avg_market_value}M`;
        
        // Position breakdown (legacy)
        this.displayPositionBreakdown(stats.tactical_analysis.position_depth);
        
        // Top signings (legacy - we'll calculate from financial data)
        this.displayTopSignings(stats.financial_analysis);
        
        // Financial Analysis
        this.displayFinancialAnalysis(stats.financial_analysis);
        
        // Transfer Analysis
        this.displayTransferAnalysis(stats.financial_analysis);
        
        // Squad Demographics
        this.displayAgeDistribution(stats.squad_demographics.age_groups);
        this.displayNationalityBreakdown(stats.squad_demographics.nationality_breakdown);
        this.displayExperienceLevels(stats.squad_demographics.experience_levels);
        
        // Tactical Analysis
        this.displayTacticalInsights(stats.tactical_analysis);
        this.displayPhysicalStats(stats.tactical_analysis);
        
        // Contract & Timeline
        this.displayContractTimeline(stats.contract_timeline);
        this.displaySquadEvolution(stats.contract_timeline);
        
        // Performance Metrics
        this.displayTrophyWinners(stats.performance_metrics);
        this.displayInternationalExperience(stats.performance_metrics);
        this.displayPreviousClubs(stats.performance_metrics);
    }
    
    displayPositionBreakdown(positionDepth) {
        const totalPlayers = Object.values(positionDepth).reduce((sum, count) => sum + count, 0);
        const container = document.getElementById('positionBreakdown');
        
        container.innerHTML = Object.entries(positionDepth).map(([position, count]) => {
            const percentage = Math.round((count / totalPlayers) * 100);
            const positionName = {
                'GK': 'Goalkeepers',
                'DEF': 'Defenders', 
                'MID': 'Midfielders',
                'FWD': 'Forwards'
            }[position] || position;
            
            return `
                <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-gray-700">${positionName}</span>
                    <div class="flex items-center">
                        <div class="w-24 bg-gray-200 rounded-full h-2 mr-3">
                            <div class="bg-blue-600 h-2 rounded-full" style="width: ${percentage}%"></div>
                        </div>
                        <span class="text-sm text-gray-600">${count}</span>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    displayTopSignings(financialData) {
        // This would need actual player data with signing fees
        // For now, we'll create a placeholder
        const container = document.getElementById('topSignings');
        container.innerHTML = `
            <div class="text-center text-gray-500 py-8">
                <i class="fas fa-chart-line text-4xl mb-4"></i>
                <p>Top signings data available in position investment analysis</p>
            </div>
        `;
    }
    
    displayFinancialAnalysis(financialData) {
        const container = document.getElementById('financialAnalysis');
        
        container.innerHTML = `
            <div class="space-y-3">
                <h4 class="font-semibold text-gray-700">Investment by Position</h4>
                ${Object.entries(financialData.position_investment).map(([position, amount]) => `
                    <div class="flex justify-between items-center">
                        <span class="text-sm text-gray-600">${position}</span>
                        <span class="font-medium">£${amount.toFixed(1)}M</span>
                    </div>
                `).join('')}
                
                <div class="mt-4 pt-4 border-t border-gray-200">
                    <h4 class="font-semibold text-gray-700 mb-2">Salary Distribution</h4>
                    ${Object.entries(financialData.salary_distribution).map(([range, count]) => `
                        <div class="flex justify-between items-center">
                            <span class="text-sm text-gray-600">${range}</span>
                            <span class="font-medium">${count} players</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    displayTransferAnalysis(financialData) {
        const container = document.getElementById('transferAnalysis');
        const freeVsPaid = financialData.free_vs_paid;
        
        container.innerHTML = `
            <div class="space-y-4">
                <div>
                    <h4 class="font-semibold text-gray-700 mb-3">Spending by Year</h4>
                    ${Object.entries(financialData.spending_by_year).map(([year, amount]) => `
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-sm text-gray-600">${year}</span>
                            <span class="font-medium">£${amount.toFixed(1)}M</span>
                        </div>
                    `).join('')}
                </div>
                
                <div class="pt-4 border-t border-gray-200">
                    <h4 class="font-semibold text-gray-700 mb-3">Transfer Types</h4>
                    <div class="grid grid-cols-2 gap-4">
                        <div class="text-center p-3 bg-green-50 rounded-lg">
                            <div class="text-2xl font-bold text-green-600">${freeVsPaid.free}</div>
                            <div class="text-sm text-gray-600">Free Transfers</div>
                        </div>
                        <div class="text-center p-3 bg-blue-50 rounded-lg">
                            <div class="text-2xl font-bold text-blue-600">${freeVsPaid.paid}</div>
                            <div class="text-sm text-gray-600">Paid Transfers</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    displayAgeDistribution(ageGroups) {
        const container = document.getElementById('ageDistribution');
        const total = Object.values(ageGroups).reduce((sum, count) => sum + count, 0);
        
        container.innerHTML = Object.entries(ageGroups).map(([range, count]) => {
            const percentage = Math.round((count / total) * 100);
            return `
                <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-gray-700">${range}</span>
                    <div class="flex items-center">
                        <div class="w-16 bg-gray-200 rounded-full h-2 mr-3">
                            <div class="bg-blue-600 h-2 rounded-full" style="width: ${percentage}%"></div>
                        </div>
                        <span class="text-sm text-gray-600">${count}</span>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    displayNationalityBreakdown(nationalityData) {
        const container = document.getElementById('nationalityBreakdown');
        
        container.innerHTML = Object.entries(nationalityData)
            .sort((a, b) => b[1] - a[1])
            .map(([country, count]) => `
                <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-600">${country}</span>
                    <span class="font-medium">${count}</span>
                </div>
            `).join('');
    }
    
    displayExperienceLevels(experienceData) {
        const container = document.getElementById('experienceLevels');
        const total = Object.values(experienceData).reduce((sum, count) => sum + count, 0);
        
        container.innerHTML = Object.entries(experienceData).map(([level, count]) => {
            const percentage = Math.round((count / total) * 100);
            return `
                <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-gray-700">${level}</span>
                    <div class="flex items-center">
                        <div class="w-16 bg-gray-200 rounded-full h-2 mr-3">
                            <div class="bg-purple-600 h-2 rounded-full" style="width: ${percentage}%"></div>
                        </div>
                        <span class="text-sm text-gray-600">${count}</span>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    displayTacticalInsights(tacticalData) {
        const container = document.getElementById('tacticalInsights');
        
        container.innerHTML = `
            <div class="space-y-4">
                <div>
                    <h4 class="font-semibold text-gray-700 mb-3">Preferred Foot</h4>
                    ${Object.entries(tacticalData.foot_preference).map(([foot, count]) => `
                        <div class="flex justify-between items-center">
                            <span class="text-sm text-gray-600">${foot} foot</span>
                            <span class="font-medium">${count} players</span>
                        </div>
                    `).join('')}
                </div>
                
                <div class="pt-4 border-t border-gray-200">
                    <h4 class="font-semibold text-gray-700 mb-3">Formation Flexibility</h4>
                    <div class="grid grid-cols-2 gap-2 text-sm">
                        ${Object.entries(tacticalData.position_depth).map(([pos, count]) => `
                            <div class="flex justify-between">
                                <span class="text-gray-600">${pos}</span>
                                <span class="font-medium">${count}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }
    
    displayPhysicalStats(tacticalData) {
        const container = document.getElementById('physicalStats');
        
        container.innerHTML = `
            <div class="space-y-3">
                <h4 class="font-semibold text-gray-700 mb-3">Average Height by Position</h4>
                ${Object.entries(tacticalData.avg_height_by_position).map(([position, height]) => `
                    <div class="flex justify-between items-center">
                        <span class="text-sm text-gray-600">${position}</span>
                        <span class="font-medium">${height}cm</span>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    displayContractTimeline(contractData) {
        const container = document.getElementById('contractTimeline');
        
        container.innerHTML = `
            <div class="space-y-3">
                <h4 class="font-semibold text-gray-700 mb-3">Contract Expiry Years</h4>
                ${Object.entries(contractData.contract_expiry_timeline)
                    .sort((a, b) => a[0] - b[0])
                    .map(([year, count]) => `
                        <div class="flex justify-between items-center">
                            <span class="text-sm text-gray-600">${year}</span>
                            <span class="font-medium">${count} players</span>
                        </div>
                    `).join('')}
            </div>
        `;
    }
    
    displaySquadEvolution(contractData) {
        const container = document.getElementById('squadEvolution');
        
        container.innerHTML = `
            <div class="space-y-3">
                <h4 class="font-semibold text-gray-700 mb-3">Squad by Arrival Period</h4>
                ${Object.entries(contractData.arrival_periods).map(([period, count]) => `
                    <div class="flex justify-between items-center">
                        <span class="text-sm text-gray-600">${period}</span>
                        <span class="font-medium">${count} players</span>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    displayTrophyWinners(performanceData) {
        const container = document.getElementById('trophyWinners');
        
        container.innerHTML = `
            <div class="text-center">
                <div class="text-3xl font-bold text-yellow-600 mb-2">${performanceData.trophy_winners}</div>
                <div class="text-sm text-gray-600 mb-4">Trophy Winners</div>
                
                <div class="text-2xl font-bold text-yellow-500 mb-2">${performanceData.total_trophies}</div>
                <div class="text-sm text-gray-600">Total Trophies</div>
            </div>
        `;
    }
    
    displayInternationalExperience(performanceData) {
        const container = document.getElementById('internationalExperience');
        
        container.innerHTML = `
            <div class="text-center">
                <div class="text-3xl font-bold text-blue-600 mb-2">${performanceData.international_caps}</div>
                <div class="text-sm text-gray-600 mb-4">Total Caps</div>
                
                <div class="text-2xl font-bold text-blue-500 mb-2">${performanceData.avg_international_caps}</div>
                <div class="text-sm text-gray-600">Average per Player</div>
            </div>
        `;
    }
    
    displayPreviousClubs(performanceData) {
        const container = document.getElementById('previousClubs');
        
        container.innerHTML = Object.entries(performanceData.previous_clubs)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 8)
            .map(([club, count]) => `
                <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-600">${club}</span>
                    <span class="font-medium">${count}</span>
                </div>
            `).join('');
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
    
    showSectionLoading(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'section-loading flex items-center justify-center py-12';
            loadingDiv.innerHTML = `
                <div class="text-center">
                    <div class="loading-spinner mx-auto mb-4"></div>
                    <p class="text-gray-600">Loading...</p>
                </div>
            `;
            section.appendChild(loadingDiv);
        }
    }
    
    hideSectionLoading(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            const loadingDiv = section.querySelector('.section-loading');
            if (loadingDiv) {
                loadingDiv.remove();
            }
        }
    }
    
    showSectionError(sectionId, message) {
        const section = document.getElementById(sectionId);
        if (section) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'section-error bg-red-50 border border-red-200 rounded-lg p-6 mx-4 my-8';
            errorDiv.innerHTML = `
                <div class="flex items-center">
                    <i class="fas fa-exclamation-triangle text-red-500 text-xl mr-3"></i>
                    <div>
                        <h3 class="text-red-800 font-semibold">Error Loading Data</h3>
                        <p class="text-red-600 mt-1">${message}</p>
                        <button onclick="location.reload()" class="mt-3 bg-red-600 text-white px-4 py-2 rounded-md text-sm hover:bg-red-700 transition">
                            Retry
                        </button>
                    </div>
                </div>
            `;
            section.appendChild(errorDiv);
        }
    }
    
    // Chat functionality methods
    setupChatEventListeners() {
        const chatSendButton = document.getElementById('chatSendButton');
        const chatInput = document.getElementById('chatInput');
        
        if (chatSendButton) {
            chatSendButton.addEventListener('click', this.sendMessage.bind(this));
        }
        
        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
            
            chatInput.addEventListener('input', this.handleChatInputChange.bind(this));
            chatInput.addEventListener('input', this.updateCharacterCounter.bind(this));
        }
        
        // Suggested questions
        const suggestedButtons = document.querySelectorAll('.suggested-question');
        suggestedButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const question = e.target.textContent.trim();
                this.sendSuggestedQuestion(question);
            });
        });
    }
    
    async loadChatData() {
        try {
            // Load suggested questions
            await this.loadSuggestedQuestions();
            
            // Check chat health
            await this.checkChatHealth();
            
            // Initialize chat if empty
            if (this.chatHistory.length === 0) {
                this.initializeChat();
            }
        } catch (error) {
            console.error('Error loading chat data:', error);
            this.showChatError('Failed to initialize chat');
        }
    }
    
    async loadSuggestedQuestions() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/chat/suggestions`);
            const data = await response.json();
            
            if (data.success) {
                this.displaySuggestedQuestions(data.data.slice(0, 4)); // Show first 4
            }
        } catch (error) {
            console.error('Error loading suggested questions:', error);
        }
    }
    
    displaySuggestedQuestions(questions) {
        const container = document.getElementById('chatSuggestedQuestions');
        if (!container) return;
        
        container.innerHTML = questions.map(question => `
            <button class="suggested-question bg-blue-50 text-blue-700 px-4 py-2 rounded-lg text-sm hover:bg-blue-100 transition">
                ${question}
            </button>
        `).join('');
        
        // Re-attach event listeners
        const suggestedButtons = container.querySelectorAll('.suggested-question');
        suggestedButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const question = e.target.textContent.trim();
                this.sendSuggestedQuestion(question);
            });
        });
    }
    
    async checkChatHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/chat/health`);
            const data = await response.json();
            
            const healthIndicator = document.getElementById('chatHealthIndicator');
            if (healthIndicator) {
                if (data.healthy) {
                    healthIndicator.className = 'w-3 h-3 bg-green-500 rounded-full';
                    healthIndicator.title = 'Chat service is online';
                } else {
                    healthIndicator.className = 'w-3 h-3 bg-red-500 rounded-full';
                    healthIndicator.title = 'Chat service is offline';
                }
            }
        } catch (error) {
            console.error('Error checking chat health:', error);
        }
    }
    
    initializeChat() {
        const welcomeMessage = {
            type: 'ai',
            message: "Hello! I'm your Chelsea FC history assistant. Ask me anything about the club's history, players, managers, trophies, and memorable moments. What would you like to know?",
            timestamp: Date.now()
        };
        
        this.chatHistory.push(welcomeMessage);
        this.displayChatMessage(welcomeMessage);
    }
    
    async sendMessage() {
        const chatInput = document.getElementById('chatInput');
        const message = chatInput.value.trim();
        
        if (!message) return;
        
        // Clear input and disable send button
        chatInput.value = '';
        this.updateSendButton(false);
        
        // Add user message to chat
        const userMessage = {
            type: 'user',
            message: message,
            timestamp: Date.now()
        };
        
        this.chatHistory.push(userMessage);
        this.displayChatMessage(userMessage);
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/chat/send`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    history: this.chatHistory.slice(-10) // Send last 10 messages for context
                })
            });
            
            const data = await response.json();
            
            this.hideTypingIndicator();
            
            if (data.success) {
                const aiMessage = {
                    type: 'ai',
                    message: data.message,
                    timestamp: Date.now(),
                    queryTime: data.query_time
                };
                
                this.chatHistory.push(aiMessage);
                this.displayChatMessage(aiMessage);
            } else {
                this.showChatError(data.error || 'Failed to get response');
            }
        } catch (error) {
            this.hideTypingIndicator();
            console.error('Error sending message:', error);
            this.showChatError('Connection error. Please try again.');
        }
    }
    
    async sendSuggestedQuestion(question) {
        const chatInput = document.getElementById('chatInput');
        chatInput.value = question;
        await this.sendMessage();
    }
    
    displayChatMessage(message) {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.type === 'user' ? 'user-message' : 'ai-message'} mb-4 fade-in`;
        
        const time = new Date(message.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        if (message.type === 'user') {
            messageDiv.innerHTML = `
                <div class="flex justify-end">
                    <div class="bg-blue-500 text-white rounded-lg px-4 py-2 max-w-md">
                        <p class="text-sm">${this.escapeHtml(message.message)}</p>
                        <p class="text-xs opacity-75 mt-1">${time}</p>
                    </div>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="flex items-start space-x-3">
                    <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <i class="fas fa-robot text-blue-600 text-sm"></i>
                    </div>
                    <div class="bg-gray-100 rounded-lg px-4 py-2 max-w-md">
                        <p class="text-sm text-gray-800">${this.formatAIMessage(message.message)}</p>
                        <div class="flex items-center justify-between mt-1">
                            <p class="text-xs text-gray-500">${time}</p>
                            ${message.queryTime ? `<p class="text-xs text-gray-400">${message.queryTime}</p>` : ''}
                        </div>
                    </div>
                </div>
            `;
        }
        
        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) return;
        
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typingIndicator';
        typingDiv.className = 'message ai-message mb-4';
        typingDiv.innerHTML = `
            <div class="flex items-start space-x-3">
                <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-robot text-blue-600 text-sm"></i>
                </div>
                <div class="bg-gray-100 rounded-lg px-4 py-2">
                    <div class="typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        this.isTyping = true;
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
        this.isTyping = false;
    }
    
    handleChatInputChange(event) {
        const message = event.target.value.trim();
        this.updateSendButton(message.length > 0 && !this.isTyping);
    }
    
    updateSendButton(enabled) {
        const sendButton = document.getElementById('chatSendButton');
        if (sendButton) {
            sendButton.disabled = !enabled;
            sendButton.className = enabled 
                ? 'bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors'
                : 'bg-gray-400 text-white px-6 py-3 rounded-lg font-medium cursor-not-allowed disabled:bg-gray-400 disabled:cursor-not-allowed';
        }
    }
    
    updateCharacterCounter(event) {
        const charCounter = document.getElementById('charCounter');
        if (charCounter) {
            const currentLength = event.target.value.length;
            const maxLength = 500;
            charCounter.textContent = `${currentLength}/${maxLength}`;
            
            // Change color as user approaches limit
            if (currentLength > 450) {
                charCounter.className = 'absolute right-3 top-3 text-xs text-red-500';
            } else if (currentLength > 400) {
                charCounter.className = 'absolute right-3 top-3 text-xs text-orange-500';
            } else {
                charCounter.className = 'absolute right-3 top-3 text-xs text-gray-400';
            }
        }
    }
    
    scrollToBottom() {
        const messagesContainer = document.getElementById('chatMessages');
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    formatAIMessage(message) {
        // Basic formatting for AI messages
        return this.escapeHtml(message)
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }
    
    showChatError(message) {
        const errorMessage = {
            type: 'ai',
            message: `❌ ${message}`,
            timestamp: Date.now()
        };
        
        this.displayChatMessage(errorMessage);
    }
}

// Initialize the application
const app = new BluesBookApp();

