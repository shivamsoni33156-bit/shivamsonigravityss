from flask import Blueprint, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Enrollment, Course, Material

student_bp = Blueprint('student', __name__)

@student_bp.route('/courses', methods=['GET'])
@jwt_required()
def enrolled_courses():
    identity = get_jwt_identity()
    if identity['role'] != 'student':
        return jsonify({'error': 'Students only'}), 403
    
    enrollments = Enrollment.query.filter_by(student_id=identity['id'], status='approved').all()
    courses = []
    for e in enrollments:
        course = Course.query.get(e.course_id)
        courses.append({'id': course.id, 'title': course.title})
    return jsonify(courses)

@student_bp.route('/materials/<int:course_id>', methods=['GET'])
@jwt_required()
def get_materials(course_id):
    identity = get_jwt_identity()
    enrollment = Enrollment.query.filter_by(student_id=identity['id'], course_id=course_id, status='approved').first()
    if not enrollment:
        return jsonify({'error': 'Not enrolled'}), 403
    
    materials = Material.query.filter_by(course_id=course_id).all()
    return jsonify([{'id': m.id, 'title': m.title, 'type': m.file_type} for m in materials])

@student_bp.route('/material/<int:course_id>/<filename>')
def serve_student_material(course_id, filename):
    # Check enrollment here in prod
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

