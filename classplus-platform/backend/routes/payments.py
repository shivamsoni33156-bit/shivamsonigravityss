from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Payment, Enrollment, Course
from werkzeug.utils import secure_filename
import os
import uuid

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_payment():
    identity = get_jwt_identity()
    if identity['role'] != 'student':
        return jsonify({'error': 'Students only'}), 403
    
    data = request.form
    course_id = int(data['course_id'])
    amount = float(data['amount'])
    
    course = Course.query.get_or_404(course_id)
    
    proof_file = request.files.get('proof')
    proof_path = None
    if proof_file and proof_file.filename:
        filename = secure_filename(proof_file.filename)
        unique_filename = f"proof_{uuid.uuid4()}_{filename}"
        upload_path = os.path.join('uploads', 'proofs', unique_filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        proof_file.save(upload_path)
        proof_path = unique_filename
    
    payment = Payment(
        student_id=identity['id'],
        course_id=course_id,
        amount=amount,
        proof_path=proof_path
    )
    enrollment = Enrollment(
        student_id=identity['id'],
        course_id=course_id,
        status='pending'
    )
    db.session.add(payment)
    db.session.add(enrollment)
    db.session.commit()
    
    return jsonify({'message': 'Payment submitted for approval', 'upi': '7229985050', 'bank': 'SBI 30392342115 Zakir Husain'}), 201

@payments_bp.route('/history', methods=['GET'])
@jwt_required()
def payment_history():
    identity = get_jwt_identity()
    payments = Payment.query.filter_by(student_id=identity['id']).all()
    return jsonify([{
        'id': p.id,
        'course_id': p.course_id,
        'amount': p.amount,
        'status': p.status
    } for p in payments])

