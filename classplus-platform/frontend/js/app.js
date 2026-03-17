// Common API Helper with JWT

const API_BASE = 'http://localhost:5000/api';

let token = localStorage.getItem('token');
let userRole = localStorage.getItem('role');

function setAuth(tokenVal, roleVal) {
  token = tokenVal;
  userRole = roleVal;
  localStorage.setItem('token', token);
  localStorage.setItem('role', userRole);
}

function apiCall(endpoint, options = {}) {
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    },
    ...options
  };
  return fetch(`${API_BASE}${endpoint}`, config)
    .then(res => {
      if (res.status === 401) {
        logout();
        throw new Error('Unauthorized');
      }
      return res.json();
    });
}

function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  window.location.href = 'login.html';
}

function showRoleContent() {
  const roleSections = document.querySelectorAll('[data-role]');
  roleSections.forEach(sec => {
    sec.style.display = sec.dataset.role === userRole ? 'block' : 'none';
  });
}

// Sidebar toggle
function toggleSidebar() {
  document.querySelector('.sidebar').classList.toggle('mobile-hidden');
}

// Sidebar toggle
function toggleSidebar() {
  document.querySelector('.sidebar').classList.toggle('mobile-hidden');
}

function loadPage(page) {
  window.location.href = page;
}

// Init on load
document.addEventListener('DOMContentLoaded', () => {
  if (token) {
    showRoleContent();
  }
  if (!token && (window.location.pathname.includes('dashboard') || window.location.pathname.includes('courses'))) {
    window.location.href = 'login.html';
  }
});

