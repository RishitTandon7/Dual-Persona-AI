# 🤖 Enhanced AI Shopping Assistant

A comprehensive multi-platform shopping assistant with intelligent product discovery, advanced scraping capabilities, and modern UI/UX design.

## ✨ Features

### 🛍️ Multi-Platform Support
- **Amazon India** - Comprehensive product scraping
- **Flipkart** - Indian e-commerce giant support  
- **Myntra** - Fashion and lifestyle products
- **Unified Product Data** - Consistent structure across all platforms

### 🧠 Intelligent Product Discovery
- **Smart Question Flow** - Context-aware questioning system
- **Budget Range Filtering** - ₹1,000 to ₹30,000+ ranges
- **Brand Preferences** - Premium, popular, or specific brands
- **Product-Specific Questions** - Electronics, fashion, books, home goods
- **Personalized Recommendations** - Based on user preferences

### ⚡ Backend Enhancements
- **Multi-threaded Scraping** - Faster product retrieval
- **Intelligent Caching** - 5-minute cache for repeated searches
- **Enhanced Error Handling** - Graceful fallbacks and mock data
- **Platform Comparison** - Side-by-side product analysis

### 🎨 Modern UI/UX
- **Glassmorphism Design** - Beautiful translucent effects
- **Smooth Animations** - CSS transitions and keyframe animations
- **Responsive Design** - Mobile-first approach
- **Typing Indicators** - Real-time chatbot feedback
- **Product Galleries** - Enhanced image displays

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd ai-shopping-assistant

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

### Usage
1. Open your browser and navigate to `http://localhost:5000`
2. Start chatting with the AI shopping assistant
3. Answer questions about your preferences
4. Browse recommended products across multiple platforms

## 📡 API Endpoints

### Core Endpoints
- `GET /api/health` - Health check and feature status
- `POST /api/scrape` - Multi-platform product search
- `GET /api/platforms` - Available shopping platforms
- `POST /api/clear-cache` - Clear search cache
- `POST /api/persona-debate` - AI-powered product recommendations

### Question Flow Endpoints
- `POST /api/questions/start` - Start new question session
- `POST /api/questions/answer` - Submit answer to current question
- `GET /api/questions/session/<session_id>` - Get session status

## 🎯 Question Flow Types

### Budget Questions
- Under ₹1,000 💸
- ₹1,000 - ₹5,000 💰  
- ₹5,000 - ₹15,000 💵
- ₹15,000 - ₹30,000 💎
- Over ₹30,000 🏦

### Brand Preferences
- Any brand 🌐
- Premium brands only 👑
- Popular trusted brands ⭐
- Specific brands 🎯

### Product Categories
- **Electronics** - Performance, battery, storage, display, camera
- **Fashion** - Casual, formal, sports, traditional, accessories
- **Books** - Fiction, non-fiction, academic, children's, comics
- **Home Goods** - Living room, kitchen, bedroom, bathroom, office

## 🛠️ Technical Architecture

### Backend Stack
- **Flask** - Web framework with RESTful APIs
- **Flask-CORS** - Cross-origin resource sharing
- **Web Scraping** - Multi-platform product data extraction
- **Caching** - Intelligent search result caching
- **Multi-threading** - Concurrent platform scraping

### Frontend Features
- **Modern CSS** - Glassmorphism design with gradients
- **JavaScript** - Dynamic chat interface
- **Responsive Grid** - Adaptive product displays
- **Real-time Updates** - WebSocket-like functionality

## 🔧 Configuration

### Environment Variables
```bash
# Server configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# Scraping settings
CACHE_TIMEOUT=300  # 5 minutes
MAX_RESULTS=12     # Default products per search
```

### Platform Settings
Platforms can be enabled/disabled in the web interface:
- Amazon 📦 - Electronics, general merchandise
- Flipkart 🛒 - Wide range of products
- Myntra 👕 - Fashion and lifestyle

## 📊 Performance Features

### Caching Strategy
- **5-minute cache** for identical search queries
- **Platform statistics** for search optimization
- **Automatic cache clearing** on demand

### Error Handling
- **Graceful fallbacks** to mock data when scraping fails
- **Input validation** for all API endpoints
- **Comprehensive logging** for debugging

## 🎨 UI Components

### Chat Interface
- **Message bubbles** with user/bot differentiation
- **Typing indicators** with animated dots
- **Smooth scrolling** for message history
- **Real-time updates** without page refresh

### Product Display
- **Grid layout** with responsive cards
- **Hover effects** with scale and shadow animations
- **Platform badges** with platform-specific icons
- **Action buttons** for product interaction

### Question Flow
- **Multiple choice** options with emojis
- **Progress indicators** showing completion status
- **Visual feedback** for selected options
- **Smooth transitions** between questions

## 🔮 Future Enhancements

### Planned Features
- **Price Comparison** - Cross-platform price analysis
- **Wishlist Functionality** - Save products for later
- **Search History** - Track previous searches
- **Product Recommendations** - AI-powered suggestions
- **Real Product Links** - Direct links to product pages

### Technical Improvements
- **Database Integration** - Persistent user data
- **Authentication** - User accounts and preferences
- **Advanced Scraping** - More platforms and categories
- **Machine Learning** - Personalized recommendations

## 🤝 Contributing

We welcome contributions! Please feel free to:
1. Fork the repository
2. Create feature branches
3. Submit pull requests
4. Report issues and suggestions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Flask and modern web technologies
- Inspired by intelligent shopping assistants
- Designed for the Indian e-commerce market
- Focused on user experience and performance

---

**Happy Shopping!** 🛍️✨
