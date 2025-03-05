from flask import Flask, render_template, send_from_directory, request, redirect, flash, url_for
import datetime
import requests
import os
import sys

# Helper function to determine resource path for PyInstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Configure Flask to use the correct paths for templates and static files
app = Flask(__name__, 
            template_folder=resource_path('templates'),
            static_folder=resource_path('static'))

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/') 
def home():
    return render_template('index.html')

@app.route('/about/') 
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/projects/')
def projects():
    return render_template('projects.html')

@app.route('/privacy/')
def privacy():
    return render_template('privacy.html')

@app.route('/terms/')
def terms():
    return render_template('terms.html')

# Cloudflare Turnstile configuration
CF_TURNSTILE_SECRET_KEY = "0x4AAAAAAA_ke_to0umQvFHzyU09Og46uCg"
CF_TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    # Get form data
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    subject = request.form.get('subject', '')
    message = request.form.get('message', '')
    
    # Get Turnstile token
    cf_turnstile_response = request.form.get('cf-turnstile-response', '')
    
    # Verify Turnstile token
    if not cf_turnstile_response:
        return render_template('contact_error.html', error_message="Please complete the security check.")
    
    # Make verification request to Cloudflare
    verification_data = {
        'secret': CF_TURNSTILE_SECRET_KEY,
        'response': cf_turnstile_response,
        'remoteip': request.remote_addr
    }
    
    try:
        response = requests.post(CF_TURNSTILE_VERIFY_URL, data=verification_data)
        result = response.json()
        
        if not result.get('success', False):
            error_codes = result.get('error-codes', [])
            print(f"Turnstile verification failed: {error_codes}")
            return render_template('contact_error.html', error_message="Security check failed. Please try again.")
    except Exception as e:
        print(f"Error verifying Turnstile: {e}")
        return render_template('contact_error.html', error_message="Error verifying security check. Please try again.")
    
    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Format the contact information
    contact_info = f"""\n{'='*50}\nTIMESTAMP: {timestamp}\nNAME: {name}\nEMAIL: {email}\nSUBJECT: {subject}\nMESSAGE:\n{message}\n{'='*50}\n"""
    
    # Save to contact.txt file
    try:
        contact_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contact.txt')
        with open(contact_file_path, 'a') as f:
            f.write(contact_info)
        return render_template('contact_success.html')
    except Exception as e:
        print(f"Error saving contact form: {e}")
        return render_template('contact_error.html', error_message="There was an error saving your message. Please try again later.")

if __name__ == '__main__':
    # For development
    app.run(host='0.0.0.0', port=5000, debug=True)