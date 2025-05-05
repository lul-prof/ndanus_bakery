// Admin JavaScript for Ndanu's Little Treats

document.addEventListener('DOMContentLoaded', function() {
    // Product form image preview
    const imageInput = document.getElementById('image');
    const imagePreview = document.getElementById('image-preview');
    
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                };
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
    
    // Rich text editor for product description
    const descriptionTextarea = document.getElementById('description');
    if (descriptionTextarea) {
        // Simple rich text controls
        const editorControls = document.createElement('div');
        editorControls.className = 'editor-controls';
        editorControls.innerHTML = `
            <button type="button" data-command="bold" title="Bold"><i class="fas fa-bold"></i></button>
            <button type="button" data-command="italic" title="Italic"><i class="fas fa-italic"></i></button>
            <button type="button" data-command="underline" title="Underline"><i class="fas fa-underline"></i></button>
            <button type="button" data-command="insertUnorderedList" title="Bullet List"><i class="fas fa-list-ul"></i></button>
        `;
        
        descriptionTextarea.parentNode.insertBefore(editorControls, descriptionTextarea);
        
        // Add event listeners to buttons
        const buttons = editorControls.querySelectorAll('button');
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                const command = this.getAttribute('data-command');
                document.execCommand(command, false, null);
                descriptionTextarea.focus();
            });
        });
    }
    
    // Delete confirmation
    const deleteButtons = document.querySelectorAll('.delete-btn');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Dashboard charts (using Chart.js)
    const salesChart = document.getElementById('sales-chart');
    if (salesChart && window.Chart) {
        const ctx = salesChart.getContext('2d');
        
        // Sample data - replace with actual data from your backend
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                datasets: [{
                    label: 'Sales',
                    data: [12, 19, 3, 5, 2, 3, 7],
                    backgroundColor: 'rgba(248, 180, 0, 0.2)',
                    borderColor: 'rgba(248, 180, 0, 1)',
                    borderWidth: 2,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Date range picker for reports
    const dateFrom = document.getElementById('date_from');
    const dateTo = document.getElementById('date_to');
    
    if (dateFrom && dateTo) {
        dateFrom.addEventListener('change', function() {
            dateTo.min = this.value;
        });
        
        dateTo.addEventListener('change', function() {
            dateFrom.max = this.value;
        });
    }
});