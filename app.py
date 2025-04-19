from flask import Flask, render_template, request, session
import wikipedia
import random

# Initialize the app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session


# Route for Home Page
@app.route('/')
def index():
    categories = ['science', 'history', 'technology', 'art', 'sports']
    return render_template('index.html', categories=categories)


# Route to start the test
@app.route('/start', methods=['POST'])
def start_test():
    category = request.form['category']
    search_results = wikipedia.search(category)
    if search_results:
        page_title = random.choice(search_results)
        try:
            fact = wikipedia.summary(page_title, sentences=2)
        except wikipedia.exceptions.DisambiguationError as e:
            fact = wikipedia.summary(random.choice(e.options), sentences=2)
    else:
        fact = "Could not find any interesting facts."

    session['fact'] = fact  # Save original text for checking later

    return render_template('test.html', fact=fact)


# Route to submit test
@app.route('/submit', methods=['POST'])
def submit():
    typed_text = request.form['typed_text']
    original_text = session.get('fact')
    time_taken = float(request.form['time_taken'])  # seconds

    # Calculate accuracy
    correct_chars = sum(1 for a, b in zip(typed_text, original_text) if a == b)
    total_chars = len(original_text)
    accuracy = (correct_chars / total_chars) * 100

    # Calculate WPM
    words = len(typed_text.split())
    minutes = time_taken / 60
    speed = words / minutes if minutes > 0 else 0

    return render_template('result.html', accuracy=round(accuracy, 2), speed=round(speed, 2))


# Start the app
if __name__ == "__main__":
    app.run()
