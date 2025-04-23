@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Basic validation
        if username in users_db:
            return "Username already exists!", 400  # Username already exists
        if password != confirm_password:
            return "Passwords do not match!", 400  # Password mismatch
        
        # Add new user to the in-memory database
        users_db[username] = password
        return redirect(url_for('home'))  # Redirect to home (login page) after registration
    
    return render_template('register.html')  # Render registration page
