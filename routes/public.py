from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.product import Product
from models.blog import BlogPost
from utils.helpers import send_email
from app import db

public = Blueprint('public', __name__)

@public.route('/')
def home():
    featured_products = Product.query.filter_by(is_available=True).limit(6).all()
    return render_template('public/home.html', products=featured_products)

@public.route('/products')
def products():
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category, is_available=True).all()
    else:
        products = Product.query.filter_by(is_available=True).all()
    return render_template('public/products.html', products=products)

@public.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    related_products = Product.query.filter_by(
        category=product.category, 
        is_available=True
    ).filter(Product.id != id).limit(4).all()
    return render_template('public/product_detail.html', product=product, related_products=related_products)

@public.route('/about')
def about():
    return render_template('public/about.html')

@public.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        send_email(
            'info@ndanustreats.com',
            'New Contact Form Submission',
            'email/contact.html',
            name=name,
            email=email,
            message=message
        )
        
        flash('Thank you for your message. We will get back to you soon!', 'success')
        return redirect(url_for('public.contact'))
        
    return render_template('public/contact.html')

@public.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.filter_by(is_published=True).order_by(
        BlogPost.created_at.desc()
    ).paginate(page=page, per_page=6)
    return render_template('public/blog.html', posts=posts)

@public.route('/blog/<int:id>')
def blog_post(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('public/blog_post.html', post=post)

@public.route('/gallery')
def gallery():
    return render_template('public/gallery.html')

@public.route('/newsletter-signup', methods=['POST'])
def newsletter_signup():
    email = request.form.get('email')
    if email:
        # Add email to newsletter list (implement your newsletter service integration)
        flash('Thank you for subscribing to our newsletter!', 'success')
    return redirect(request.referrer or url_for('public.home'))
'''
@public.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    related_products = Product.query.filter_by(
        category=product.category, 
        is_available=True
    ).filter(Product.id != id).limit(4).all()
    return render_template('public/product_detail.html', product=product, related_products=related_products)
    '''