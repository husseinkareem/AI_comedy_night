document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('startCompetition').addEventListener('click', startCompetition);
});

async function startCompetition() {
    const resultsDiv = document.getElementById('results');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const jokeCountInput = document.getElementById('jokeCount');
    const jokeCount = parseInt(jokeCountInput.value);

    if (isNaN(jokeCount) || jokeCount < 1 || jokeCount > 5) {
        resultsDiv.innerHTML = 'Please enter a valid number of jokes (1-5).';
        return;
    }

    // Show loading indicator
    loadingIndicator.classList.remove('hidden');
    resultsDiv.innerHTML = '';

    try {
        const response = await fetch('/run_competition', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ jokeCount: jokeCount }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}, message: ${data.error || 'Unknown error'}`);
        }

        let resultsHtml = `<h2>Theme: ${data.theme}</h2>`;
        data.jokes.forEach((joke, index) => {
            const totalScore = (joke.scores.humor + joke.scores.relevance + joke.scores.creativity) / 3;
            resultsHtml += `
                <div class="joke">
                    <h3>Joke ${index + 1} (${joke.model})</h3>
                    <p>${joke.text}</p>
                    <div class="scores">
                        <p class="score">Humor: ${joke.scores.humor}/10</p>
                        <p class="score">Relevance: ${joke.scores.relevance}/10</p>
                        <p class="score">Creativity: ${joke.scores.creativity}/10</p>
                        <p class="total-score">Total Score: ${totalScore.toFixed(2)}/10</p>
                    </div>
                    <p class="explanation">Explanation: ${joke.explanation}</p>
                </div>
            `;
        });

        resultsDiv.innerHTML = resultsHtml;
    } catch (error) {
        resultsDiv.innerHTML = `An error occurred: ${error.message}`;
        console.error('Error:', error);
    } finally {
        // Hide loading indicator
        loadingIndicator.classList.add('hidden');
    }
}
