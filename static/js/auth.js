// auth.js - Обработка регистрации и авторизации с полной CSRF поддержкой
const API_BASE_URL = 'http://localhost:8000/api/auth/';
const AUTH_TOKEN_KEY = 'lyriquest_auth_token';
const CSRF_TOKEN_KEY = 'csrftoken';

// Получение элементов DOM
const registerForm = document.getElementById('register-form');
const loginForm = document.getElementById('login-form');
const authMessage = document.getElementById('auth-message');

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
    setupForms();
    ensureCSRFToken(); // Убедимся, что CSRF токен есть
});

// Проверка статуса авторизации
function checkAuthStatus() {
    const token = localStorage.getItem(AUTH_TOKEN_KEY);
    if (token && !isTokenExpired(token)) {
        window.location.href = '/index.html';
    }
}

// Проверка истечения срока действия токена (базовая реализация)
function isTokenExpired(token) {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.exp < Date.now() / 1000;
    } catch {
        return true;
    }
}

// Настройка обработчиков форм
function setupForms() {
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
}

// Получение CSRF токена из куки
function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(`${CSRF_TOKEN_KEY}=`))
        ?.split('=')[1];
    return cookieValue;
}

// Запрашиваем CSRF токен, если его нет
async function ensureCSRFToken() {
    if (!getCSRFToken()) {
        try {
            await fetch(API_BASE_URL + 'csrf/', {
                method: 'GET',
                credentials: 'include'
            });
        } catch (error) {
            console.error('CSRF token fetch error:', error);
        }
    }
}

// Обработка регистрации
async function handleRegister(e) {
    e.preventDefault();
    
    const formData = {
        username: registerForm.querySelector('#username').value.trim(),
        email: registerForm.querySelector('#email').value.trim(),
        password: registerForm.querySelector('#password').value,
        password2: registerForm.querySelector('#password2').value
    };

    // Валидация
    if (formData.password !== formData.password2) {
        showMessage('Пароли не совпадают', 'error');
        return;
    }

    if (!formData.username || !formData.email) {
        showMessage('Все поля обязательны для заполнения', 'error');
        return;
    }

    try {
        // Убедимся, что CSRF токен есть
        await ensureCSRFToken();
        
        const response = await fetch(API_BASE_URL + 'register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() || ''
            },
            body: JSON.stringify(formData),
            credentials: 'include'
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('Регистрация успешна! Проверьте email для подтверждения.', 'success');
            registerForm.reset();
            setTimeout(() => showLogin(), 2000);
        } else {
            const error = Object.values(data).flat().join(' ') || 'Ошибка регистрации';
            showMessage(error, 'error');
        }
    } catch (error) {
        showMessage('Сервер недоступен', 'error');
        console.error('Registration error:', error);
    }
}

// Обработка входа
async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;

    if (!username || !password) {
        showMessage('Введите имя пользователя и пароль', 'error');
        return;
    }

    try {
        await ensureCSRFToken();
        
        const response = await fetch(`${API_BASE_URL}login/`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() || ''
            },
            body: JSON.stringify({ username, password }),
            credentials: 'include'
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem(AUTH_TOKEN_KEY, data.access);
            
            // Сохраняем refresh токен в httpOnly куки через сервер
            await fetch(`${API_BASE_URL}set_refresh_cookie/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${data.access}`
                },
                credentials: 'include'
            });
            
            window.location.href = '/index.html';
        } else {
            showMessage(data.detail || 'Неверные учетные данные', 'error');
        }
    } catch (error) {
        showMessage('Сервер недоступен', 'error');
        console.error('Login error:', error);
    }
}

// Выход из системы
async function logout() {
    try {
        await fetch(`${API_BASE_URL}logout/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem(AUTH_TOKEN_KEY)}`
            },
            credentials: 'include'
        });
    } catch (error) {
        console.error('Logout error:', error);
    }
    
    localStorage.removeItem(AUTH_TOKEN_KEY);
    window.location.href = '/regaut.html';
}

// Показать сообщение
function showMessage(text, type) {
    if (!authMessage) return;
    
    authMessage.textContent = text;
    authMessage.className = `alert alert-${type}`;
    authMessage.style.display = 'block';
    
    setTimeout(() => {
        authMessage.style.display = 'none';
    }, 5000);
}

// Переключение между формами
function showRegister() {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
    document.getElementById('auth-message').style.display = 'none';
}

function showLogin() {
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('auth-message').style.display = 'none';
}

// Экспорт функций в глобальную область видимости
window.showRegister = showRegister;
window.showLogin = showLogin;
window.logout = logout;