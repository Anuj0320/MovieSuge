const recommendBtn = document.getElementById('recommendBtn');
const movieInput = document.getElementById('movieInput');
const recommendationsContainer = document.getElementById('recommendations');
const loader = document.getElementById('loader');

recommendBtn.addEventListener('click', async () => {
    const movieName = movieInput.value.trim();

    if (!movieName) {
        alert("Please enter a movie name!");
        return;
    }

    // UI Feedback
    recommendationsContainer.innerHTML = '';
    loader.classList.remove('hidden');

    try {
        const response = await fetch('http://127.0.0.1:5000/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ movie: movieName })
        });

        const data = await response.json();
        loader.classList.add('hidden');

        if (data.success) {
            displayMovies(data.movies);
        } else {
            recommendationsContainer.innerHTML = `<p class="error-msg">${data.message}</p>`;
        }
    } catch (error) {
        loader.classList.add('hidden');
        alert("Make sure your Python server (app.py) is running!");
        console.error("Error:", error);
    }
});

function displayMovies(movies) {
    recommendationsContainer.innerHTML = ''; // Clear previous
    movies.forEach(movie => {
        const card = document.createElement('div');
        card.className = 'movie-card';
        card.innerHTML = `
            <img src="${movie.poster}" alt="${movie.title}" loading="lazy">
            <div class="movie-info">
                <h3>${movie.title}</h3>
            </div>
        `;
        recommendationsContainer.appendChild(card);
    });
}