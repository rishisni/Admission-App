from flask import Blueprint, render_template, redirect, url_for, request, flash,send_file,abort
from forms import ApplicationForm
from app import db
from models import Application
from utils import save_file
from config import Config

import os
student_bp = Blueprint('student', __name__)

@student_bp.route('/apply', methods=['GET', 'POST'])
def apply():
    form = ApplicationForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_app = Application.query.filter_by(email=form.email.data).first()
        if existing_app:
            flash("An application with this email already exists. You can track it using your Application ID.", "warning")
            return redirect(url_for('student.track'))

        # Save files
        id_proof_path = save_file(form.id_proof.data)
        degree_path = save_file(form.degree_certificate.data)

        # Create application
        application = Application(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            academic_details=form.academic_details.data,
            id_proof=id_proof_path,
            degree_certificate=degree_path
        )
        db.session.add(application)
        db.session.commit()

        
        return render_template('application_submitted.html', app_id=application.id)

    return render_template('application_form.html', form=form)


@student_bp.route('/student/download/<int:app_id>')
def download_pdf(app_id):
    application = Application.query.get_or_404(app_id)
    
    if application.status != 'Approved' or not application.pdf_path:
        abort(403, description="PDF not available or application not approved yet")
    
    file_path = os.path.join(Config.UPLOAD_FOLDER, application.pdf_path)

    if not os.path.exists(file_path):
        abort(404, description="PDF file not found")
    
    return send_file(file_path, as_attachment=True)

@student_bp.route('/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        identifier = request.form.get('identifier')

        
        if identifier.isdigit():
            application = Application.query.filter_by(id=int(identifier)).first()
        else:
            application = Application.query.filter_by(email=identifier).first()

        if not application:
            flash("Application not found. Please check your details.", "danger")
            return redirect(url_for('student.track'))

        return render_template('track_status.html', application=application)

    return render_template('track_form.html')
