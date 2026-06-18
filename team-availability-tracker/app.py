from flask import Flask, render_template, redirect, request
import sqlite3

app = Flask(__name__)

# Database Setup
conn = sqlite3.connect('team.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS team (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    role TEXT,
    department TEXT,
    image TEXT,
    status INTEGER
)
''')

cursor.execute('SELECT COUNT(*) FROM team')

count = cursor.fetchone()[0]

if count == 0:

    members = [

        (
            'Priya Sharma',
            'Frontend Developer',
            'Development',
            'https://randomuser.me/api/portraits/women/44.jpg',
            1
        ),

        (
            'Rahul Verma',
            'Backend Engineer',
            'Development',
            'https://randomuser.me/api/portraits/men/32.jpg',
            0
        ),

        (
            'Sneha Patel',
            'UI/UX Designer',
            'Design',
            'https://randomuser.me/api/portraits/women/68.jpg',
            1
        ),

        (
            'Arjun Reddy',
            'Python Developer',
            'AI Team',
            'https://randomuser.me/api/portraits/men/51.jpg',
            0
        )

    ]

    cursor.executemany(
        '''
        INSERT INTO team
        (name, role, department, image, status)
        VALUES (?, ?, ?, ?, ?)
        ''',
        members
    )

conn.commit()
conn.close()


@app.route('/')
def home():

    search = request.args.get('search', '')

    conn = sqlite3.connect('team.db')
    cursor = conn.cursor()

    if search:

        cursor.execute(
            '''
            SELECT * FROM team
            WHERE name LIKE ?
            ''',
            ('%' + search + '%',)
        )

    else:

        cursor.execute(
            'SELECT * FROM team'
        )

    members = cursor.fetchall()

    conn.close()

    available = len(
        [m for m in members if m[5] == 1]
    )

    unavailable = len(
        [m for m in members if m[5] == 0]
    )

    return render_template(
        'index.html',
        members=members,
        available=available,
        unavailable=unavailable,
        search=search
    )


@app.route('/toggle/<int:id>')
def toggle(id):

    conn = sqlite3.connect('team.db')
    cursor = conn.cursor()

    cursor.execute(
        'SELECT status FROM team WHERE id=?',
        (id,)
    )

    current = cursor.fetchone()[0]

    new_status = 0 if current == 1 else 1

    cursor.execute(
        '''
        UPDATE team
        SET status=?
        WHERE id=?
        ''',
        (new_status, id)
    )

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)