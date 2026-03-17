// Student specific

document.addEventListener('DOMContentLoaded', () => {
  if (userRole !== 'student') return;

  // For dashboard enrolled courses
  apiCall('/student/courses')
    .then(courses => {
      const grid = document.getElementById('studentCourses');
      grid.innerHTML = courses.map(course => `
        <div class="course-card">
          <div class="course-image">📚</div>
          <div class="course-info">
            <div class="course-title">${course.title}</div>
            <button class="btn" onclick="loadMaterials(${course.id})">View Materials</button>
          </div>
        </div>
      `).join('');
    })
    .catch(err => console.error(err));
});

