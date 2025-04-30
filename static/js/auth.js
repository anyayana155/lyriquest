// auth.js - Обработка регистрации и авторизации
const API_BASE_URL = 'http://localhost:8000/api/auth/'; 
const AUTH_TOKEN_KEY = 'lyriquest_auth_token';
const registerForm = document.getElementById('register-form');
const loginForm = document.getElementById('login-form');
const authMessage = document.getElementById('auth-message');

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
    setupForms();
});

// Проверка статуса авторизации
function checkAuthStatus() {
    const token = localStorage.getItem(AUTH_TOKEN_KEY);
    if (token) {
        // Пользователь авторизован - перенаправляем
        window.location.href = '/index.html';
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

// Обработка регистрации
async function handleRegister(e) {
    e.preventDefault();
    
    const formData = {
        username: registerForm.querySelector('#username').value,
        email: registerForm.querySelector('#email').value,
        password: registerForm.querySelector('#password').value,
        password2: registerForm.querySelector('#password2').value
    };

    if (formData.password !== formData.password2) {
        showMessage('Пароли не совпадают', 'error');
        return;
    }

    try {
        const response = await fetch(API_BASE_URL + 'register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: formData.username,
                email: formData.email,
                password: formData.password,
                password2: formData.password2
            })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('Регистрация успешна! Проверьте email для подтверждения.', 'success');
            registerForm.reset();
        } else {
            const error = data.email?.[0] || data.username?.[0] || data.password?.[0] || 'Ошибка регистрации';
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
    const username = document.getElementById('username').value; // Изменил с #login-username
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}login/`, {  // Добавил / в конце
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();

        if (response.ok) {
            // Сохраняем токен
            localStorage.setItem(AUTH_TOKEN_KEY, data.access);
            
            // Перенаправляем
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
function logout() {
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
function showRegister() {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
}

function showLogin() {
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('login-form').style.display = 'block';
}

window.showRegister = showRegister;
window.showLogin = showLogin;
window.logout = logout;