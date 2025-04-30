const API_URL = 'http://localhost:8000/api/'; 
// Проверка авторизации при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});
async function checkAuth() {
    const token = localStorage.getItem('access_token');
    const currentPage = window.location.pathname;
    
    // Если пользователь не авторизован и не на странице входа/регистрации
    if (!token && !['/regaut.html', '/'].includes(currentPage)) {
        window.location.href = '/regaut.html';
        return;
    }
    
    // Если пользователь авторизован
    if (token) {
        try {
            const response = await fetch(`${API_URL}users/me/`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!response.ok) throw new Error('Невалидный токен');
            
            const userData = await response.json();
            updateUI(userData);
        } catch (error) {
            console.error('Ошибка проверки авторизации:', error);
            logout();
        }
    }
}

function updateUI(userData) {
    // Обновляем имя пользователя во всех элементах с классом 'username'
    document.querySelectorAll('.username').forEach(el => {
        el.textContent = userData.username;
    });
    
    // Показываем элементы для авторизованных пользователей
    document.querySelectorAll('.auth-only').forEach(el => {
        el.style.display = 'block';
    });
    
    // Скрываем элементы для гостей
    document.querySelectorAll('.guest-only').forEach(el => {
        el.style.display = 'none';
    });
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/regaut.html';
}

// Делаем функцию доступной глобально
window.logout = logout;