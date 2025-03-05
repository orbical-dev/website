document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('.contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            // Get form fields
            const nameField = document.getElementById('name');
            const emailField = document.getElementById('email');
            const messageField = document.getElementById('message');
            
            // Basic validation
            let isValid = true;
            
            // Name validation
            if (!nameField.value.trim()) {
                isValid = false;
                highlightField(nameField, 'Please enter your name');
            } else {
                resetField(nameField);
            }
            
            // Email validation
            if (!emailField.value.trim()) {
                isValid = false;
                highlightField(emailField, 'Please enter your email');
            } else if (!isValidEmail(emailField.value.trim())) {
                isValid = false;
                highlightField(emailField, 'Please enter a valid email address');
            } else {
                resetField(emailField);
            }
            
            // Message validation
            if (!messageField.value.trim()) {
                isValid = false;
                highlightField(messageField, 'Please enter your message');
            } else {
                resetField(messageField);
            }
            
            // Check Turnstile
            const turnstileResponse = document.querySelector('[name="cf-turnstile-response"]');
            if (!turnstileResponse || !turnstileResponse.value) {
                isValid = false;
                // Create a message below the Turnstile widget
                const turnstileContainer = document.querySelector('.cf-turnstile');
                if (turnstileContainer) {
                    const errorContainer = document.createElement('div');
                    errorContainer.className = 'turnstile-error';
                    errorContainer.style.color = '#e74c3c';
                    errorContainer.style.fontSize = '0.85rem';
                    errorContainer.style.marginTop = '0.25rem';
                    errorContainer.style.textAlign = 'center';
                    errorContainer.textContent = 'Please complete the security check';
                    
                    // Remove any existing error message
                    const existingError = turnstileContainer.parentNode.querySelector('.turnstile-error');
                    if (existingError) {
                        existingError.remove();
                    }
                    
                    turnstileContainer.parentNode.appendChild(errorContainer);
                }
            } else {
                // Remove any existing error message
                const turnstileContainer = document.querySelector('.cf-turnstile');
                if (turnstileContainer) {
                    const existingError = turnstileContainer.parentNode.querySelector('.turnstile-error');
                    if (existingError) {
                        existingError.remove();
                    }
                }
            }
            
            // If form is not valid, prevent submission
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    // Helper functions
    function highlightField(field, message) {
        field.style.borderColor = '#e74c3c';
        
        // Create or update error message
        let errorMsg = field.parentNode.querySelector('.error-message');
        if (!errorMsg) {
            errorMsg = document.createElement('div');
            errorMsg.className = 'error-message';
            errorMsg.style.color = '#e74c3c';
            errorMsg.style.fontSize = '0.85rem';
            errorMsg.style.marginTop = '0.25rem';
            field.parentNode.appendChild(errorMsg);
        }
        errorMsg.textContent = message;
    }
    
    function resetField(field) {
        field.style.borderColor = '';
        const errorMsg = field.parentNode.querySelector('.error-message');
        if (errorMsg) {
            errorMsg.remove();
        }
    }
    
    function isValidEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }
});
