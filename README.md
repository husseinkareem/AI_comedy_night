# AI Comedy Night 🎭🤖

![AI Comedy Night Logo](images/logo.webp "AI Comedy Night Logo")

## Översikt

AI Comedy Night är en interaktiv webbapplikation som använder artificiell intelligens för att generera och bedöma skämt. Användare kan starta en skämttävling där AI:n genererar skämt baserade på ett slumpmässigt tema och sedan bedömer dem.

![App Screenshot](path/to/app_screenshot.png)
<!-- Lägg till en skärmdump av applikationens huvudgränssnitt -->

## Funktioner

- 🎲 Slumpmässig temgenerering för varje skämttävling
- 🤣 AI-genererade skämt baserade på temat
- 🏆 Automatisk bedömning av skämt med poäng och förklaringar
- 🔢 Flexibelt antal skämt (1-5) per tävling
- 💻 Responsivt och användarvänligt gränssnitt

## Teknisk Stack

- **Backend**: Python med Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI**: OpenAI's GPT-3.5 Turbo
- **Styling**: Custom CSS med responsiv design

## Installation

1. Klona repositoryt:
   ```
   git clone https://github.com/yourusername/ai-comedy-night.git
   cd ai-comedy-night
   ```

2. Installera beroenden:
   ```
   pip install -r requirements.txt
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
<!-- GIF som visar hur man använder applikationen -->

1. Ange antalet skämt du vill generera (1-5)
2. Klicka på "Start Competition"
3. Vänta medan AI:n genererar temat och skämten
4. Läs skämten, deras poäng och förklaringar
5. Skratta (förhoppningsvis)!

## Projektstruktur

- `app.py`: Huvudapplikationsfil med Flask-servern
- `joke_competition.py`: Logik för skämtgenerering och bedömning
- `static/`: Innehåller CSS och JavaScript filer
- `templates/`: Innehåller HTML-mallar
- `main.py`: Skript för att köra tävlingen i terminalen (alternativ användning)

## Framtida Förbättringar

- [ ] Implementera användarautentisering
- [ ] Lägga till en highscore-lista för de bästa skämten
- [ ] Skapa en funktion för användargenererade teman
- [ ] Integrera text-till-tal för uppläsning av skämt
- [ ] Utöka med fler språkalternativ

## Bidra

Vi välkomnar bidrag till AI Comedy Night! Följ dessa steg:

1. Forka repositoryt
2. Skapa en ny branch (`git checkout -b feature/AmazingFeature`)
3. Commita dina ändringar (`git commit -m 'Add some AmazingFeature'`)
4. Pusha till branchen (`git push origin feature/AmazingFeature`)
5. Öppna en Pull Request


## Kontakt

Projektlänk: [https://github.com/yourusername/ai-comedy-night](https://github.com/yourusername/ai-comedy-night)
