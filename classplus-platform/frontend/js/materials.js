// Materials

let currentCourseId = new URLSearchParams(window.location.search).get('course') || document.getElementById('courseId').textContent;

function loadCurrentMaterials() {
  const courseId = parseInt(new URLSearchParams(window.location.search).get('course') || prompt('Enter Course ID'));
  if (!courseId) return;

  document.getElementById('courseId').textContent = courseId;

  apiCall(`/student/materials/${courseId}`)
    .then(materials => {
      const grid = document.getElementById('materialsList');
      grid.innerHTML = materials.map(m => `
        <div class="course-card">
          <div class="course-image">${m.type.toUpperCase()}</div>
          <div class="course-info">
            <h4>${m.title}</h4>
            <a href="http://localhost:5000/api/student/material/${courseId}/${m.file_path}" class="btn" download>Download</a>
            ${m.type === 'video' ? `<video controls src="http://localhost:5000/api/student/material/${courseId}/${m.file_path}" style="width: 300px; height: 200px;"></video>` : ''}
          </div>
        </div>
      `).join('');
    })
    .catch(err => alert('Access denied or no enrollment'));
}

