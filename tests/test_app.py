import os
import pytest
from io import BytesIO
from extensions import db
from app import create_app
from models import Application

@pytest.fixture
def client():
    # Create a test Flask app
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        # Clean up
        with app.app_context():
            db.drop_all()


def test_application_submission(client):
    """Test student can submit an application"""
    data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '1234567890',
        'address': '123 Street',
        'academic_details': 'BSc Computer Science',
        'id_proof': (BytesIO(b'my id proof'), 'id.pdf'),
        'degree_certificate': (BytesIO(b'my degree'), 'degree.pdf')
    }
    response = client.post('/apply', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b'Application ID' in response.data

    # Check DB entry
    app_entry = Application.query.filter_by(email='john@example.com').first()
    assert app_entry is not None
    assert app_entry.status == 'Pending'


def test_track_application_by_id(client):
    """Test tracking application by ID"""
    # Create a test application
    app_entry = Application(name='Jane', email='jane@example.com', phone='9876543210')
    db.session.add(app_entry)
    db.session.commit()

    response = client.post('/track', data={'identifier': str(app_entry.id)}, follow_redirects=True)
    assert b'Application ID' in response.data
    assert bytes(app_entry.name, 'utf-8') in response.data


def test_track_application_by_email(client):
    """Test tracking application by email"""
    app_entry = Application(name='Alice', email='alice@example.com', phone='1112223333')
    db.session.add(app_entry)
    db.session.commit()

    response = client.post('/track', data={'identifier': 'alice@example.com'}, follow_redirects=True)
    assert b'Application ID' in response.data
    assert b'Alice' in response.data


def test_download_pdf_for_approved_application(client):
    """Test PDF download works for approved applications"""
    app_entry = Application(name='Bob', email='bob@example.com', status='Approved', pdf_path='tests/test.pdf')
    db.session.add(app_entry)
    db.session.commit()

    # Create dummy PDF file
    os.makedirs('tests', exist_ok=True)
    with open('tests/test.pdf', 'wb') as f:
        f.write(b'%PDF-1.4 test pdf content')

    response = client.get(f'/student/download/{app_entry.id}')
    assert response.status_code == 200
    assert response.data.startswith(b'%PDF')

    os.remove('tests/test.pdf')
