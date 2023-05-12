from flask import Flask, render_template, request
import openai
import json

app = Flask(__name__)

openai.api_key = "YOUR_API_KEY_HERE"

@app.route('/')
def index():
    return render_template('../public/index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Extrahieren wir den Text, den der Benutzer eingegeben hat
    user_input = request.form['text']
    
    # Erstellen wir eine Anfrage an OpenAI
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    # Extrahieren wir die Antwort von OpenAI
    chat
