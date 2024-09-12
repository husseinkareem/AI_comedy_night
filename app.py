from flask import Flask, jsonify, render_template
from joke_competition import generate_theme_and_jokes, score_jokes
import webbrowser
import threading
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_competition', methods=['POST'])
def run_competition():
    theme, jokes = generate_theme_and_jokes(3)  # Generate 3 jokes
    scores, explanations = score_jokes(theme, jokes)
    
    result = {
        "theme": theme,
        "jokes": [
            {"text": joke, "score": score, "explanation": explanation}
            for joke, score, explanation in zip(jokes, scores, explanations)
        ]
    }
    
    return jsonify(result)

def open_browser():
    """Open the browser after a short delay."""
    time.sleep(1)
    webbrowser.open_new('http://localhost:5000/')

if __name__ == '__main__':
    # Start the browser-opening thread
    threading.Thread(target=open_browser).start()
    
    # Start the Flask app
    app.run(debug=True)