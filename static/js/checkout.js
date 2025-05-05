// Checkout JavaScript for Ndanu's Little Treats

document.addEventListener('DOMContentLoaded', function() {
    const checkoutForm = document.getElementById('checkout-form');
    const paymentMethodRadios = document.querySelectorAll('input[name="payment_method"]');
    const paymentSections = document.querySelectorAll('.payment-section');
    
    if (paymentMethodRadios.length > 0) {
        // Show/hide payment method specific fields
        paymentMethodRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                const selectedMethod = this.value;
                
                // Hide all payment sections
                paymentSections.forEach(section => {
                    section.style.display = 'none';
                });
                
                // Show selected payment section
                const selectedSection = document.querySelector(`.payment-section[data-method="${selectedMethod}"]`);
                if (selectedSection) {
                    selectedSection.style.display = 'block';
                }
            });
        });
        
        // Trigger change event on page load for the checked radio
        const checkedRadio = document.querySelector('input[name="payment_method"]:checked');
        if (checkedRadio) {
            checkedRadio.dispatchEvent(new Event('change'));
        }
    }
    
    // Form validation
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = this.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    }
    
    // Delivery date validation (must be at least 2 days from today)
    const deliveryDateInput = document.getElementById('delivery_date');
    if (deliveryDateInput) {
        const today = new Date();
        const minDate = new Date(today);
        minDate.setDate(today.getDate() + 2);
        
        const formatDate = date => {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        };
        
        deliveryDateInput.min = formatDate(minDate);
        
        deliveryDateInput.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            if (selectedDate < minDate) {
                alert('Please select a delivery date at least 2 days from today');
                this.value = formatDate(minDate);
            }
        });
    }
});