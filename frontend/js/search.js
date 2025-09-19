/**
 * Blue's Book - Search Functionality
 * Handles advanced search features and autocomplete
 */

class SearchManager {
    constructor(app) {
        this.app = app;
        this.searchCache = new Map();
        this.searchTimeout = null;
        this.minSearchLength = 2;
        this.maxSuggestions = 10;
    }
    
    async performSearch(query, options = {}) {
        const {
            category = 'all',
            limit = 20,
            useCache = true
        } = options;
        
        // Check cache first
        const cacheKey = `${query}-${category}-${limit}`;
        if (useCache && this.searchCache.has(cacheKey)) {
            const cached = this.searchCache.get(cacheKey);
            // Return cached result if it's less than 5 minutes old
            if (Date.now() - cached.timestamp < 300000) {
                return cached.data;
            }
        }
        
        try {
            const response = await fetch(`${this.app.apiBaseUrl}/search?q=${encodeURIComponent(query)}&category=${category}&limit=${limit}`);
            const data = await response.json();
            
            if (data.success) {
                // Cache the result
                this.searchCache.set(cacheKey, {
                    data: data.data,
                    timestamp: Date.now()
                });
                
                return data.data;
            }
            
            return [];
        } catch (error) {
            console.error('Search error:', error);
            return [];
        }
    }
    
    async getSearchSuggestions(query) {
        if (query.length < this.minSearchLength) {
            return [];
        }
        
        try {
            const response = await fetch(`${this.app.apiBaseUrl}/search/suggestions?q=${encodeURIComponent(query)}&limit=${this.maxSuggestions}`);
            const data = await response.json();
            
            if (data.success) {
                return data.data;
            }
            
            return [];
        } catch (error) {
            console.error('Suggestions error:', error);
            return [];
        }
    }
    
    debounceSearch(callback, delay = 300) {
        return (...args) => {
            clearTimeout(this.searchTimeout);
            this.searchTimeout = setTimeout(() => callback.apply(this, args), delay);
        };
    }
    
    highlightSearchTerm(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark class="bg-yellow-200 px-1 rounded">$1</mark>');
    }
    
    createSearchResult(result) {
        const { type, data } = result;
        
        if (type === 'player') {
            return this.createPlayerSearchResult(data);
        } else if (type === 'manager') {
            return this.createManagerSearchResult(data);
        }
        
        return null;
    }
    
    createPlayerSearchResult(player) {
        const positionClass = this.app.getPositionClass(player.position);
        
        return `
            <div class="search-result-item p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer" 
                 onclick="app.showPlayerModal('${player.id}')">
                <div class="flex items-center space-x-4">
                    <img src="${player.image_url}" alt="${player.name}" class="w-12 h-12 rounded-full object-cover">
                    <div class="flex-1">
                        <h4 class="font-semibold text-gray-800">${player.name}</h4>
                        <div class="flex items-center space-x-2 mt-1">
                            <span class="jersey-number text-xs">${player.jersey_number}</span>
                            <span class="position-badge ${positionClass} text-xs">${player.position}</span>
                            <span class="text-sm text-gray-500">${player.nationality}</span>
                        </div>
                    </div>
                    <div class="text-gray-400">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                        </svg>
                    </div>
                </div>
            </div>
        `;
    }
    
    createManagerSearchResult(manager) {
        return `
            <div class="search-result-item p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                <div class="flex items-center space-x-4">
                    <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                        <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                        </svg>
                    </div>
                    <div class="flex-1">
                        <h4 class="font-semibold text-gray-800">${manager.name}</h4>
                        <p class="text-sm text-gray-500 mt-1">Manager • ${manager.nationality}</p>
                    </div>
                    <div class="text-gray-400">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                        </svg>
                    </div>
                </div>
            </div>
        `;
    }
    
    createSuggestionItem(suggestion) {
        const { text, type, position, jersey_number } = suggestion;
        
        return `
            <div class="search-suggestion flex items-center space-x-3" 
                 onclick="app.selectSuggestion('${text}')">
                <div class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                    ${type === 'player' ? 
                        `<span class="text-xs font-bold text-gray-600">#${jersey_number}</span>` :
                        `<svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                        </svg>`
                    }
                </div>
                <div class="flex-1">
                    <div class="font-medium text-gray-800">${text}</div>
                    <div class="text-sm text-gray-500">
                        ${type === 'player' ? `${position} • #${jersey_number}` : 'Manager'}
                    </div>
                </div>
            </div>
        `;
    }
    
    clearCache() {
        this.searchCache.clear();
    }
    
    getCacheStats() {
        return {
            size: this.searchCache.size,
            keys: Array.from(this.searchCache.keys())
        };
    }
}

// Export for use in main app
window.SearchManager = SearchManager;

