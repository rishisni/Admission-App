import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from config import Config
from werkzeug.utils import secure_filename
from datetime import datetime

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_file(file):
    original_filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{original_filename}"
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(file_path)
    return filename

def generate_admission_pdf(application):
    
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    filename = f'admission_{application.id}.pdf'
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor("#0F2437"))
    c.drawCentredString(width/2, height - 50, "XYZ University / Admission Office")

    c.setStrokeColor(colors.HexColor("#0F2437"))
    c.setLineWidth(2)
    c.line(50, height - 60, width - 50, height - 60)

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height - 100, "Admission Letter")

    c.setFont("Helvetica", 12)
    y = height - 140
    line_height = 20

    details = [
        ("Application ID", application.id),
        ("Name", application.name),
        ("Email", application.email),
        ("Phone", application.phone),
        ("Address", application.address),
        ("Academic Details", application.academic_details),
        ("Status", application.status),
        ("Date of Issue", datetime.now().strftime("%d-%m-%Y"))
    ]

    for label, value in details:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(80, y, f"{label}:")
        c.setFont("Helvetica", 12)
        c.drawString(200, y, str(value))
        y -= line_height

    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, 100, "Authorized Signature:")
    c.line(200, 98, 400, 98)  

    c.save()

    application.pdf_path = filename
    return filename
