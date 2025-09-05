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

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor("#0F2437"))
    c.drawCentredString(width/2, height - 50, "XYZ University / Admission Office")

    c.setStrokeColor(colors.HexColor("#0F2437"))
    c.setLineWidth(2)
    c.line(50, height - 60, width - 50, height - 60)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height - 100, "Admission Letter")

    # Student Details
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

    # Footer - Stamp Style
    stamp_center_x = 350
    stamp_center_y = 100
    stamp_radius = 50

    # Draw circle for stamp
    c.setLineWidth(2)
    c.setStrokeColor(colors.red)
    c.circle(stamp_center_x, stamp_center_y, stamp_radius, stroke=1, fill=0)

    # Draw text inside stamp
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.red)
    c.drawCentredString(stamp_center_x, stamp_center_y + 10, "Authorized")
    c.drawCentredString(stamp_center_x, stamp_center_y - 5, "Signature")
    c.drawCentredString(stamp_center_x, stamp_center_y - 20, "Rishabh")
    c.drawCentredString(stamp_center_x, stamp_center_y - 35, datetime.now().strftime("%d-%m-%Y"))

    c.save()

    application.pdf_path = filename
    return filename