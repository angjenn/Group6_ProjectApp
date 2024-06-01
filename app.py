
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('workout_model.h5')

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            gender TEXT
        )
    ''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            duration INTEGER,
            type TEXT,
            intensity TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/workout', methods=['POST'])
def workout():
    age = request.form['age']
    gender = request.form['gender']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (age, gender) VALUES (?, ?)", (age, gender))
    conn.commit()
    conn.close()
    return render_template('workout_plan.html')

@app.route('/generate', methods=['POST'])
def generate():
    duration = request.form['duration']
    workout_type = request.form['workout_type']
    intensity = request.form['intensity']

    # Convert form input to numeric values for the model
    type_mapping = {'Running': 0, 'Strength': 1, 'HIIT': 2}
    intensity_mapping = {'Easy': 0, 'Moderate': 1, 'Hard': 2}

    input_data = np.array([
        int(duration),
        type_mapping[workout_type],
        intensity_mapping[intensity]
    ]).reshape(1, -1)

    # Generate workout plan using the model
    prediction = model.predict(input_data)[0]
    workout_plan = [
        {"phase": "Warm-Up", "exercise": "Arm Circles", "duration": f"{int(prediction[2])} minute", "sets": "-", "rest": "-"},
        {"phase": "Upper Body", "exercise": "Push-Ups", "reps": f"{int(prediction[1])}", "sets": f"{int(prediction[0])}", "rest": "30 seconds"},
        {"phase": "Cool Down", "exercise": "Child's Pose", "duration": f"{int(prediction[3])} minute", "sets": "-", "rest": "-"}
    ]

    return render_template('result.html', workout_plan=workout_plan)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
