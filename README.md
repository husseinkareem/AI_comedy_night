# AI Comedy Night 🎭🤖

![AI Comedy Night Logo](images/logo.webp "AI Comedy Night Logo")

## Översikt

AI Comedy Night är en interaktiv webbapplikation som använder artificiell intelligens för att generera och bedöma skämt. Användare kan starta en skämttävling där AI:n genererar skämt baserade på ett slumpmässigt tema och sedan bedömer dem.

![App Screenshot](images/app.png)

## Funktioner

- 🎲 Slumpmässig temgenerering för varje skämttävling
- 🤣 AI-genererade skämt baserade på temat
- 🏆 Automatisk bedömning av skämt med poäng och förklaringar
- 🔢 Flexibelt antal skämt (1-5) per tävling
- 💻 Responsivt och användarvänligt gränssnitt

## Teknisk Stack

- **Backend**: Python med Quart (asynkron version av Flask)
- **Frontend**: HTML, CSS, JavaScript
- **AI**: OpenAI's GPT-3.5 Turbo och GPT-4
- **Styling**: Custom CSS med responsiv design

## Installation

1. Klona repositoryt:
   ```
   git clone https://github.com/husseinkareem/AI_comedy_night.git
   cd AI_comedy_night
   ```

2. Installera de nödvändiga paketen:
   ```
   pip install quart openai python-dotenv tenacity
   ```

3. Skapa en `.env` fil i projektets rotmapp och lägg till din OpenAI API-nyckel:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. Kör applikationen:
   ```
   python app.py
   ```

5. Öppna en webbläsare och gå till `http://localhost:5001`

## Användning

![Usage GIF](path/to/usage.gif)

1. Ange antalet skämt du vill generera (1-5)
2. Klicka på "Start Competition"
3. Vänta medan AI:n genererar temat och skämten
4. Läs skämten, deras poäng och förklaringar
5. Skratta (förhoppningsvis)!

## Projektstruktur

- `app.py`: Huvudapplikationsfil med Quart-servern
- `joke_competition.py`: Logik för skämtgenerering och bedömning
- `static/`: Innehåller CSS och JavaScript filer
- `templates/`: Innehåller HTML-mallar

## Framtida Förbättringar

- [ ] Implementera användarautentisering
- [ ] Lägga till en highscore-lista för de bästa skämten
- [ ] Skapa en funktion för användargenererade teman
- [ ] Integrera text-till-tal för uppläsning av skämt
- [ ] Utöka med fler språkalternativ
- [ ] Optimera prestanda för snabbare generering av skämt

Projektlänk: [https://github.com/husseinkareem/AI_comedy_night](https://github.com/husseinkareem/AI_comedy_night)