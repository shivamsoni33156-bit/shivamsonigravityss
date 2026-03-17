// Auth specific

function login(email, password) {
  return apiCall('/auth/login', {
    method: 'POST',
    body: JSON.stringify({email, password})
  }).then(data => {
    if (data.access_token) {
      setAuth(data.access_token, data.role);
      window.location.href = 'dashboard.html';
    }
  }).catch(err => alert(err.message));
}

function register(username, email, password, role) {
  return apiCall('/auth/register', {
    method: 'POST',
    body: JSON.stringify({username, email, password, role})
  }).then(data => {
    alert('Registered! Please login.');
    window.location.href = 'login.html';
  });
}

// Form handlers
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.onsubmit = (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      login(email, password);
    };
  }

  const regForm = document.getElementById('regForm');
  if (regForm) {
    regForm.onsubmit = (e) => {
      e.preventDefault();
      const username = document.getElementById('username').value;
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      const role = document.getElementById('role').value;
      register(username, email, password, role);
    };
  }
});

