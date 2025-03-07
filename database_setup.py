# database_setup.py
from app import app, db, User, Chat, MoodEntry, Resource
from werkzeug.security import generate_password_hash
import datetime

# Use this script to initialize the database with sample data
with app.app_context():
    # Create all tables
    db.create_all()
    
    # Check if we already have data
    if User.query.count() == 0:
        print("Creating sample data...")
        
        # Create sample users
        admin = User(
            username="admin",
            email="admin@mindfulchat.com",
            password_hash=generate_password_hash("adminpassword")
        )
        
        test_user = User(
            username="testuser",
            email="test@example.com",
            password_hash=generate_password_hash("testpassword")
        )
        
        db.session.add_all([admin, test_user])
        db.session.commit()
        
        # Create sample chat history
        chats = [
            Chat(
                user_id=test_user.id,
                message="I'm feeling really stressed about work lately.",
                response="I'm sorry to hear you're feeling stressed. Work pressure can be challenging. Have you tried any relaxation techniques?",
                timestamp=datetime.datetime.utcnow() - datetime.timedelta(days=3, hours=4)
            ),
            # Add more sample chats here
        ]
        
        db.session.add_all(chats)
        
        # Create sample mood entries
        moods = [
            MoodEntry(
                user_id=test_user.id,
                mood="😔",
                notes="Feeling down due to work pressure",
                timestamp=datetime.datetime.utcnow() - datetime.timedelta(days=5)
            ),
            # Add more sample moods here
        ]
        
        db.session.add_all(moods)
        
        # Create mental health resources
        resources = [
            Resource(
                title="National Suicide Prevention Lifeline",
                description="24/7, free and confidential support for people in distress",
                url="https://suicidepreventionlifeline.org",
                resource_type="hotline"
            ),
            # Add more resources here
        ]
        
        db.session.add_all(resources)
        db.session.commit()
        
        print("Sample data created successfully!")
    else:
        print("Database already contains data. No changes made.")