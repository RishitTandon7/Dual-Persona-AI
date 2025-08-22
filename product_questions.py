import random
from datetime import datetime

class ProductQuestioner:
    def __init__(self):
        self.question_flow = []
        self.user_responses = {}
        self.current_question_index = 0
        self.completed = False
        
    def start_question_flow(self, initial_product_type):
        """Start the question flow based on initial product type"""
        self.user_responses['product_type'] = initial_product_type
        self.generate_question_flow(initial_product_type)
        return self.get_next_question()
    
    def generate_question_flow(self, product_type):
        """Generate appropriate questions based on product type"""
        self.question_flow = []
        
        # Common questions for all product types
        self.question_flow.extend([
            {
                'id': 'budget_range',
                'question': "💰 What's your budget range for this product?",
                'type': 'multiple_choice',
                'options': [
                    {'value': 'under_1000', 'label': 'Under ₹1,000', 'emoji': '💸'},
                    {'value': '1000_5000', 'label': '₹1,000 - ₹5,000', 'emoji': '💰'},
                    {'value': '5000_15000', 'label': '₹5,000 - ₹15,000', 'emoji': '💵'},
                    {'value': '15000_30000', 'label': '₹15,000 - ₹30,000', 'emoji': '💎'},
                    {'value': 'over_30000', 'label': 'Over ₹30,000', 'emoji': '🏦'}
                ]
            },
            {
                'id': 'brand_preference',
                'question': "🏷️ Do you have any brand preferences?",
                'type': 'multiple_choice',
                'options': [
                    {'value': 'any', 'label': 'Any brand is fine', 'emoji': '🌐'},
                    {'value': 'premium', 'label': 'Premium brands only', 'emoji': '👑'},
                    {'value': 'popular', 'label': 'Popular trusted brands', 'emoji': '⭐'},
                    {'value': 'specific', 'label': 'I have specific brands in mind', 'emoji': '🎯'}
                ]
            }
        ])
        
        # Product type specific questions
        if any(keyword in product_type.lower() for keyword in ['electronic', 'laptop', 'phone', 'tablet', 'camera']):
            self.add_electronics_questions()
        elif any(keyword in product_type.lower() for keyword in ['cloth', 'fashion', 'shirt', 'dress', 'shoe']):
            self.add_fashion_questions()
        elif any(keyword in product_type.lower() for keyword in ['book', 'stationery', 'pen', 'paper']):
            self.add_books_questions()
        elif any(keyword in product_type.lower() for keyword in ['home', 'kitchen', 'furniture', 'decor']):
            self.add_home_questions()
            
        # Final preference question
        self.question_flow.append({
            'id': 'primary_concern',
            'question': "🎯 What's your primary concern when buying this product?",
            'type': 'multiple_choice',
            'options': [
                {'value': 'quality', 'label': 'Highest quality', 'emoji': '👑'},
                {'value': 'price', 'label': 'Best price', 'emoji': '💰'},
                {'value': 'reviews', 'label': 'Best reviews', 'emoji': '⭐'},
                {'value': 'features', 'label': 'Specific features', 'emoji': '⚙️'},
                {'value': 'brand', 'label': 'Trusted brand', 'emoji': '🏢'}
            ]
        })
    
    def add_electronics_questions(self):
        """Add electronics-specific questions"""
        self.question_flow.extend([
            {
                'id': 'tech_specs',
                'question': "⚡ What technical specifications are important to you?",
                'type': 'multiple_choice',
                'options': [
                    {'value': 'performance', 'label': 'High performance', 'emoji': '🚀'},
                    {'value': 'battery', 'label': 'Long battery life', 'emoji': '🔋'},
                    {'value': 'storage', 'label': 'Large storage', 'emoji': '💾'},
                    {'value': 'display', 'label': 'Good display quality', 'emoji': '📺'},
                    {'value': 'camera', 'label': 'Good camera', 'emoji': '📷'}
                ]
            },
            {
                'id': 'usage_type',
                'question': "🎮 How will you primarily use this device?",
                'type': 'multiple_choice',
                'options': [
                    {'value': 'gaming', 'label': 'Gaming', 'emoji': '🎮'},
                    {'value': 'work', 'label': 'Work/Professional', 'emoji': '💼'},
                    {'value': 'entertainment', 'label': 'Entertainment', 'emoji': '🎬'},
                    {'value': 'general', 'label': 'General everyday use', 'emoji': '📱'}
                ]
            }
        ])
    
    def add_fashion_questions(self):
        """Add fashion-specific questions"""
        self.question_flow.extend([
            {
                'id': 'clothing_type',
                'question': "👚 What type of clothing are you looking for?",
                'type': 'multiple_choice',
                'options': [
                    {'value': 'casual', 'label': 'Casual wear', 'emoji': '👕'},
                    {'value': 'formal', 'label': 'Formal wear', 'emoji': '👔'},
                    {'value': 'sports', 'label': 'Sports/Activewear', 'emoji': '🏃'},
                    {'value': 'traditional', 'label': 'Traditional wear', 'emoji': '🎎'},
                    {'value': 'accessories', 'label': 'Accessories', 'emoji': '👒'}
                ]
            },
            {
                'id': 'size_preference',
                'question': "📏 Do you know your size preference?",
                'type': 'multiple_choice',
                'options': [
                    {'value': 'know_size', 'label': 'Yes, I know my size', 'emoji': '✅'},
                    {'value': 'need_help', 'label': 'Need size guidance', 'emoji': '❓'},
                    {'value': 'flexible', 'label': 'Flexible on size', 'emoji': '🔄'}
                ]
            }
        ])
    
    def add_books_questions(self):
        """Add books-specific questions"""
        self.question_flow.extend([
            {
                'id': 'book_type',
                'question': "📚 What type of book are you looking for?",
                'type': 'multiple_choice',
                'options': [
                    {'value': 'fiction', 'label': 'Fiction', 'emoji': '📖'},
                    {'value': 'non_fiction', 'label': 'Non-Fiction', 'emoji': '📘'},
                    {'value': 'academic', 'label': 'Academic/Textbook', 'emoji': '🎓'},
                    {'value': 'children', 'label': "Children's book", 'emoji': '👶'},
                    {'value': 'comic', 'label': 'Comic/Graphic novel', 'emoji': '🦸'}
                ]
            },
            {
                'id': 'format_preference',
                'question': "📖 What format do you prefer?",
                'type': 'multiple_choice',
                'options': [
                    {'value': 'paperback', 'label': 'Paperback', 'emoji': '📔'},
                    {'value': 'hardcover', 'label': 'Hardcover', 'emoji': '📕'},
                    {'value': 'ebook', 'label': 'E-book', 'emoji': '📱'},
                    {'value': 'audiobook', 'label': 'Audiobook', 'emoji': '🎧'}
                ]
            }
        ])
    
    def add_home_questions(self):
        """Add home goods-specific questions"""
        self.question_flow.extend([
            {
                'id': 'room_type',
                'question': "🏠 Which room is this for?",
                'type': 'multiple_choice',
                'options': [
                    {'value': 'living', 'label': 'Living Room', 'emoji': '🛋️'},
                    {'value': 'kitchen', 'label': 'Kitchen', 'emoji': '🍳'},
                    {'value': 'bedroom', 'label': 'Bedroom', 'emoji': '🛏️'},
                    {'value': 'bathroom', 'label': 'Bathroom', 'emoji': '🚿'},
                    {'value': 'office', 'label': 'Home Office', 'emoji': '💻'}
                ]
            },
            {
                'id': 'style_preference',
                'question': "🎨 What style do you prefer?",
                'type': 'multiple_choice',
                'options': [
                    {'value': 'modern', 'label': 'Modern', 'emoji': '🏢'},
                    {'value': 'traditional', 'label': 'Traditional', 'emoji': '🏛️'},
                    {'value': 'minimalist', 'label': 'Minimalist', 'emoji': '⚪'},
                    {'value': 'rustic', 'label': 'Rustic', 'emoji': '🌲'},
                    {'value': 'eclectic', 'label': 'Eclectic', 'emoji': '🎭'}
                ]
            }
        ])
    
    def get_next_question(self):
        """Get the next question in the flow"""
        if self.current_question_index >= len(self.question_flow):
            self.completed = True
            return self.generate_summary()
        
        question = self.question_flow[self.current_question_index]
        return {
            'question_id': question['id'],
            'question': question['question'],
            'type': question['type'],
            'options': question.get('options', []),
            'progress': f"{self.current_question_index + 1}/{len(self.question_flow)}",
            'completed': False
        }
    
    def submit_answer(self, question_id, answer):
        """Submit an answer and move to next question"""
        self.user_responses[question_id] = answer
        self.current_question_index += 1
        
        if self.current_question_index >= len(self.question_flow):
            self.completed = True
            return self.generate_summary()
        
        return self.get_next_question()
    
    def generate_summary(self):
        """Generate a summary of user preferences"""
        summary = {
            'completed': True,
            'summary': "Based on your preferences, I'll find the perfect product for you!",
            'preferences': self.user_responses,
            'recommendation_approach': self.get_recommendation_approach()
        }
        return summary
    
    def get_recommendation_approach(self):
        """Determine the best approach based on user preferences"""
        primary_concern = self.user_responses.get('primary_concern', 'quality')
        budget = self.user_responses.get('budget_range', '1000_5000')
        
        approaches = {
            'quality': "I'll focus on finding the highest quality products with excellent reviews",
            'price': "I'll prioritize finding the best value and most affordable options",
            'reviews': "I'll look for products with the best customer ratings and reviews",
            'features': "I'll search for products that match your specific feature requirements",
            'brand': "I'll focus on trusted and reputable brands that you'll love"
        }
        
        return approaches.get(primary_concern, approaches['quality'])
    
    def get_search_recommendations(self):
        """Generate search recommendations based on user responses"""
        product_type = self.user_responses.get('product_type', 'product')
        budget = self.user_responses.get('budget_range', '')
        primary_concern = self.user_responses.get('primary_concern', 'quality')
        
        recommendations = []
        
        # Base search query
        base_query = product_type
        
        # Add budget context
        budget_map = {
            'under_1000': 'affordable',
            '1000_5000': 'mid-range',
            '5000_15000': 'premium',
            '15000_30000': 'high-end',
            'over_30000': 'luxury'
        }
        
        if budget in budget_map:
            recommendations.append(f"Search for {budget_map[budget]} {product_type}")
        
        # Add primary concern context
        concern_map = {
            'quality': 'best quality',
            'price': 'best price',
            'reviews': 'highly rated',
            'features': 'feature-rich',
            'brand': 'branded'
        }
        
        if primary_concern in concern_map:
            recommendations.append(f"Look for {concern_map[primary_concern]} options")
        
        # Add specific recommendations based on product type
        if 'electronic' in product_type.lower():
            recommendations.append("Check warranty and after-sales service")
            recommendations.append("Compare specifications across brands")
        elif 'fashion' in product_type.lower():
            recommendations.append("Check size charts and return policies")
            recommendations.append("Look for customer photos for real look")
        elif 'book' in product_type.lower():
            recommendations.append("Check author reputation and reviews")
            recommendations.append("Compare prices across editions")
        
        return recommendations

# Example usage and testing
if __name__ == "__main__":
    questioner = ProductQuestioner()
    
    print("🤖 AI Product Discovery Assistant")
    print("=" * 40)
    
    # Start with a product type
    product_type = input("What type of product are you looking for? ")
    
    current = questioner.start_question_flow(product_type)
    
    while not questioner.completed:
        print(f"\n{current['progress']} {current['question']}")
        
        if current['type'] == 'multiple_choice':
            for i, option in enumerate(current['options'], 1):
                print(f"  {i}. {option['emoji']} {option['label']}")
            
            try:
                choice = int(input("\nEnter your choice (1-5): ")) - 1
                if 0 <= choice < len(current['options']):
                    selected = current['options'][choice]['value']
                    current = questioner.submit_answer(current['question_id'], selected)
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        else:
            answer = input("\nYour answer: ")
            current = questioner.submit_answer(current['question_id'], answer)
    
    print(f"\n🎉 {current['summary']}")
    print(f"\n📋 Your preferences:")
    for key, value in current['preferences'].items():
        print(f"   {key}: {value}")
    
    print(f"\n🔍 {current['recommendation_approach']}")
    
    recommendations = questioner.get_search_recommendations()
    print(f"\n💡 Search recommendations:")
    for rec in recommendations:
        print(f"   • {rec}")


