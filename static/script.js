document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('startCompetition').addEventListener('click', startCompetition);
});

async function startCompetition() {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = 'Loading...';

    try {
        const response = await fetch('/run_competition', { method: 'POST' });
        const data = await response.json();

        let resultsHtml = `<h2>Theme: ${data.theme}</h2>`;
        data.jokes.forEach((joke, index) => {
            resultsHtml += `
                <div class="joke">
                    <h3>Joke ${index + 1}</h3>
                    <p>${joke.text}</p>
                    <p>Score: ${joke.score}</p>
                    <p>Explanation: ${joke.explanation}</p>
                </div>
            `;
        });

        resultsDiv.innerHTML = resultsHtml;
    } catch (error) {
        resultsDiv.innerHTML = 'An error occurred. Please try again.';
        console.error('Error:', error);
    }
}
