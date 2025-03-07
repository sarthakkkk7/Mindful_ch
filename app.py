# app.py
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import cohere
import os
import logging
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mindfulchat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    chats = db.relationship('Chat', backref='user', lazy=True)
    moods = db.relationship('MoodEntry', backref='user', lazy=True)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(255))
    resource_type = db.Column(db.String(50))  # article, hotline, exercise, etc.

# Cohere API Key
cohere_api_key = '9ugWXHUfjx1a10JgzDyBWGaetyYQwjzaMXExeqM8'  # Replace with your Cohere API key
co = cohere.Client(cohere_api_key)

# Chatbot Processor
class ChatbotProcessor:
    def process_message(self, message):
        try:
            # Check for emergency keywords
            if any(word in message.lower() for word in ['suicide', 'kill myself', 'end it all', 'want to die']):
                return "I'm concerned about what you're sharing. If you're having thoughts of harming yourself, please call the National Suicide Prevention Lifeline at 988 immediately. They have trained counselors available 24/7."

            # Use Cohere to generate a response
            response = co.generate(
                model='command',  # Cohere's general-purpose model
                prompt=f"You are a mental health assistant. Provide supportive and empathetic responses to users.\n\nUser: {message}\nAssistant:",
                max_tokens=100,
                temperature=0.7,
                stop_sequences=["\n"]
            )
            return response.generations[0].text.strip()
        except Exception as e:
            # Log the error
            logging.error(f"Cohere API Error: {e}")
            # Provide a fallback response
            return "I'm having trouble connecting to the server. Please try again later."

# Initialize chatbot processor
chatbot = ChatbotProcessor()

# Create database if it doesn't exist
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # Log the user's message
        print(f"User Message: {user_message}")
        
        # Process the message
        bot_response = chatbot.process_message(user_message)
        
        # Log the bot's response
        print(f"Bot Response: {bot_response}")
        
        # Store the chat in the database if user is logged in
        if 'user_id' in session:
            chat_entry = Chat(
                user_id=session['user_id'],
                message=user_message,
                response=bot_response
            )
            db.session.add(chat_entry)
            db.session.commit()
        
        return jsonify({'response': bot_response})
    except Exception as e:
        # Log the error
        logging.error(f"Error in /chat route: {e}")
        return jsonify({'response': "Sorry, I encountered an error. Please try again."})

@app.route('/track-mood', methods=['POST'])
def track_mood():
    try:
        data = request.json
        mood = data.get('mood', '')
        
        responses = {
            '😊': "I'm glad you're feeling good today! What's been going well for you?",
            '😐': "Sounds like you're feeling neutral today. Is there anything on your mind?",
            '😔': "I'm sorry you're feeling down. Would you like to talk about what's troubling you?",
            '😢': "I notice you're feeling sad. Remember it's okay to express your emotions. Is there something specific that's making you feel this way?",
            '😡': "I see you're feeling angry. That's a valid emotion. Would it help to talk about what's frustrating you?"
        }
        
        response = responses.get(mood, "Thank you for sharing how you're feeling.")
        
        # Store the mood in the database if user is logged in
        if 'user_id' in session:
            mood_entry = MoodEntry(
                user_id=session['user_id'],
                mood=mood
            )
            db.session.add(mood_entry)
            db.session.commit()
        
        return jsonify({'response': response})
    except Exception as e:
        logging.error(f"Error in /track-mood route: {e}")
        return jsonify({'response': "Sorry, I encountered an error. Please try again."})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
            # Check if username or email already exists
            if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                return jsonify({'error': 'Username or email already exists'}), 400
            
            # Create new user
            new_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()
            
            # Log the user in
            session['user_id'] = new_user.id
            
            return jsonify({'success': 'Registration successful'})
        except Exception as e:
            logging.error(f"Error in /register route: {e}")
            return jsonify({'error': 'An error occurred during registration'}), 500
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = User.query.filter_by(username=username).first()
            
            if not user or not check_password_hash(user.password_hash, password):
                return jsonify({'error': 'Invalid username or password'}), 401
            
            # Log the user in
            session['user_id'] = user.id
            
            return jsonify({'success': 'Login successful'})
        except Exception as e:
            logging.error(f"Error in /login route: {e}")
            return jsonify({'error': 'An error occurred during login'}), 500
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/resources')
def resources():
    resources = Resource.query.all()
    return render_template('resources.html', resources=resources)

@app.route('/mood-history')
def mood_history():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    moods = MoodEntry.query.filter_by(user_id=session['user_id']).order_by(MoodEntry.timestamp.desc()).all()
    return render_template('mood_history.html', moods=moods)

if __name__ == '__main__':
    app.run(debug=True)
