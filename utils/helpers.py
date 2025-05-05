import os
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename
import uuid

def save_image(file, folder):
    """Save an image file and return the filename"""
    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
    filepath = os.path.join(current_app.root_path, 'static/uploads', folder, filename)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save and optimize image
    image = Image.open(file)
    image.thumbnail((800, 800))
    image.save(filepath, optimize=True, quality=85)
    
    return filename

def format_currency(amount):
    """Format currency with KES symbol"""
    return f"KES {amount:,.2f}"

def generate_order_reference():
    """Generate unique order reference"""
    return f"ORD-{uuid.uuid4().hex[:8].upper()}"

def calculate_order_total(cart_items):
    """Calculate total amount for cart items"""
    return sum(item.product.price * item.quantity for item in cart_items)

def send_email(to_email, subject, template, **kwargs):
    """Send email using Flask-Mail"""
    from flask_mail import Message
    from flask import render_template
    from app import mail
    
    msg = Message(
        subject,
        recipients=[to_email],
        html=render_template(template, **kwargs),
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)