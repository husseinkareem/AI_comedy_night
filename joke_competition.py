import os
import openai
from dotenv import load_dotenv
from functools import lru_cache

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@lru_cache(maxsize=100)
def openai_chat_completion(messages, temperature=0.7):
    """Cached wrapper for OpenAI ChatCompletion."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return None

def generate_theme_and_jokes(num_jokes=3):
    """Generate a theme and jokes in a single API call."""
    messages = [
        {"role": "system", "content": "You are a creative theme generator and comedian. Generate a short, interesting theme for a joke competition, followed by the specified number of jokes based on that theme."},
        {"role": "user", "content": f"Generate a theme for a joke competition and {num_jokes} jokes based on that theme. Format your response as follows:\nTheme: [theme]\nJoke 1: [joke1]\nJoke 2: [joke2]\n..."}
    ]
    response = openai_chat_completion(tuple(messages))
    if response:
        lines = response.split('\n')
        theme = lines[0].replace("Theme: ", "").strip()
        jokes = [line.split(": ", 1)[1] for line in lines[1:] if line.startswith("Joke")]
        return theme, jokes
    return None, []

def score_jokes(theme, jokes):
    """Score multiple jokes in a single API call."""
    jokes_text = "\n".join([f"Joke {i+1}: {joke}" for i, joke in enumerate(jokes)])
    messages = [
        {"role": "system", "content": "You are a joke evaluator. Score the given jokes based on humor, relevance to the theme, and creativity. Provide a score out of 10 and a brief explanation for each joke."},
        {"role": "user", "content": f"Theme: {theme}\n{jokes_text}\nScore each joke out of 10 and explain your rating. Format your response as follows:\nJoke 1 Score: [score]\nJoke 1 Explanation: [explanation]\nJoke 2 Score: [score]\nJoke 2 Explanation: [explanation]\n..."}
    ]
    response = openai_chat_completion(tuple(messages))
    if response:
        lines = response.split('\n')
        scores = []
        explanations = []
        for i in range(0, len(lines), 2):
            if i+1 < len(lines):
                scores.append(lines[i].split(": ", 1)[1])
                explanations.append(lines[i+1].split(": ", 1)[1])
        return scores, explanations
    return [], []