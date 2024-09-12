import os
from openai import OpenAI
from dotenv import load_dotenv
from functools import lru_cache
import json

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class APIError(Exception):
    """Custom exception for API-related errors"""
    pass

@lru_cache(maxsize=100)
def openai_chat_completion_cached(messages_json, temperature):
    """Cached wrapper for OpenAI ChatCompletion."""
    messages = json.loads(messages_json)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise APIError(f"OpenAI API error: {str(e)}")

def openai_chat_completion(messages, temperature=0.7):
    """Wrapper for the cached OpenAI ChatCompletion function."""
    messages_json = json.dumps(messages)
    return openai_chat_completion_cached(messages_json, temperature)

def generate_theme_and_jokes(num_jokes=3):
    """Generate a theme and jokes in a single API call."""
    messages = [
        {"role": "system", "content": "You are a creative theme generator and comedian. Generate a short, interesting theme for a joke competition, followed by the specified number of jokes based on that theme."},
        {"role": "user", "content": f"Generate a theme for a joke competition and exactly {num_jokes} joke(s) based on that theme. Format your response as follows:\nTheme: [theme]\nJoke 1: [joke1]\nJoke 2: [joke2]\n... (continue for the specified number of jokes)"}
    ]
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response = openai_chat_completion(messages)
            if response:
                lines = response.split('\n')
                theme = None
                jokes = []
                for line in lines:
                    if line.startswith("Theme:"):
                        theme = line.split(":", 1)[1].strip()
                    elif line.startswith("Joke"):
                        joke = line.split(":", 1)[1].strip()
                        jokes.append(joke)
                
                if theme is None or len(jokes) != num_jokes:
                    if attempt < max_attempts - 1:
                        print(f"Attempt {attempt + 1} failed. Retrying...")
                        continue
                    else:
                        raise APIError(f"Failed to generate correct number of jokes after {max_attempts} attempts.")
                return theme, jokes
            else:
                raise APIError("No response received from the API")
        except Exception as e:
            if attempt < max_attempts - 1:
                print(f"Attempt {attempt + 1} failed. Retrying...")
            else:
                print(f"Error generating theme and jokes: {str(e)}")
                raise APIError(f"Error generating theme and jokes: {str(e)}")

def score_jokes(theme, jokes):
    """Score multiple jokes in a single API call."""
    jokes_text = "\n".join([f"Joke {i+1}: {joke}" for i, joke in enumerate(jokes)])
    messages = [
        {"role": "system", "content": "You are a joke evaluator. Score the given jokes based on humor, relevance to the theme, and creativity. Provide a score out of 10 and a brief explanation for each joke."},
        {"role": "user", "content": f"Theme: {theme}\n{jokes_text}\nScore each joke out of 10 and explain your rating. Format your response as follows:\nJoke 1 Score: [score]\nJoke 1 Explanation: [explanation]\n"}
    ]
    try:
        response = openai_chat_completion(messages)
        if response:
            lines = response.split('\n')
            scores = []
            explanations = []
            current_explanation = ""
            for line in lines:
                if line.startswith("Joke") and "Score:" in line:
                    if current_explanation:
                        explanations.append(current_explanation.strip())
                        current_explanation = ""
                    score = line.split("Score:", 1)[1].strip()
                    scores.append(score)
                elif line.startswith("Explanation:"):
                    current_explanation = line.split("Explanation:", 1)[1].strip()
                else:
                    current_explanation += " " + line.strip()
            
            if current_explanation:
                explanations.append(current_explanation.strip())

            if len(scores) != len(jokes) or len(explanations) != len(jokes):
                raise APIError(f"Mismatch in number of jokes and scores/explanations. Jokes: {len(jokes)}, Scores: {len(scores)}, Explanations: {len(explanations)}")
            return scores, explanations
        else:
            raise APIError("No response received from the API")
    except Exception as e:
        print(f"Error scoring jokes: {str(e)}")
        raise APIError(f"Error scoring jokes: {str(e)}")