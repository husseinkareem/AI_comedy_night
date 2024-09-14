from quart import Quart, jsonify, render_template, request
from joke_competition import generate_theme_and_jokes, score_jokes, APIError
import traceback
import logging
import webbrowser
import asyncio

app = Quart(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/run_competition', methods=['POST'])
async def run_competition():
    try:
        app.logger.debug("Received request to run competition")
        data = await request.json
        joke_count = data.get('jokeCount', 1)  # Default to 1 if not provided

        app.logger.debug(f"Joke count: {joke_count}")

        # Validate joke count
        if not isinstance(joke_count, int) or joke_count < 1 or joke_count > 5:
            app.logger.warning(f"Invalid joke count: {joke_count}")
            return jsonify({"error": "Invalid number of jokes. Please choose between 1 and 5."}), 400

        app.logger.debug(f"Generating {joke_count} jokes")
        theme, jokes_with_models = await generate_theme_and_jokes(joke_count)
        app.logger.debug(f"Generated theme: {theme}")
        app.logger.debug(f"Generated jokes: {jokes_with_models}")
        app.logger.debug(f"Number of generated jokes: {len(jokes_with_models)}")

        if len(jokes_with_models) != joke_count:
            raise APIError(f"Generated {len(jokes_with_models)} jokes instead of the requested {joke_count}")

        app.logger.debug(f"Scoring jokes")
        jokes_scores = await score_jokes(theme, jokes_with_models)
        app.logger.debug(f"Scores and explanations: {jokes_scores}")

        result = {
            "theme": theme,
            "jokes": [
                {
                    "text": joke,
                    "model": model,
                    "scores": scores,
                    "explanation": explanation
                }
                for (joke, model), (scores, explanation) in zip(jokes_with_models, jokes_scores)
            ]
        }
        
        app.logger.debug(f"Returning result: {result}")
        return jsonify(result)
    except APIError as e:
        app.logger.error(f"API Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": "An unexpected error occurred"}), 500

def open_browser():
    webbrowser.open_new('http://localhost:5001/')

if __name__ == '__main__':
    import threading
    threading.Thread(target=open_browser).start()
    app.run(debug=True, port=5001)