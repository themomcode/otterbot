from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import datetime
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# This would be your main chatbot logic
class OtterBot:
    def __init__(self):
        self.name = "Otterbot"
        
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("Warning: GEMINI_API_KEY not found in environment variables")
            self.model = None
        else:
            genai.configure(api_key=api_key)
            # Use gemini-pro for text generation
            self.model = genai.GenerativeModel('gemini-pro')
            print("Gemini API initialized successfully")
        
        # Legal-focused system prompt
        self.legal_system_prompt = """
        You are Otterbot, an AI assistant specialized in legal language and communication. 
        Your primary functions are:
        1. Help users understand legal terminology and concepts
        2. Analyze legal language patterns and structures
        3. Assist with legal document comprehension
        4. Provide educational information about legal communication
        
        Always maintain a professional tone and clarify that you provide educational information only, 
        not legal advice. If asked about specific legal cases or advice, remind users to consult 
        with qualified legal professionals.
        """
        
    def process_message(self, user_message):
        """
        Main function to process user messages using Gemini API
        """
        try:
            # If Gemini is not configured, fall back to simple responses
            if not self.model:
                return self._fallback_response(user_message)
            
            # Create a legal-focused prompt
            full_prompt = f"""
            {self.legal_system_prompt}
            
            User message: {user_message}
            
            Please respond helpfully while focusing on legal language learning and communication.
            """
            
            # Generate response using Gemini
            response = self.model.generate_content(full_prompt)
            
            if response and response.text:
                return response.text
            else:
                return "I'm having trouble generating a response right now. Please try again."
                
        except Exception as e:
            print(f"Error with Gemini API: {str(e)}")
            return self._fallback_response(user_message)
    
    def _fallback_response(self, user_message):
        """
        Fallback responses when Gemini API is not available
        """
        message_lower = user_message.lower()
        
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey']):
            return "Hello! I'm Otterbot, your legal language learning assistant. How can I help you understand legal terminology or communication today?"
        elif any(word in message_lower for word in ['legal', 'law', 'contract', 'terms']):
            return "I'd love to help with legal language! However, I need my AI capabilities to provide detailed assistance. Please make sure the GEMINI_API_KEY is configured."
        elif any(word in message_lower for word in ['dataset', 'data']):
            return "I can help you query legal datasets and analyze legal language patterns. What specific information are you looking for?"
        else:
            return f"I received your message: '{user_message}'. To provide better legal language assistance, please configure the Gemini API key."
    
    def query_dataset(self, query_params):
        """
        Function to query your specific datasets.
        Replace this with your actual dataset querying logic.
        """
        # Placeholder for dataset querying
        return {"status": "success", "data": "Sample dataset response"}

# Initialize the bot
bot = OtterBot()

@app.route('/')
def index():
    """Serve the main HTML page"""
    # You can serve your HTML file directly or return it as a string
    # For now, returning a simple message - replace with your HTML content
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Otterbot</title>
    </head>
    <body>
        <h1>Otterbot Backend is Running!</h1>
        <p>The chatbot backend is working. Make sure to serve your HTML file separately or update this route.</p>
    </body>
    </html>
    '''

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend"""
    try:
        # Get JSON data from request
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message']
        timestamp = data.get('timestamp', datetime.datetime.now().isoformat())
        
        # Log the conversation (optional)
        print(f"[{timestamp}] User: {user_message}")
        
        # Process the message with your bot
        bot_response = bot.process_message(user_message)
        
        # Log the response (optional)
        print(f"[{datetime.datetime.now().isoformat()}] Bot: {bot_response}")
        
        # Return the response
        return jsonify({
            'response': bot_response,
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        print(f"Error processing chat: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Sorry, something went wrong processing your message.'
        }), 500

@app.route('/dataset', methods=['POST'])
def query_dataset():
    """Handle dataset queries"""
    try:
        data = request.json
        result = bot.query_dataset(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'bot_name': bot.name
    })

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    print(f"Starting Otterbot on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
