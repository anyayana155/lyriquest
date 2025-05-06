document.addEventListener('DOMContentLoaded', () => {
  const audioPlayer = document.getElementById('audio-player');
  const searchForm = document.getElementById('music-search-form');
  const resultsContainer = document.getElementById('music-results');
  
  if (searchForm) {
      searchForm.addEventListener('submit', async (e) => {
          e.preventDefault();
          const query = document.getElementById('music-search-input').value;
          
          try {
              const response = await fetch(`/api/music/jamendo/search/?q=${encodeURIComponent(query)}`);
              const data = await response.json();
              
              resultsContainer.innerHTML = '';
              data.forEach(track => {
                  const trackElement = document.createElement('div');
                  trackElement.className = 'music-track';
                  trackElement.innerHTML = `
                      <h3>${track.name} - ${track.artist_name}</h3>
                      <img src="${track.image}" alt="Cover" width="100">
                      <button onclick="playTrack('${track.audio}')">Play</button>
                      <button onclick="importTrack('${track.id}')">Import</button>
                  `;
                  resultsContainer.appendChild(trackElement);
              });
          } catch (error) {
              console.error('Search error:', error);
          }
      });
  }
});

function playTrack(audioUrl) {
  const audioPlayer = document.getElementById('audio-player');
  audioPlayer.src = audioUrl;
  audioPlayer.play();
}

async function importTrack(jamendoId) {
  try {
      const response = await fetch('/api/music/jamendo/import/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCSRFToken(),
          },
          body: JSON.stringify({ jamendo_id: jamendoId })
      });
      
      if (response.ok) {
          alert('Track imported successfully!');
      } else {
          const error = await response.json();
          alert(error.error || 'Import failed');
      }
  } catch (error) {
      console.error('Import error:', error);
      alert('Import failed');
  }
}

// Вспомогательная функция для получения CSRF токена
function getCSRFToken() {
  const cookieValue = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1];
  return cookieValue;
}