import click
from flask.cli import with_appcontext
from app import db
from models.user import User
from models.product import Product
from werkzeug.security import generate_password_hash
import random
import string

def register_commands(app):
    """Register custom Flask CLI commands."""
    app.cli.add_command(create_admin)
    app.cli.add_command(list_users)
    app.cli.add_command(reset_password)
    app.cli.add_command(product_commands)

@click.command('create-admin')
@click.option('--username', prompt=True, help='Admin username')
@click.option('--email', prompt=True, help='Admin email')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Admin password')
@with_appcontext
def create_admin(username, email, password):
    """Create a new admin user."""
    try:
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=True
        )
        db.session.add(user)
        db.session.commit()
        click.echo(f"Admin user {username} created successfully!")
    except Exception as e:
        db.session.rollback()
        click.echo(f"Error creating admin user: {str(e)}")

@click.command('list-users')
@click.option('--admin-only', is_flag=True, help='List only admin users')
@with_appcontext
def list_users(admin_only):
    """List all users or admin users only."""
    try:
        if admin_only:
            users = User.query.filter_by(is_admin=True).all()
            click.echo("Admin Users:")
        else:
            users = User.query.all()
            click.echo("All Users:")
            
        for user in users:
            click.echo(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Admin: {user.is_admin}")
            
        click.echo(f"Total: {len(users)} users")
    except Exception as e:
        click.echo(f"Error listing users: {str(e)}")

@click.command('reset-password')
@click.option('--username', prompt=True, help='Username to reset password for')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='New password')
@with_appcontext
def reset_password(username, password):
    """Reset a user's password."""
    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            click.echo(f"User {username} not found.")
            return
            
        user.password_hash = generate_password_hash(password)
        db.session.commit()
        click.echo(f"Password for {username} has been reset successfully.")
    except Exception as e:
        db.session.rollback()
        click.echo(f"Error resetting password: {str(e)}")

@click.group('product')
def product_commands():
    """Product management commands."""
    pass

@product_commands.command('list')
@with_appcontext
def list_products():
    """List all products."""
    try:
        products = Product.query.all()
        click.echo("Products:")
        for product in products:
            click.echo(f"ID: {product.id}, Name: {product.name}, Price: {product.price}, Stock: {product.stock}")
        click.echo(f"Total: {len(products)} products")
    except Exception as e:
        click.echo(f"Error listing products: {str(e)}")

@product_commands.command('create')
@click.option('--name', prompt=True, help='Product name')
@click.option('--description', prompt=True, help='Product description')
@click.option('--price', prompt=True, type=float, help='Product price')
@click.option('--stock', prompt=True, type=int, help='Product stock')
@click.option('--category', prompt=True, help='Product category')
@with_appcontext
def create_product(name, description, price, stock, category):
    """Create a new product."""
    try:
        # Generate a random image name since we can't upload via CLI
        image_name = f"product_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}.jpg"
        
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            image_url=image_name
        )
        db.session.add(product)
        db.session.commit()
        click.echo(f"Product {name} created successfully!")
    except Exception as e:
        db.session.rollback()
        click.echo(f"Error creating product: {str(e)}")