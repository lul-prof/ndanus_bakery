// Cart JavaScript for Ndanu's Little Treats

document.addEventListener('DOMContentLoaded', function() {
    // Quantity update
    const quantityInputs = document.querySelectorAll('.quantity-input');
    
    if (quantityInputs.length > 0) {
        quantityInputs.forEach(input => {
            input.addEventListener('change', function() {
                const form = this.closest('form');
                form.submit();
            });
        });
    }
    
    // Quantity increment/decrement buttons
    const decrementBtns = document.querySelectorAll('.quantity-decrement');
    const incrementBtns = document.querySelectorAll('.quantity-increment');
    
    decrementBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.nextElementSibling;
            let value = parseInt(input.value);
            if (value > 1) {
                input.value = value - 1;
                input.dispatchEvent(new Event('change'));
            }
        });
    });
    
    incrementBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.previousElementSibling;
            let value = parseInt(input.value);
            input.value = value + 1;
            input.dispatchEvent(new Event('change'));
        });
    });
    
    // Remove item confirmation
    const removeButtons = document.querySelectorAll('.remove-item');
    
    removeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to remove this item from your cart?')) {
                e.preventDefault();
            }
        });
    });
    
    // Cart total calculation
    function updateCartTotal() {
        const cartItems = document.querySelectorAll('.cart-item');
        let total = 0;
        
        cartItems.forEach(item => {
            const price = parseFloat(item.querySelector('.item-price').getAttribute('data-price'));
            const quantity = parseInt(item.querySelector('.quantity-input').value);
            total += price * quantity;
        });
        
        const totalElement = document.querySelector('.cart-total-amount');
        if (totalElement) {
            totalElement.textContent = total.toFixed(2);
        }
    }
    
    // Update total when quantity changes
    quantityInputs.forEach(input => {
        input.addEventListener('change', updateCartTotal);
    });
});