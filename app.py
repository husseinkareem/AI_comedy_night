from flask import Flask, jsonify, render_template
from joke_competition import generate_theme_and_jokes, score_jokes, APIError
import webbrowser
import threading
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_competition', methods=['POST'])
def run_competition():
    try:
        theme, jokes = generate_theme_and_jokes(3)  # Generate 3 jokes
        if theme is None or not jokes:
            return jsonify({"error": "Failed to generate theme and jokes"}), 500
        
        scores, explanations = score_jokes(theme, jokes)
        if not scores or not explanations:
            return jsonify({"error": "Failed to score jokes"}), 500
        
        result = {
            "theme": theme,
            "jokes": [
                {"text": joke, "score": score, "explanation": explanation}
                for joke, score, explanation in zip(jokes, scores, explanations)
            ]
        }
        
        return jsonify(result)
    except APIError as e:
        return jsonify({"error": str(e)}), 500

def open_browser():
    """Open the browser after a short delay."""
    time.sleep(1)
    webbrowser.open_new('http://localhost:5000/')

if __name__ == '__main__':
    # Start the browser-opening thread
    threading.Thread(target=open_browser).start()
    
    # Start the Flask app
    app.run(debug=True)