from flask import Flask, render_template, redirect
import sqlite3
import random

app = Flask(__name__)

quotes = [

    (
        "Success is not final, failure is not fatal.",
        "Winston Churchill",
        "Success"
    ),

    (
        "Believe you can and you're halfway there.",
        "Theodore Roosevelt",
        "Motivation"
    ),

    (
        "Dream big and dare to fail.",
        "Norman Vaughan",
        "Dream"
    ),

    (
        "Push yourself because no one else will.",
        "Unknown",
        "Motivation"
    ),

    (
        "Small steps every day lead to big results.",
        "Unknown",
        "Growth"
    )
]

# Database
conn = sqlite3.connect('quotes.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT,
    author TEXT,
    category TEXT
)
''')

conn.commit()
conn.close()


@app.route('/')
def home():

    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM history ORDER BY id DESC'
    )

    history = cursor.fetchall()

    conn.close()

    return render_template(
        'index.html',
        history=history
    )


@app.route('/generate')
def generate():

    quote = random.choice(quotes)

    text = quote[0]
    author = quote[1]
    category = quote[2]

    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO history
        (quote, author, category)
        VALUES (?, ?, ?)
        ''',
        (text, author, category)
    )

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)