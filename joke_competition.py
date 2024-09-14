import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import logging
import asyncio
from tenacity import retry, stop_after_attempt, wait_random_exponential

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class APIError(Exception):
    """Custom exception for API-related errors"""
    pass

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
async def generate_theme():
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Generate a short, interesting theme for a joke competition."},
            {"role": "user", "content": "Theme:"}
        ],
        max_tokens=20,
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
async def generate_joke(theme, model):
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a comedian. Generate a short joke based on the given theme."},
            {"role": "user", "content": f"Theme: {theme}\nJoke:"}
        ],
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].message.content.strip(), model

async def generate_theme_and_jokes(joke_count):
    theme = await generate_theme()
    models = ["gpt-3.5-turbo", "gpt-4", "gpt-3.5-turbo-16k"] * (joke_count // 3 + 1)
    tasks = [generate_joke(theme, models[i]) for i in range(joke_count)]
    jokes_with_models = await asyncio.gather(*tasks)
    return theme, jokes_with_models

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(5))
async def score_jokes(theme, jokes_with_models):
    jokes_text = "\n".join([f"Joke {i+1} (by {model}): {joke}" for i, (joke, model) in enumerate(jokes_with_models)])
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a joke evaluator. Score the given jokes based on humor, relevance to the theme, and creativity. Provide separate scores out of 10 for each category and a brief explanation."},
            {"role": "user", "content": f"Theme: {theme}\n{jokes_text}\nScore each joke out of 10 for humor, relevance, and creativity. Provide a brief explanation. Format your response as follows:\nJoke 1:\nHumor: [score]/10\nRelevance: [score]/10\nCreativity: [score]/10\nExplanation: [explanation]\n"}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    
    content = response.choices[0].message.content
    logging.debug(f"Raw GPT-4 response: {content}")
    jokes_scores = []
    for joke_eval in content.split('Joke ')[1:]:
        lines = joke_eval.split('\n')
        scores = {}
        explanation = "No explanation provided."
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                if key in ['humor', 'relevance', 'creativity']:
                    scores[key] = int(value.split('/')[0])
                elif key == 'explanation':
                    explanation = value
        jokes_scores.append((scores, explanation))
    
    logging.debug(f"Parsed scores: {jokes_scores}")
    
    if len(jokes_scores) != len(jokes_with_models):
        raise APIError(f"Mismatch in number of jokes and evaluations. Jokes: {len(jokes_with_models)}, Evaluations: {len(jokes_scores)}")
    
    return jokes_scores