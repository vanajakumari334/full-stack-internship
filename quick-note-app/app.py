from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create Database
conn = sqlite3.connect('notes.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    created_at TEXT
)
''')

conn.commit()
conn.close()


@app.route('/', methods=['GET', 'POST'])
def home():

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        note = request.form['note']

        time = datetime.now().strftime('%d-%m-%Y %H:%M')

        cursor.execute(
            'INSERT INTO notes (content, created_at) VALUES (?, ?)',
            (note, time)
        )

        conn.commit()

    cursor.execute('SELECT * FROM notes ORDER BY id DESC')

    notes = cursor.fetchall()

    conn.close()

    return render_template(
        'index.html',
        notes=notes
    )


@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute(
        'DELETE FROM notes WHERE id=?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)