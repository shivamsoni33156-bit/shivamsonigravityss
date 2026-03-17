from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Course, Enrollment, Material, Payment
import os
from werkzeug.utils import secure_filename
import uuid

teacher_bp = Blueprint('teacher', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'mp4', 'jpg', 'jpeg', 'png', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@teacher_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    identity = get_jwt_identity()
    if identity['role'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    teacher_id = identity['id']
    total_courses = Course.query.filter_by(teacher_id=teacher_id).count()
    total_students = db.session.query(Enrollment.student_id.distinct()).join(Course).filter(Course.teacher_id == teacher_id).count()
    earnings = db.session.query(db.func.sum(Payment.amount)).join(Enrollment).join(Course).filter(Course.teacher_id == teacher_id, Payment.status == 'approved').scalar() or 0
    
    return jsonify({
        'total_students': total_students,
        'total_courses': total_courses,
        'earnings': earnings
    })

@teacher_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    identity = get_jwt_identity()
    if identity['role'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.json
    course = Course(
        title=data['title'],
        description=data.get('description'),
        price=data.get('price', 0.0),
        teacher_id=identity['id']
    )
    db.session.add(course)
    db.session.commit()
    return jsonify({'message': 'Course created', 'course_id': course.id}), 201

@teacher_bp.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    identity = get_jwt_identity()
    if identity['role'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    courses = Course.query.filter_by(teacher_id=identity['id']).all()
    return jsonify([{'id': c.id, 'title': c.title, 'price': c.price} for c in courses])

@teacher_bp.route('/materials/<int:course_id>', methods=['POST'])
@jwt_required()
def upload_material(course_id):
    identity = get_jwt_identity()
    if identity['role'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    course = Course.query.get_or_404(course_id)
    if course.teacher_id != identity['id']:
        return jsonify({'error': 'Not your course'}), 403
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)
        
        material = Material(
            course_id=course_id,
            title=request.form.get('title', filename),
            file_path=unique_filename,
            file_type=filename.rsplit('.', 1)[1].lower()
        )
        db.session.add(material)
        db.session.commit()
        return jsonify({'message': 'Uploaded', 'material_id': material.id})
    
    return jsonify({'error': 'Invalid file type'}), 400

@teacher_bp.route('/materials/<int:course_id>/<filename>')
@jwt_required()
def serve_material(course_id, filename):
    # Auth check omitted for simplicity, add later
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

