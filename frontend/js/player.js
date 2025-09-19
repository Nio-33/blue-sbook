/**
 * Blue's Book - Player Management
 * Handles player-specific functionality and display
 */

class PlayerManager {
    constructor(app) {
        this.app = app;
        this.favorites = this.loadFavorites();
        this.recentPlayers = this.loadRecentPlayers();
    }
    
    loadFavorites() {
        try {
            const stored = localStorage.getItem('bluesbook_favorites');
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.error('Error loading favorites:', error);
            return [];
        }
    }
    
    saveFavorites() {
        try {
            localStorage.setItem('bluesbook_favorites', JSON.stringify(this.favorites));
        } catch (error) {
            console.error('Error saving favorites:', error);
        }
    }
    
    loadRecentPlayers() {
        try {
            const stored = localStorage.getItem('bluesbook_recent');
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.error('Error loading recent players:', error);
            return [];
        }
    }
    
    saveRecentPlayers() {
        try {
            localStorage.setItem('bluesbook_recent', JSON.stringify(this.recentPlayers));
        } catch (error) {
            console.error('Error saving recent players:', error);
        }
    }
    
    addToFavorites(playerId) {
        if (!this.favorites.includes(playerId)) {
            this.favorites.push(playerId);
            this.saveFavorites();
            this.updateFavoriteUI(playerId, true);
        }
    }
    
    removeFromFavorites(playerId) {
        const index = this.favorites.indexOf(playerId);
        if (index > -1) {
            this.favorites.splice(index, 1);
            this.saveFavorites();
            this.updateFavoriteUI(playerId, false);
        }
    }
    
    isFavorite(playerId) {
        return this.favorites.includes(playerId);
    }
    
    addToRecent(playerId) {
        // Remove if already exists
        const index = this.recentPlayers.indexOf(playerId);
        if (index > -1) {
            this.recentPlayers.splice(index, 1);
        }
        
        // Add to beginning
        this.recentPlayers.unshift(playerId);
        
        // Keep only last 10
        this.recentPlayers = this.recentPlayers.slice(0, 10);
        
        this.saveRecentPlayers();
    }
    
    getRecentPlayers() {
        return this.recentPlayers;
    }
    
    updateFavoriteUI(playerId, isFavorite) {
        const button = document.querySelector(`[data-player-id="${playerId}"] .favorite-btn`);
        if (button) {
            if (isFavorite) {
                button.innerHTML = `
                    <svg class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"></path>
                    </svg>
                `;
                button.classList.add('text-red-500');
                button.classList.remove('text-gray-400');
            } else {
                button.innerHTML = `
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>
                `;
                button.classList.add('text-gray-400');
                button.classList.remove('text-red-500');
            }
        }
    }
    
    createPlayerCard(player) {
        const positionClass = this.app.getPositionClass(player.position);
        const isFavorite = this.isFavorite(player.player_id);
        
        return `
            <div class="player-card p-6 relative" data-player-id="${player.player_id}" onclick="app.showPlayerModal('${player.player_id}')">
                <!-- Favorite Button -->
                <button class="absolute top-4 right-4 favorite-btn ${isFavorite ? 'text-red-500' : 'text-gray-400'} hover:text-red-500 transition-colors" 
                        onclick="event.stopPropagation(); playerManager.toggleFavorite('${player.player_id}')">
                    <svg class="w-5 h-5" fill="${isFavorite ? 'currentColor' : 'none'}" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>
                </button>
                
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
    
    createPlayerModalContent(player) {
        const positionClass = this.app.getPositionClass(player.position);
        const isFavorite = this.isFavorite(player.player_id);
        
        // Add to recent players
        this.addToRecent(player.player_id);
        
        return `
            <div class="space-y-6">
                <!-- Player Header -->
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-6">
                        <img src="${player.image_url}" alt="${player.name}" class="w-24 h-24 rounded-lg object-cover">
                        <div>
                            <div class="flex items-center space-x-3 mb-2">
                                <span class="jersey-number text-lg">${player.jersey_number}</span>
                                <span class="position-badge ${positionClass} text-sm">${player.position}</span>
                            </div>
                            <h4 class="text-2xl font-bold text-gray-800">${player.name}</h4>
                            <p class="text-gray-600">${player.nationality} • Age ${player.age}</p>
                        </div>
                    </div>
                    
                    <!-- Action Buttons -->
                    <div class="flex space-x-2">
                        <button class="favorite-btn p-2 rounded-lg ${isFavorite ? 'text-red-500 bg-red-50' : 'text-gray-400 bg-gray-50'} hover:bg-red-50 transition-colors" 
                                onclick="playerManager.toggleFavorite('${player.player_id}')">
                            <svg class="w-6 h-6" fill="${isFavorite ? 'currentColor' : 'none'}" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                            </svg>
                        </button>
                        <button class="p-2 rounded-lg text-gray-400 bg-gray-50 hover:bg-gray-100 transition-colors" 
                                onclick="playerManager.sharePlayer('${player.player_id}')">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z"></path>
                            </svg>
                        </button>
                    </div>
                </div>
                
                <!-- Player Details -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <h5 class="font-semibold text-gray-700 mb-3">Club Information</h5>
                        <div class="space-y-2">
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Years at Club:</span>
                                <span class="text-sm font-medium">${player.years_at_club || 'Unknown'}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Signing Fee:</span>
                                <span class="text-sm font-medium">${player.signing_fee || 'Unknown'}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Weekly Salary:</span>
                                <span class="text-sm font-medium">${player.weekly_salary || 'Unknown'}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <h5 class="font-semibold text-gray-700 mb-3">Personal Details</h5>
                        <div class="space-y-2">
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Birth Date:</span>
                                <span class="text-sm font-medium">${player.birth_date || 'Unknown'}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Nationality:</span>
                                <span class="text-sm font-medium">${player.nationality}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Position:</span>
                                <span class="text-sm font-medium">${player.position}</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Fun Facts -->
                ${player.fun_facts && player.fun_facts.length > 0 ? `
                    <div>
                        <h5 class="font-semibold text-gray-700 mb-3">Fun Facts</h5>
                        <div class="space-y-3">
                            ${player.fun_facts.map(fact => `
                                <div class="fun-fact">
                                    <p class="text-sm text-gray-700">${fact}</p>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}
                
                <!-- Last Updated -->
                <div class="text-xs text-gray-500 text-center pt-4 border-t border-gray-200">
                    Last updated: ${new Date(player.last_updated).toLocaleDateString()}
                </div>
            </div>
        `;
    }
    
    toggleFavorite(playerId) {
        if (this.isFavorite(playerId)) {
            this.removeFromFavorites(playerId);
        } else {
            this.addToFavorites(playerId);
        }
    }
    
    async sharePlayer(playerId) {
        const player = this.app.players.find(p => p.player_id === playerId);
        if (!player) return;
        
        const shareData = {
            title: `${player.name} - Chelsea FC Player`,
            text: `Check out ${player.name} (#${player.jersey_number}) from Chelsea FC!`,
            url: window.location.href
        };
        
        try {
            if (navigator.share) {
                await navigator.share(shareData);
            } else {
                // Fallback to clipboard
                await navigator.clipboard.writeText(`${shareData.text} ${shareData.url}`);
                this.showNotification('Player info copied to clipboard!');
            }
        } catch (error) {
            console.error('Error sharing player:', error);
        }
    }
    
    showNotification(message) {
        // Simple notification - could be enhanced with a toast library
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
    
    getFavoritesCount() {
        return this.favorites.length;
    }
    
    getRecentCount() {
        return this.recentPlayers.length;
    }
}

// Export for use in main app
window.PlayerManager = PlayerManager;

