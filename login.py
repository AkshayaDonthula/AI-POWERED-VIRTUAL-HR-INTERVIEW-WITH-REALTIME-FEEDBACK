from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Dummy in-memory database for user data
users_db = {}

# Homepage route
@app.route('/')
def home():
    return render_template('login.html')  # Display the login page

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if user exists or passwords don't match
        if username in users_db:
            return "Username already exists!", 400
        if password != confirm_password:
            return "Passwords do not match!", 400
        
        # Save user data in the in-memory database
        users_db[username] = password
        return redirect(url_for('home'))  # Redirect to login page after registration

    return render_template('register.html')  # Display the registration page

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Validate credentials
    if username in users_db and users_db[username] == password:
        return redirect(url_for('resume'))  # Redirect to the resume page after successful login
    else:
        return "Invalid credentials!", 401  # Return an error if login fails

# Resume route (after successful login)
@app.route('/resume')
def resume():
    return render_template('resume.html')  # Display the resume page

if __name__ == '__main__':
    app.run(debug=True)
