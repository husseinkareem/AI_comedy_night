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

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

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
        resultsDiv.innerHTML = `An error occurred: ${error.message}`;
        console.error('Error:', error);
    } finally {
        // Hide loading indicator
        loadingIndicator.classList.add('hidden');
    }
}
