# Mindful_ch
Mental Health Chatbot powered by AI

Step 1: Set Up Your Development Environment
Install Python:

Download and install Python from python.org.

During installation, make sure to check the box that says "Add Python to PATH".

Install a Code Editor:

Download and install Visual Studio Code (VS Code), a beginner-friendly code editor.

Install Git:

Download and install Git from git-scm.com. This will help you manage your code and deploy it later.

Open a Terminal:

On Windows, open Command Prompt or PowerShell.

On macOS/Linux, open Terminal.
. Create a Project Folder:

Open your terminal and run:

bash
Copy
mkdir mindfulchat
cd mindfulchat

Step 2: Set Up a Virtual Environment
A virtual environment helps you manage dependencies for your project.
Create a Virtual Environment:

Run the following command in your terminal:

bash
Copy
python -m venv venv
This creates a folder called venv in your project.

Activate the Virtual Environment:

On Windows:

bash
Copy
venv\Scripts\activate
On macOS/Linux:

bash
Copy
source venv/bin/activate
You’ll see (venv) in your terminal, indicating the virtual environment is active.

Step 3: Install Required Libraries
Install Flask and Other Dependencies:

Run the following commands in your terminal:

bash
Copy
pip install flask flask-sqlalchemy nltk openai
This installs:

Flask: A web framework for Python.

Flask-SQLAlchemy: For database management.

NLTK: For natural language processing.

OpenAI: For integrating the AI chatbot.

Download NLTK Data:

Run the following commands in your terminal:
bash
Copy
python
Then, in the Python shell:

python
Copy
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
exit()
Step 4: Create the Flask Application
Create app.py:

In your project folder (mindfulchat), create a file named app.py.

Copy and paste the updated app.py code from the previous response into this file.

Set Up the Database:

In your terminal, run:
bash
Copy
python
Then, in the Python shell:

python
Copy
from app import db, app
with app.app_context():
    db.create_all()
exit()
This creates the SQLite database file (mindfulchat.db) in your project folder.

Step 5: Add OpenAI API Key
Sign Up for OpenAI:

Go to OpenAI and create an account.

Get your API key from the OpenAI Dashboard.

Add the API Key to app.py:
python
Copy
openai.api_key = 'your-actual-api-key'
Step 6: Create the Frontend
Create a Folder for Templates:

In your project folder, create a folder named templates.

Inside templates, create the following files:

index.html

login.html

register.html

resources.html

mood-history.html

Add HTML Files:

Copy and paste the updated HTML code from the previous response into each respective file.

Add Tailwind CSS:

In each HTML file, add the following line inside the <head> tag:

html
Copy
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
Run HTML
Create a Static Folder:

In your project folder, create a folder named static.

Inside static, create a folder named css.

Inside css, create a file named style.css.

Copy and paste the updated CSS code from the previous response into style.css.

Step 7: Run the Application
Start the Flask Server:

In your terminal, run:

bash
Copy
python app.py
You should see output like:

Copy
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
Open the Application:

Open your browser and go to http://127.0.0.1:5000/.
You should see the MindfulChat homepage.

Step 8: Test the Chatbot
Interact with the Chatbot:

Type a message in the chat input box and press Send.

The chatbot should respond using OpenAI’s GPT-3.

Test Mood Tracking:

Click on the mood buttons (😊, 😐, 😔, etc.) to track your mood.

Check the mood history page (/mood-history) to see your recorded moods.
Test Resources Page:

Visit the resources page (/resources) to see the list of mental health resources.

Step 9: Deploy the Application
Create a GitHub Repository:

Go to GitHub and create a new repository.

Follow the instructions to push your code to GitHub.

Deploy to Heroku:

Sign up for a free account on Heroku.

Install the Heroku CLI from here.
Log in to Heroku:

bash
Copy
heroku login
Create a new Heroku app:

bash
Copy
heroku create
Push your code to Heroku:

bash
Copy
git push heroku main
Open your app:

bash
Copy
heroku open


