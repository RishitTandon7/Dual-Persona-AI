from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import sys
import os
from datetime import datetime
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Add current directory to Python path to import webscraper
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the enhanced webscraper functions
try:
    from webscraper_fixed import scrape_all_platforms, premiummax, budgetbalance, persona_debate
    from product_questions import ProductQuestioner
    WEBSCRAPER_AVAILABLE = True
    QUESTIONER_AVAILABLE = True
    print("✅ Successfully imported enhanced webscraper functions")
    print("✅ Successfully imported product questioner")
except ImportError as e:
    WEBSCRAPER_AVAILABLE = False
    QUESTIONER_AVAILABLE = False
    print(f"⚠️ Warning: Could not import webscraper functions: {e}")
    print("Using mock data for demonstration")

# Simple cache implementation
search_cache = {}
CACHE_TIMEOUT = 300  # 5 minutes

# Product questioner instances
questioner_sessions = {}

@app.route('/')
def serve_frontend():
    """Serve the main frontend page"""
    return send_from_directory('.', 'enhanced-index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', path)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'backend_available': WEBSCRAPER_AVAILABLE,
        'timestamp': datetime.now().isoformat(),
        'message': 'Enhanced AI Shopping Assistant Backend is running',
        'features': ['multi-platform', 'caching', 'enhanced-scraping']
    })

@app.route('/api/scrape', methods=['POST'])
def scrape_products():
    """API endpoint for multi-platform product scraping"""
    try:
        data = request.get_json()
        
        if not data or 'search_query' not in data:
            return jsonify({'error': 'Search query is required'}), 400
        
        search_query = data['search_query'].strip()
        max_results = data.get('max_results', 12)
        preference = data.get('preference', 'neutral')
        platforms = data.get('platforms', ['amazon', 'flipkart', 'myntra'])
        
        if not search_query:
            return jsonify({'error': 'Search query cannot be empty'}), 400
        
        # Check cache first
        cache_key = f"{search_query}_{preference}_{max_results}"
        if cache_key in search_cache and time.time() - search_cache[cache_key]['timestamp'] < CACHE_TIMEOUT:
            cached_data = search_cache[cache_key]['data']
            print(f"📦 Serving from cache: {search_query}")
            return jsonify(cached_data)
        
        if WEBSCRAPER_AVAILABLE:
            try:
                # Use the enhanced multi-platform scraper
                results = scrape_all_platforms(search_query, max_results)
                
                if not results:
                    response_data = {
                        'success': True,
                        'data': [],
                        'message': 'No products found for your search across all platforms',
                        'timestamp': datetime.now().isoformat(),
                        'platforms_searched': platforms
                    }
                    search_cache[cache_key] = {
                        'data': response_data,
                        'timestamp': time.time()
                    }
                    return jsonify(response_data)
                
                # Get persona recommendations
                pm_recs = premiummax(results, 4)
                bb_recs = budgetbalance(results, 4)
                
                # Get final recommendation based on preference
                final_rec = persona_debate(results, preference)
                
                # Prepare platform statistics
                platform_stats = {}
                for product in results:
                    platform = product['platform']
                    platform_stats[platform] = platform_stats.get(platform, 0) + 1
                
                response_data = {
                    'success': True,
                    'data': results,
                    'premium_recommendations': pm_recs,
                    'budget_recommendations': bb_recs,
                    'final_recommendation': final_rec,
                    'preference': preference,
                    'timestamp': datetime.now().isoformat(),
                    'platform_stats': platform_stats,
                    'total_results': len(results),
                    'source': 'Multi-Platform (Amazon, Flipkart, Myntra)'
                }
                
                # Cache the results
                search_cache[cache_key] = {
                    'data': response_data,
                    'timestamp': time.time()
                }
                
                return jsonify(response_data)
                
            except Exception as e:
                return jsonify({
                    'error': f'Scraping failed: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                }), 500
        else:
            # Fallback to enhanced mock data
            mock_data = generate_enhanced_mock_data(search_query, max_results, platforms)
            return jsonify({
                'success': True,
                'data': mock_data,
                'premium_recommendations': mock_data[:4],
                'budget_recommendations': mock_data[-4:],
                'final_recommendation': mock_data[0],
                'preference': preference,
                'timestamp': datetime.now().isoformat(),
                'source': 'mock_data',
                'note': 'webscraper.py not available - using enhanced mock data'
            })
            
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

def generate_enhanced_mock_data(search_query, max_results, platforms):
    """Generate enhanced mock product data with multiple platforms"""
    products = []
    platforms_info = {
        'amazon': {'icon': '📦', 'base_price': 1000},
        'flipkart': {'icon': '🛒', 'base_price': 800},
        'myntra': {'icon': '👕', 'base_price': 1200}
    }
    
    for i in range(max_results):
        platform = list(platforms_info.keys())[i % len(platforms_info)]
        platform_data = platforms_info[platform]
        
        price = platform_data['base_price'] + (i * 300)
        rating = max(3.0, min(5.0, 4.0 + (i * 0.1)))
        
        product = {
            'title': f'{search_query.capitalize()} {platform.capitalize()} Edition {i+1}',
            'price': price,
            'rating': round(rating, 1),
            'url': f'https://www.{platform}.com/search?q={search_query.replace(" ", "+")}',
            'image': f'https://picsum.photos/300/400?random={i+100}',
            'platform': platform.capitalize(),
            'platform_icon': platform_data['icon']
        }
        products.append(product)
    
    return products

@app.route('/api/platforms', methods=['GET'])
def get_platforms():
    """Get available shopping platforms"""
    platforms = [
        {'name': 'Amazon', 'icon': '📦', 'enabled': True},
        {'name': 'Flipkart', 'icon': '🛒', 'enabled': True},
        {'name': 'Myntra', 'icon': '👕', 'enabled': True}
    ]
    return jsonify({'platforms': platforms})

@app.route('/api/clear-cache', methods=['POST'])
def clear_cache():
    """Clear the search cache"""
    search_cache.clear()
    return jsonify({'success': True, 'message': 'Cache cleared', 'cache_size': 0})

@app.route('/api/questions/start', methods=['POST'])
def start_question_flow():
    """Start a new question flow session"""
    try:
        data = request.get_json()
        
        if not data or 'product_type' not in data:
            return jsonify({'error': 'Product type is required'}), 400
        
        product_type = data['product_type'].strip()
        session_id = str(int(time.time() * 1000))  # Unique session ID
        
        if QUESTIONER_AVAILABLE:
            questioner = ProductQuestioner()
            first_question = questioner.start_question_flow(product_type)
            
            # Store the questioner instance
            questioner_sessions[session_id] = {
                'questioner': questioner,
                'created_at': time.time()
            }
            
            return jsonify({
                'success': True,
                'session_id': session_id,
                'question': first_question,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Questioner not available',
                'timestamp': datetime.now().isoformat()
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': f'Failed to start question flow: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/questions/answer', methods=['POST'])
def submit_answer():
    """Submit an answer to the current question"""
    try:
        data = request.get_json()
        
        if not data or 'session_id' not in data or 'answer' not in data:
            return jsonify({'error': 'Session ID and answer are required'}), 400
        
        session_id = data['session_id']
        answer = data['answer']
        
        if session_id not in questioner_sessions:
            return jsonify({'error': 'Invalid session ID'}), 404
        
        questioner_data = questioner_sessions[session_id]
        questioner = questioner_data['questioner']
        
        # Get current question to know the question_id
        current_question = questioner.get_next_question()
        if current_question['completed']:
            return jsonify({
                'success': True,
                'completed': True,
                'result': current_question,
                'timestamp': datetime.now().isoformat()
            })
        
        next_step = questioner.submit_answer(current_question['question_id'], answer)
        
        return jsonify({
            'success': True,
            'next_question': next_step,
            'completed': next_step.get('completed', False),
            'timestamp': datetime.now().isoformat()
        })
            
    except Exception as e:
        return jsonify({
            'error': f'Failed to submit answer: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/questions/session/<session_id>', methods=['GET'])
def get_session_status(session_id):
    """Get the current status of a question session"""
    if session_id not in questioner_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    questioner_data = questioner_sessions[session_id]
    questioner = questioner_data['questioner']
    
    current_question = questioner.get_next_question()
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'current_question': current_question,
        'completed': questioner.completed,
        'progress': f"{questioner.current_question_index}/{len(questioner.question_flow)}",
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/persona-debate', methods=['POST'])
def persona_debate_endpoint():
    """API endpoint for persona debate simulation"""
    try:
        data = request.get_json()
        
        if not data or 'products' not in data:
            return jsonify({'error': 'Products data is required'}), 400
        
        products = data['products']
        preference = data.get('preference', 'neutral')
        
        if WEBSCRAPER_AVAILABLE:
            try:
                # Use the actual persona debate function
                final_choice = persona_debate(products, preference)
                
                return jsonify({
                    'success': True,
                    'final_choice': final_choice,
                    'preference': preference,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({
                    'error': f'Persona debate failed: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                }), 500
        else:
            # Enhanced mock persona debate
            filtered = [p for p in products if p.get('price', 0) > 0 and p.get('rating', 0) > 0]
            if not filtered:
                filtered = products
                
            if preference == 'premium':
                final_choice = sorted(filtered, key=lambda x: x.get('rating', 0), reverse=True)[0]
            elif preference == 'budget':
                final_choice = sorted(filtered, key=lambda x: x.get('price', 0))[0]
            else:
                final_choice = sorted(filtered, key=lambda x: (x.get('rating', 0) / (x.get('price', 0) + 1)), reverse=True)[0]
            
            return jsonify({
                'success': True,
                'final_choice': final_choice,
                'preference': preference,
                'timestamp': datetime.now().isoformat(),
                'note': 'Enhanced mock persona debate results'
            })
            
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🤖 Starting Enhanced AI Shopping Assistant Server...")
    print(f"📦 Webscraper available: {WEBSCRAPER_AVAILABLE}")
    if not WEBSCRAPER_AVAILABLE:
        print("💡 Note: webscraper.py functions not available. Using enhanced mock data.")
    print("🌐 Multi-Platform Support: Amazon, Flipkart, Myntra")
    print("⚡ Features: Caching, Enhanced scraping, Platform comparison")
    print("🌐 Server running on http://localhost:5000")
    print("🔍 API endpoints:")
    print("   - GET  /api/health")
    print("   - POST /api/scrape")
    print("   - GET  /api/platforms")
    print("   - POST /api/clear-cache")
    print("   - POST /api/persona-debate")
    app.run(debug=True, host='0.0.0.0', port=5000)



