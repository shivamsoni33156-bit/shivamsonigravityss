// Payments

document.addEventListener('DOMContentLoaded', () => {
  loadHistory();
  
  const form = document.getElementById('paymentForm');
  form.onsubmit = (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('course_id', document.getElementById('course_id').value);
    formData.append('amount', document.getElementById('amount').value);
    const proof = document.getElementById('proof').files[0];
    if (proof) formData.append('proof', proof);

    fetch('http://localhost:5000/api/payments/submit', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      alert(data.message);
      form.reset();
      loadHistory();
    })
    .catch(err => alert(err));
  };
});

function loadHistory() {
  apiCall('/payments/history')
    .then(payments => {
      document.getElementById('historyList').innerHTML = payments.map(p => 
        `<div class="card">${p.course_id} - ₹${p.amount} - ${p.status}</div>`
      ).join('');
    });
}

