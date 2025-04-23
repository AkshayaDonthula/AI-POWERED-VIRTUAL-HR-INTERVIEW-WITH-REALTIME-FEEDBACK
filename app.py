from flask import Flask, render_template, Response, request,redirect,url_for, jsonify
import cv2
import speech_recognition as sr
from pydub import AudioSegment
import os
import random
import nltk

nltk.download('punkt')

app = Flask(__name__)

# Homepage route
@app.route('/')
def home():
    return render_template('login.html')  # Display the login page

# Dummy in-memory database for user data
users_db = {}

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
        return redirect(url_for('index'))  # Redirect to the resume page after successful login
    else:
        return "Invalid credentials!", 401  # Return an error if login fails


# Set the correct FFmpeg path (make sure this is where you installed FFmpeg)
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"  # Replace with your actual path
AudioSegment.ffmpeg = r"C:\ffmpeg\bin\ffmpeg.exe"     # Replace with your actual path
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"   # Replace with your actual path


# Predefined interview questions
QUESTIONS = [
    "Tell me about yourself.",
    "What are your strengths and weaknesses?",
    "Why should we hire you?",
    "Describe a challenge you've faced and how you overcame it.",
    "Where do you see yourself in five years?"
]

# Function to capture video frames
def generate_frames():
    camera = cv2.VideoCapture(0)  # Open webcam

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/interview', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/get_question', methods=['GET'])
def get_question():
    """Returns a random interview question."""
    question = random.choice(QUESTIONS)
    return jsonify({"question": question})

@app.route('/process_audio', methods=['POST'])
def process_audio():
    """Processes the user's audio response and provides feedback."""
    audio_file = request.files['audio']
    input_audio_path = "temp_audio.webm"
    output_audio_path = "converted_audio.wav"

    # Save the uploaded file
    audio_file.save(input_audio_path)

    # Convert to WAV using pydub
    try:
        audio = AudioSegment.from_file(input_audio_path)
        audio.export(output_audio_path, format="wav")

        # Use SpeechRecognition to analyze the response
        recognizer = sr.Recognizer()
        with sr.AudioFile(output_audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            feedback = analyze_response(text)

        os.remove(input_audio_path)
        os.remove(output_audio_path)

    except Exception as e:
        feedback = f"Error processing audio: {str(e)}"

    return jsonify({"feedback": feedback})

def analyze_response(text):
    """Analyzes the response and provides feedback based on keywords."""
    keywords = ["teamwork", "leadership", "problem-solving", "communication"]
    words = nltk.word_tokenize(text.lower())
    score = sum(1 for word in words if word in keywords)

    if score >= 3:
        return "Great response! You demonstrated strong skills."
    elif score == 2:
        return "Good response, but try to elaborate more on your strengths."
    else:
        return "Your response lacks key points. Try to include relevant skills."

if __name__ == "__main__":
    app.run(debug=True)
