from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Enrollment, Payment

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    identity = get_jwt_identity()
    if identity['role'] != 'admin':
        return jsonify({'error': 'Admin only'}), 403
    
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'role': u.role} for u in users])

@admin_bp.route('/payments/pending', methods=['GET'])
@jwt_required()
def pending_payments():
    identity = get_jwt_identity()
    if identity['role'] != 'admin':
        return jsonify({'error': 'Admin only'}), 403
    
    payments = Payment.query.filter_by(status='pending').all()
    return jsonify([{
        'id': p.id,
        'student_id': p.student_id,
        'course_id': p.course_id,
        'amount': p.amount
    } for p in payments])

@admin_bp.route('/enrollments/pending', methods=['GET'])
@jwt_required()
def pending_enrollments():
    identity = get_jwt_identity()
    if identity['role'] != 'admin':
        return jsonify({'error': 'Admin only'}), 403
    
    enrolls = Enrollment.query.filter_by(status='pending').all()
    return jsonify([{'id': e.id, 'student_id': e.student_id, 'course_id': e.course_id} for e in enrolls])

