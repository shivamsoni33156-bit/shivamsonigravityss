from flask import Flask
from flask_cors import CORS
from .config import Config
from ..models import db
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)
jwt = JWTManager(app)

from .auth import auth_bp
from .routes.teacher import teacher_bp
from .routes.student import student_bp
from .routes.payments import payments_bp
from .routes.admin import admin_bp

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(teacher_bp, url_prefix='/api/teacher')
app.register_blueprint(student_bp, url_prefix='/api/student')
app.register_blueprint(payments_bp, url_prefix='/api/payments')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

@app.route('/')
def home():
    return {'message': 'Classplus Platform API - Run /api/register or /api/login'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

