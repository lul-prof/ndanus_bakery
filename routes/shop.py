from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_required
from models.product import Product
from models.order import Order, OrderItem
from utils.helpers import generate_order_reference, calculate_order_total
from utils.payment import MPESAPayment, PayPalPayment
from app import db

shop = Blueprint('shop', __name__)

@shop.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    products = []
    total = 0
    delivery_fee = 200
    if cart_items:
        for product_id, quantity in cart_items.items():
            product = Product.query.get(int(product_id))
            if product:
                products.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': product.price * quantity
                })
                total += product.price * quantity
    return render_template('shop/cart.html', cart_items=products, total=total,delivery_fee=delivery_fee)

@shop.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    
    product = Product.query.get_or_404(product_id)
    if product.stock < quantity:
        flash('Sorry, not enough stock available.', 'danger')
        return redirect(request.referrer)
    
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
    
    session['cart'] = cart
    flash('Product added to cart!', 'success')
    return redirect(request.referrer)

@shop.route('/cart/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form.get('quantity'))
    cart = session.get('cart', {})
    
    if quantity <= 0:
        cart.pop(str(product_id), None)
    else:
        product = Product.query.get_or_404(product_id)
        if product.stock < quantity:
            flash('Sorry, not enough stock available.', 'danger')
            return redirect(url_for('shop.cart'))
        cart[str(product_id)] = quantity
    
    session['cart'] = cart
    return redirect(url_for('shop.cart'))

@shop.route('/cart/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    return redirect(url_for('shop.cart'))

@shop.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty. Please add some products first.', 'warning')
        return redirect(url_for('shop.cart'))

    products = []
    subtotal = 0
    # Calculate delivery fee
    delivery_fee = 200  
    total = subtotal + delivery_fee
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        
        # Create order
        order = Order(
            user_id=current_user.id,
            reference=generate_order_reference(),
            total_amount=calculate_order_total(cart_items),
            payment_method=payment_method,
            shipping_address=request.form.get('shipping_address')
        )
        
        # Add order items
        for product_id, quantity in cart_items.items():
            product = Product.query.get(int(product_id))
            if product:
                order_item = OrderItem(
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price
                )
                order.items.append(order_item)
                product.stock -= quantity
     
     
        for product_id, quantity in cart.items():
            product = Product.query.get(product_id)
            if product:
                item_total = product.price * quantity
                subtotal += item_total
                products.append({
                    'product': product,
                    'quantity': quantity,
                    'total': item_total
                })
        total = subtotal + delivery_fee


        
        db.session.add(order)
        db.session.commit()
        
        # Process payment
        if payment_method == 'mpesa':
            mpesa = MPESAPayment()
            result = mpesa.initiate_payment(
                current_user.phone,
                order.total_amount,
                order.reference
            )
            if result.get('ResponseCode') == '0':
                session.pop('cart', None)
                flash('Order placed successfully! Please complete the payment on your phone.', 'success')
                return redirect(url_for('auth.orders'))
        elif payment_method == 'paypal':
            paypal = PayPalPayment()
            result = paypal.create_order(order.items, order.total_amount)
            if result.get('id'):
                return redirect(result['links'][1]['href'])  # Redirect to PayPal checkout
        
        flash('Payment processing failed. Please try again.', 'danger')
        return redirect(url_for('shop.checkout'))
    
    return render_template('shop/checkout.html', 
                          cart_items=products, 
                          subtotal=subtotal,
                          delivery_fee=delivery_fee,
                          total=total)