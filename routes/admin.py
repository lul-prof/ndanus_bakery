from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.product import Product
from models.order import Order
from models.blog import BlogPost
from utils.helpers import save_image
from app import db
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('public.home'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get counts for dashboard stats
    total_orders = Order.query.count()
    total_products = Product.query.count()
    
    # Get total revenue (assuming you have a total_amount field in Order)
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    # Get total customers
    total_customers = db.session.query(db.func.count(db.distinct(Order.user_id))).scalar() or 0
    
    # Create stats object
    stats = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'total_customers': total_customers
    }
    
    # Get recent orders and low stock products
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    low_stock_products = Product.query.filter(Product.stock < 10).all()
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_orders=recent_orders,
                         low_stock_products=low_stock_products)

@admin.route('/products')
@login_required
@admin_required
def products():
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        image = request.files.get('image')
        image_filename = save_image(image, 'products') if image else None
        
        product = Product(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            category=request.form.get('category'),
            stock=int(request.form.get('stock')),
            image_url=image_filename
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/product_form.html')

@admin.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        image = request.files.get('image')
        if image:
            product.image_url = save_image(image, 'products')
        
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.category = request.form.get('category')
        product.stock = int(request.form.get('stock'))
        product.is_available = bool(request.form.get('is_available'))
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/product_form.html', product=product)

@admin.route('/orders')
@login_required
@admin_required
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@admin.route('/orders/<int:id>')
@login_required
@admin_required
def order_detail(id):
    order = Order.query.get_or_404(id)
    return render_template('admin/order_detail.html', order=order)

@admin.route('/orders/update-status/<int:id>', methods=['POST'])
@login_required
@admin_required
def update_order_status(id):
    order = Order.query.get_or_404(id)
    order.status = request.form.get('status')
    db.session.commit()
    flash('Order status updated successfully!', 'success')
    return redirect(url_for('admin.order_detail', id=id))

@admin.route('/blog')
@login_required
@admin_required
def blog_posts():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blog_posts.html', posts=posts)

@admin.route('/blog/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_blog_post():
    if request.method == 'POST':
        image = request.files.get('image')
        image_filename = save_image(image, 'blog') if image else None
        
        post = BlogPost(
            title=request.form.get('title'),
            content=request.form.get('content'),
            image_url=image_filename,
            author_id=current_user.id,
            is_published=bool(request.form.get('is_published'))
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('admin.blog_posts'))
    
    return render_template('admin/blog_form.html')

@admin.route('/blog/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_blog_post(id):
    post = BlogPost.query.get_or_404(id)
    
    if request.method == 'POST':
        image = request.files.get('image')
        if image:
            post.image_url = save_image(image, 'blog')
        
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.is_published = bool(request.form.get('is_published'))
        
        db.session.commit()
        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('admin.blog_posts'))
    
    return render_template('admin/blog_form.html', post=post)

# ... existing code ...

@admin.route('/reports')
@login_required
@admin_required
def reports():
    """Admin reports page"""
    # Get some basic statistics for the reports
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    # Get sales by category
    product_categories = db.session.query(Product.category, db.func.count(Product.id)).group_by(Product.category).all()
    
    # Get recent orders for the report
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # Get top selling products
    top_products = Product.query.order_by(Product.sales_count.desc()).limit(5).all()
    
    return render_template('admin/reports.html', 
                          total_orders=total_orders,
                          total_revenue=total_revenue,
                          product_categories=product_categories,
                          recent_orders=recent_orders,
                          top_products=top_products)


@admin.route('/products/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin.products'))
                    