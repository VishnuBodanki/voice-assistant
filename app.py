from flask import Flask, render_template, request, redirect, url_for
import threading
import webbrowser
import database
import assistant
app = Flask(__name__)

# Initialize DB and add default user
database.init_db()
database.add_user("vishnu", "Vishnu@123", "Vishnu Bodanki")

# ---------------- Routes ---------------- #

@app.route('/')
def login_page():
    return render_template('voice-assistant.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = database.check_user(username, password)

    if user:
        # Start voice assistant in a background thread
        threading.Thread(target=assistant.run_assistant, daemon=True).start()
        return redirect(url_for('dashboard', name=user[3]))
    else:
        return render_template('voice-assistant.html', login_error="Invalid credentials!")

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']

    try:
        database.add_user(username, password, name)
        success = "User registered successfully! You can login now."
        return render_template('voice-assistant.html', signup_success=success)
    except Exception as e:
        error = "Username already exists! Try a different one."
        return render_template('voice-assistant.html', signup_error=error)

@app.route('/dashboard/<name>')
def dashboard(name):
    html = f"""
    <h2>Welcome {name}! Voice Assistant is running in the background.</h2>
    <p>Say 'close assistant' to stop it or 'open assistant' to start it again.</p>
    """
    return html

# ---------------- Auto-open browser ---------------- #
if __name__ == "__main__":
    # Open browser after 1.5 seconds
    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=True)
