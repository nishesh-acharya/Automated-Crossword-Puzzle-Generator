from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import openai
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash('Username already exists')
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('index.html', username=user.username)


@app.route('/puzzleeasy', methods=['GET', 'POST'])
def puzzle_easy():
    if request.method == 'POST':
        response = remove_ordinal_numbers(generate_crossword_clues(6))
        user = User.query.get(session['user_id'])
        return render_template('puzzle.html', difficulty='easy', result=response, username=user.username)
    else:
        user = User.query.get(session['user_id'])
        return render_template('index.html', username=user.username)


@app.route('/puzzlemedium', methods=['GET', 'POST'])
def puzzle_medium():
    if request.method == 'POST':
        response = remove_ordinal_numbers(generate_crossword_clues(9))
        user = User.query.get(session['user_id'])
        return render_template('puzzle.html', difficulty='medium', result=response, username=user.username)
    else:
        user = User.query.get(session['user_id'])
        return render_template('index.html', username=user.username)


@app.route('/puzzlehard', methods=['POST'])
def puzzle_hard():
    if request.method == 'POST':
        response = remove_ordinal_numbers(generate_crossword_clues(12))
        user = User.query.get(session['user_id'])
        return render_template('puzzle.html', difficulty='hard', result=response, username=user.username)
    else:
        user = User.query.get(session['user_id'])
        return render_template('index.html', username=user.username)


@app.route('/increase_score', methods=['GET','POST'])
def increase_score():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    increment = 0

    if request.form.get('increase_amount') == 'easy':
        increment = 5
    elif request.form.get('increase_amount') == 'medium':
        increment = 10
    elif request.form.get('increase_amount') == 'hard':
        increment = 15

    user.score += increment
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/leaderboard')
def leaderboard():
    top_users = User.query.order_by(User.score.desc()).limit(10)
    user = User.query.get(session['user_id'])
    return render_template('leaderboard.html', top_users=top_users, username=user.username)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

def generate_crossword_clues(a):
    # Set up OpenAI API client
    openai.api_key = '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'  # Replace with your actual OpenAI API key

    # Define the prompt
    prompt = f"""List {a} pairs of words(single word) of varying difficulty and clues for crossword puzzle as following.
    Guitar: Stringed musical instrument.
    Tiger: Large feline with stripes.
    Fireplace: Hearth for burning wood.
    Serendipity: The occurrence of fortunate events by chance; a happy accident or discovery.
    Word: Clue.
    """
    # Generate text using OpenAI's API
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.9
    )
    generated_text = response.choices[0].text.strip()

    return generated_text

def remove_ordinal_numbers(input_string):
    # Split the input string into lines
    lines = input_string.split('\n')

    # Loop through each line and remove the ordinal numbers using regex
    for i in range(len(lines)):
        # Use regex to find and remove the ordinal numbers and the dot following them
        lines[i] = re.sub(r'\d+[.)]\s*', '', lines[i])

    # Join the lines back into a string
    output_string = '\n'.join(lines)

    return output_string

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
