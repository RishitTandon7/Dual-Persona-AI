class ShoppingAssistant {
    constructor() {
        this.isSearching = false;
        this.currentPlatform = 'all'; // Default to all platforms
        this.init();
    }

    init() {
        this.bindEvents();
        this.scrollToBottom();
        this.setupPlatformFilters();
    }

    bindEvents() {
        const searchBtn = document.getElementById('search-btn');
        const searchInput = document.getElementById('search-input');

        if (searchBtn) {
            searchBtn.addEventListener('click', () => this.handleSearch());
        }
        
        if (searchInput) {
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.handleSearch();
                }
            });
        }
    }

    setupPlatformFilters() {
        const platformButtons = document.querySelectorAll('.platform-btn');
        platformButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active class from all buttons
                platformButtons.forEach(b => b.classList.remove('active'));
                // Add active class to clicked button
                btn.classList.add('active');
                this.currentPlatform = btn.dataset.platform;
                
                // Filter products if we have any displayed
                const productsGrid = document.getElementById('products-grid');
                if (productsGrid && productsGrid.children.length > 0) {
                    this.filterProductsByPlatform();
                }
            });
        });
    }

    async handleSearch() {
        if (this.isSearching) return;

        const searchQuery = document.getElementById('search-input').value.trim();
        
        if (!searchQuery) {
            this.addSystemMessage('Please enter a product to search for!');
            return;
        }

        this.isSearching = true;
        this.showLoading();
        this.hideError();

        // Add user message
        this.addUserMessage(searchQuery);

        try {
            const results = await this.searchProducts(searchQuery);
            
            if (results && results.length > 0) {
                this.displayProducts(results);
                this.displayRecommendations();
                this.showProductsDisplay();
                this.addSystemMessage(`Found ${results.length} products across multiple platforms!`);
            } else {
                this.addSystemMessage('No products found. Try a different search term.');
            }
        } catch (error) {
            this.showError(`Search failed: ${error.message}`);
            this.addSystemMessage('Sorry, I encountered an error while searching. Please try again.');
        } finally {
            this.hideLoading();
            this.isSearching = false;
        }
    }

    async searchProducts(searchQuery) {
        const platforms = this.getSelectedPlatforms();
        
        const response = await fetch('http://localhost:5000/api/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                search_query: searchQuery,
                max_results: 12,
                platforms: platforms,
                preference: 'neutral'
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Server error: ${response.status}`);
        }

        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Search failed');
        }

        // Store the full response data for recommendations
        this.lastSearchData = data;
        
        return data.data;
    }

    getSelectedPlatforms() {
        switch (this.currentPlatform) {
            case 'Amazon': return ['amazon'];
            case 'Flipkart': return ['flipkart'];
            case 'Myntra': return ['myntra'];
            default: return ['amazon', 'flipkart', 'myntra'];
        }
    }

    addUserMessage(query) {
        const messagesContainer = document.getElementById('chat-messages');
        const platforms = this.getSelectedPlatforms();
        const platformText = platforms.length === 3 ? 'all platforms' : platforms.join(', ');

        const messageHTML = `
            <div class="message user-message">
                <div class="message-content">
                    <div class="message-header">
                        <span class="persona-name">You</span>
                        <span class="timestamp">Just now</span>
                    </div>
                    <p><strong>Search:</strong> ${query}</p>
                    <p><strong>Platforms:</strong> ${platformText}</p>
                </div>
            </div>
        `;

        messagesContainer.innerHTML += messageHTML;
        this.scrollToBottom();
    }

    addBotMessage(persona, message) {
        const messagesContainer = document.getElementById('chat-messages');
        const avatarClass = persona.toLowerCase();
        const personaName = persona === 'premiummax' ? 'PremiumMax' : 'BudgetBalance';
        const icon = persona === 'premiummax' ? 'crown' : 'wallet';

        const messageHTML = `
            <div class="message bot-message">
                <div class="avatar ${avatarClass}">
                    <i class="fas fa-${icon}"></i>
                </div>
                <div class="message-content">
                    <div class="message-header">
                        <span class="persona-name">${personaName}</span>
                        <span class="timestamp">Just now</span>
                    </div>
                    <p>${message}</p>
                </div>
            </div>
        `;

        messagesContainer.innerHTML += messageHTML;
        this.scrollToBottom();
    }

    addSystemMessage(message) {
        const messagesContainer = document.getElementById('chat-messages');
        
        const messageHTML = `
            <div class="message bot-message">
                <div class="avatar system">
                    <i class="fas fa-info-circle"></i>
                </div>
                <div class="message-content">
                    <div class="message-header">
                        <span class="persona-name">System</span>
                        <span class="timestamp">Just now</span>
                    </div>
                    <p>${message}</p>
                </div>
            </div>
        `;

        messagesContainer.innerHTML += messageHTML;
        this.scrollToBottom();
    }

    displayProducts(products) {
        const productsGrid = document.getElementById('products-grid');
        if (!productsGrid) return;
        
        productsGrid.innerHTML = '';

        products.forEach(product => {
            const productHTML = `
                <div class="product-card" data-platform="${product.platform.toLowerCase()}">
                    <div class="product-platform">
                        <span class="platform-icon">${product.platform_icon || '📦'}</span>
                        <span>${product.platform}</span>
                    </div>
                    ${product.image ? `<img src="${product.image}" alt="${product.title}" class="product-image" onerror="this.style.display='none'">` : ''}
                    <h4 class="product-title">${this.truncateText(product.title, 60)}</h4>
                    <div class="product-price">₹${product.price}</div>
                    <div class="product-rating">
                        ${this.generateStars(product.rating)}
                        <span>(${product.rating})</span>
                    </div>
                    <a href="${product.url}" target="_blank" class="btn btn-primary">
                        <i class="fas fa-external-link-alt"></i> View Product
                    </a>
                </div>
            `;
            productsGrid.innerHTML += productHTML;
        });

        // Apply current platform filter
        this.filterProductsByPlatform();
    }

    filterProductsByPlatform() {
        const products = document.querySelectorAll('.product-card');
        products.forEach(product => {
            const productPlatform = product.dataset.platform;
            if (this.currentPlatform === 'all' || productPlatform === this.currentPlatform.toLowerCase()) {
                product.style.display = 'block';
            } else {
                product.style.display = 'none';
            }
        });
    }

    showProductsDisplay() {
        const productsDisplay = document.getElementById('products-display');
        if (productsDisplay) {
            productsDisplay.classList.remove('hidden');
        }
    }

    generateStars(rating) {
        const fullStars = Math.floor(rating);
        const halfStar = rating % 1 >= 0.5;
        const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);
        
        let stars = '';
        for (let i = 0; i < fullStars; i++) stars += '⭐';
        if (halfStar) stars += '⭐';
        for (let i = 0; i < emptyStars; i++) stars += '☆';
        
        return stars;
    }

    truncateText(text, maxLength) {
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }

    showLoading() {
        const loadingElement = document.getElementById('loading');
        if (loadingElement) {
            loadingElement.classList.remove('hidden');
        }
    }

    hideLoading() {
        const loadingElement = document.getElementById('loading');
        if (loadingElement) {
            loadingElement.classList.add('hidden');
        }
    }

    showError(message) {
        const errorElement = document.getElementById('error-message');
        const errorText = document.getElementById('error-text');
        
        if (errorElement && errorText) {
            errorText.textContent = message;
            errorElement.classList.remove('hidden');
        }
    }

    hideError() {
        const errorElement = document.getElementById('error-message');
        if (errorElement) {
            errorElement.classList.add('hidden');
        }
    }

    displayRecommendations() {
        if (!this.lastSearchData) return;
        
        const personaDebateSection = document.getElementById('persona-debate');
        const finalRecommendationSection = document.getElementById('final-recommendation');
        
        if (!personaDebateSection || !finalRecommendationSection) return;
        
        // Clear previous recommendations
        personaDebateSection.innerHTML = '';
        finalRecommendationSection.innerHTML = '';
        
        const { premium_recommendations, budget_recommendations, final_recommendation } = this.lastSearchData;
        
        // Display persona debate
        if (premium_recommendations && premium_recommendations.length > 0) {
            let debateHTML = `
                <div class="persona-section">
                    <h3>🤖 PremiumMax (High-End Expert) Recommendations</h3>
                    <div class="recommendation-grid">
            `;
            
            premium_recommendations.forEach((product, index) => {
                debateHTML += `
                    <div class="recommendation-card">
                        <div class="platform-badge">${product.platform_icon} ${product.platform}</div>
                        ${product.image ? `<img src="${product.image}" alt="${product.title}" class="recommendation-image" onerror="this.style.display='none'">` : ''}
                        <h4>${this.truncateText(product.title, 50)}</h4>
                        <div class="price-rating">
                            <span class="price">₹${product.price}</span>
                            <span class="rating">⭐${product.rating}</span>
                        </div>
                        <a href="${product.url}" target="_blank" class="btn btn-small">
                            <i class="fas fa-external-link-alt"></i> View
                        </a>
                    </div>
                `;
            });
            
            debateHTML += `</div></div>`;
            personaDebateSection.innerHTML += debateHTML;
        }
        
        if (budget_recommendations && budget_recommendations.length > 0) {
            let debateHTML = `
                <div class="persona-section">
                    <h3>🤖 BudgetBalance (Smart Saver) Recommendations</h3>
                    <div class="recommendation-grid">
            `;
            
            budget_recommendations.forEach((product, index) => {
                debateHTML += `
                    <div class="recommendation-card">
                        <div class="platform-badge">${product.platform_icon} ${product.platform}</div>
                        ${product.image ? `<img src="${product.image}" alt="${product.title}" class="recommendation-image" onerror="this.style.display='none'">` : ''}
                        <h4>${this.truncateText(product.title, 50)}</h4>
                        <div class="price-rating">
                            <span class="price">₹${product.price}</span>
                            <span class="rating">⭐${product.rating}</span>
                        </div>
                        <a href="${product.url}" target="_blank" class="btn btn-small">
                            <i class="fas fa-external-link-alt"></i> View
                        </a>
                    </div>
                `;
            });
            
            debateHTML += `</div></div>`;
            personaDebateSection.innerHTML += debateHTML;
        }
        
        // Display final recommendation
        if (final_recommendation) {
            const finalHTML = `
                <div class="final-recommendation-card">
                    <h3>🎯 FINAL RECOMMENDATION</h3>
                    <div class="final-product">
                        <div class="platform-badge large">${final_recommendation.platform_icon} ${final_recommendation.platform}</div>
                        ${final_recommendation.image ? `<img src="${final_recommendation.image}" alt="${final_recommendation.title}" class="final-product-image" onerror="this.style.display='none'">` : ''}
                        <h2>${final_recommendation.title}</h2>
                        <div class="final-details">
                            <div class="price">₹${final_recommendation.price}</div>
                            <div class="rating">⭐${final_recommendation.rating}</div>
                        </div>
                        <p class="recommendation-text">Best value for money based on your search criteria!</p>
                        <a href="${final_recommendation.url}" target="_blank" class="btn btn-primary btn-large">
                            <i class="fas fa-shopping-cart"></i> Buy Now on ${final_recommendation.platform}
                        </a>
                    </div>
                </div>
            `;
            finalRecommendationSection.innerHTML = finalHTML;
        }
        
        // Show the sections
        personaDebateSection.classList.remove('hidden');
        finalRecommendationSection.classList.remove('hidden');
    }

    scrollToBottom() {
        const messagesContainer = document.getElementById('chat-messages');
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ShoppingAssistant();
});


