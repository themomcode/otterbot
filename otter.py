from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import datetime
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# This would be your main chatbot logic
class OtterBot:
    def __init__(self):
        self.name = "Otterbot"
        # Initialize your datasets or LLM connections here
        
    def process_message(self, user_message):
        """
        Main function to process user messages and generate responses.
        This is where you'll integrate your LLM API calls and dataset queries.
        """
        # Convert message to lowercase for easier processing
        message_lower = user_message.lower()
        
        # Simple response logic (replace this with your LLM integration)
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey']):
            return "Hello there! I'm Otterbot. How can I assist you today?"
        elif any(word in message_lower for word in ['dataset', 'data']):
            return "I can help you query datasets! What specific information are you looking for?"
        elif any(word in message_lower for word in ['help', 'what can you do']):
            return "I'm an AI chatbot that can reference specific datasets and answer questions. Try asking me about data or say hello!"
        else:
            # This is where you'd call your LLM API
            return f"You said: '{user_message}'. I'm still learning how to respond to that!"
    
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
