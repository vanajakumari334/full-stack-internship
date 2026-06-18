from flask import Flask, render_template, redirect, request
import sqlite3

app = Flask(__name__)

# Create database
conn = sqlite3.connect('coffee.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS coffees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    image TEXT,
    votes INTEGER
)
''')

cursor.execute('SELECT COUNT(*) FROM coffees')

count = cursor.fetchone()[0]

if count == 0:

    coffees = [

        (
            'Cappuccino',
            'Rich espresso with steamed milk foam.',
            'https://images.unsplash.com/photo-1509042239860-f550ce710b93',
            0
        ),

        (
            'Espresso',
            'Strong and bold Italian coffee shot.',
            'https://images.unsplash.com/photo-1511920170033-f8396924c348',
            0
        ),

        (
            'Latte',
            'Smooth coffee with creamy milk texture.',
            'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085',
            0
        ),

        (
            'Cold Coffee',
            'Refreshing chilled coffee drink.',
            'https://images.unsplash.com/photo-1461023058943-07fcbe16d735',
            0
        )

    ]

    cursor.executemany(
        '''
        INSERT INTO coffees
        (name, description, image, votes)
        VALUES (?, ?, ?, ?)
        ''',
        coffees
    )

conn.commit()
conn.close()


@app.route('/')
def home():

    search = request.args.get('search', '')

    conn = sqlite3.connect('coffee.db')
    cursor = conn.cursor()

    if search:

        cursor.execute(
            "SELECT * FROM coffees WHERE name LIKE ?",
            ('%' + search + '%',)
        )

    else:

        cursor.execute(
            "SELECT * FROM coffees ORDER BY votes DESC"
        )

    coffees = cursor.fetchall()

    conn.close()

    return render_template(
        'index.html',
        coffees=coffees,
        search=search
    )


@app.route('/vote/<int:id>')
def vote(id):

    conn = sqlite3.connect('coffee.db')
    cursor = conn.cursor()

    cursor.execute(
        'UPDATE coffees SET votes = votes + 1 WHERE id=?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)