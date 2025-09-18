from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import scraper
try:
    from webscraper import scrape_amazon_in, premiummax, budgetbalance, persona_debate
    WEBSCRAPER_AVAILABLE = True
    print("✅ Successfully imported webscraper functions")
except ImportError as e:
    WEBSCRAPER_AVAILABLE = False
    print(f"⚠️ Warning: Could not import webscraper functions: {e}")

@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'backend_available': WEBSCRAPER_AVAILABLE,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/scrape', methods=['POST'])
def scrape_amazon():
    try:
        data = request.get_json()
        if not data or 'search_query' not in data:
            return jsonify({'error': 'Search query is required'}), 400

        search_query = data['search_query']
        max_results = data.get('max_results', 10)
        preference = data.get('preference', 'neutral')

        if not search_query.strip():
            return jsonify({'error': 'Search query cannot be empty'}), 400

        if WEBSCRAPER_AVAILABLE:
            results = scrape_amazon_in(search_query, max_results)

            if not results:
                return jsonify({
                    'success': True,
                    'data': [],
                    'message': 'No products found',
                    'timestamp': datetime.now().isoformat()
                })

            pm_recs = premiummax(results, 3)
            bb_recs = budgetbalance(results, 3)
            final_rec = persona_debate(results, preference)

            return jsonify({
                'success': True,
                'data': results,
                'premium_recommendations': pm_recs,
                'budget_recommendations': bb_recs,
                'final_recommendation': final_rec,
                'preference': preference,
                'timestamp': datetime.now().isoformat(),
                'source': 'Amazon India'
            })

        else:
            return jsonify({
                'error': 'Webscraper not available'
            }), 500

    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/persona-debate', methods=['POST'])
def persona_debate_endpoint():
    try:
        data = request.get_json()
        if not data or 'products' not in data:
            return jsonify({'error': 'Products data is required'}), 400

        products = data['products']
        preference = data.get('preference', 'neutral')
        final_choice = persona_debate(products, preference)

        return jsonify({
            'success': True,
            'final_choice': final_choice,
            'preference': preference,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🤖 Starting AI Shopping Assistant Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
    print(f"📦 Webscraper available: {WEBSCRAPER_AVAILABLE}")


