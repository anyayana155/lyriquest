// class MusicPlayer {
//     constructor() {
//         this.audioPlayer = document.getElementById('audio-player');
//         this.searchResults = document.getElementById('search-results');
//         this.initEventListeners();
//     }

//     initEventListeners() {
//         const searchForm = document.getElementById('search-form');
//         if (searchForm) {
//             searchForm.addEventListener('submit', (e) => this.handleSearch(e));
//         }
//     }

//     async handleSearch(e) {
//         e.preventDefault();
//         const query = document.getElementById('search-query').value.trim();
        
//         if (!query) return;

//         try {
//             const response = await fetch(`/api/music/youtube/search/?q=${encodeURIComponent(query)}`);
//             const tracks = await response.json();
//             this.displaySearchResults(tracks);
//         } catch (error) {
//             console.error('Search error:', error);
//             this.searchResults.innerHTML = '<p>Error searching for tracks</p>';
//         }
//     }

//     displaySearchResults(tracks) {
//         this.searchResults.innerHTML = '';
        
//         if (!tracks || tracks.length === 0) {
//             this.searchResults.innerHTML = '<p>No tracks found</p>';
//             return;
//         }

//         tracks.forEach(track => {
//             const trackElement = document.createElement('div');
//             trackElement.className = 'track';
//             trackElement.innerHTML = `
//                 <img src="${track.thumbnail_url}" width="120" alt="${track.title}">
//                 <div class="track-info">
//                     <h4>${track.title}</h4>
//                     <p>${track.artist}</p>
//                     <button data-id="${track.youtube_id}">Play</button>
//                 </div>
//             `;
//             trackElement.querySelector('button').addEventListener('click', () => this.playTrack(track.youtube_id));
//             this.searchResults.appendChild(trackElement);
//         });
//     }

//     async playTrack(youtubeId) {
//         try {
//             console.log(`Attempting to play track: ${youtubeId}`);
            
//             const response = await fetch(`/api/music/youtube/audio/?id=${youtubeId}`);
//             const data = await response.json();
            
//             if (data.audio_url) {
//                 console.log(`Audio URL received: ${data.audio_url}`);
                
//                 // Останавливаем текущее воспроизведение
//                 this.audioPlayer.pause();
                
//                 // Устанавливаем новый источник
//                 this.audioPlayer.src = data.audio_url;
                
//                 // Добавляем обработчик ошибок
//                 this.audioPlayer.onerror = () => {
//                     console.error('Audio playback error:', this.audioPlayer.error);
//                     alert('Error playing audio. Please try another track.');
//                 };
                
//                 // Пытаемся воспроизвести
//                 const playPromise = this.audioPlayer.play();
                
//                 if (playPromise !== undefined) {
//                     playPromise.catch(error => {
//                         console.error('Playback failed:', error);
//                         alert('Playback failed. Please try another track.');
//                     });
//                 }
//             } else {
//                 throw new Error('No audio URL provided');
//             }
//         } catch (error) {
//             console.error('Error playing track:', error);
//             alert('Could not play track. Please try again.');
//         }
//     }
// }

// // Инициализация при загрузке страницы
// document.addEventListener('DOMContentLoaded', () => {
//     window.musicPlayer = new MusicPlayer();
// });
