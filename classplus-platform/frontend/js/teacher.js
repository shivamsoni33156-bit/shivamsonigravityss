// Teacher specific

function loadCourses() {
  apiCall('/teacher/courses')
    .then(courses => {
      const grid = document.getElementById('coursesList');
      grid.innerHTML = courses.map(course => `
        <div class="course-card">
          <div class="course-image">${course.title[0]}</div>
          <div class="course-info">
            <h4>${course.title}</h4>
            <p>₹${course.price}</p>
            <button class="btn" onclick="uploadToCourse(${course.id})">Add Material</button>
          </div>
        </div>
      `).join('') || '<p>No courses yet.</p>';
    });
}

document.addEventListener('DOMContentLoaded', () => {
  if (userRole !== 'teacher') return;

  // Courses page
  const courseForm = document.getElementById('courseForm');
  if (courseForm) {
    courseForm.onsubmit = (e) => {
      e.preventDefault();
      apiCall('/teacher/courses', {
        method: 'POST',
        body: JSON.stringify({
          title: document.getElementById('title').value,
          description: document.getElementById('description').value,
          price: parseFloat(document.getElementById('price').value)
        })
      }).then(() => {
        alert('Course created!');
        courseForm.reset();
        loadCourses();
      });
    };
    loadCourses();
  }

  // Dashboard data
  const cards = document.getElementById('teacherCards');
  if (cards) {
    apiCall('/teacher/dashboard')
      .then(data => {
        document.getElementById('totalStudents').textContent = data.total_students;
        document.getElementById('totalCourses').textContent = data.total_courses;
        document.getElementById('earnings').textContent = `₹${data.earnings}`;
      });
  }
});

