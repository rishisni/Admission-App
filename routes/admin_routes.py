from flask import Blueprint, render_template, redirect, url_for
from app import db
from models import Application
from utils import generate_admission_pdf

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def dashboard():
    applications = Application.query.all()
    return render_template('admin_dashboard.html', applications=applications)

@admin_bp.route('/admin/approve/<int:app_id>')
def approve(app_id):
    app = Application.query.get_or_404(app_id)
    app.status = 'Approved'
    db.session.commit()
    generate_admission_pdf(app)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/reject/<int:app_id>')
def reject(app_id):
    app = Application.query.get_or_404(app_id)
    app.status = 'Rejected'
    db.session.commit()
    return redirect(url_for('admin.dashboard'))
