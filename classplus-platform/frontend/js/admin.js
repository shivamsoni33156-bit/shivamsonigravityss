// Admin

function loadUsers() {
  apiCall('/admin/users')
    .then(users => {
      document.getElementById('adminData').innerHTML = '<h3>Users</h3>' + users.map(u => `<div class="card">${u.username} (${u.role})</div>`).join('');
    });
}

function loadPendingPayments() {
  apiCall('/admin/payments/pending')
    .then(payments => {
      document.getElementById('adminData').innerHTML = '<h3>Pending Payments</h3>' + payments.map(p => `<div class="card">Payment ${p.id} for course ${p.course_id} ₹${p.amount}</div>`).join('');
    });
}

function loadPendingEnrolls() {
  apiCall('/admin/enrollments/pending')
    .then(enrolls => {
      document.getElementById('adminData').innerHTML = '<h3>Pending Enrollments</h3>' + enrolls.map(e => `<div class="card">Student ${e.student_id} for course ${e.course_id}</div>`).join('');
    });
}

