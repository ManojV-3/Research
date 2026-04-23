from flask import Flask, render_template, request, jsonify, g
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'research-vault-2024'

DATABASE = os.path.join(os.path.dirname(__file__), 'instance', 'research_pub.db')
os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop('db', None)
    if db: db.close()

def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            designation TEXT NOT NULL, department TEXT NOT NULL,
            year_of_joining INTEGER NOT NULL, email TEXT NOT NULL UNIQUE,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS publication (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            faculty_id INTEGER NOT NULL REFERENCES faculty(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            pub_type TEXT NOT NULL CHECK(pub_type IN ('journal','conference','book_chapter','book')),
            publication_name TEXT NOT NULL, issn_isbn TEXT, pub_year INTEGER NOT NULL,
            pub_month TEXT NOT NULL, doi TEXT, created_at TEXT DEFAULT (datetime('now'))
        );
    """)
    db.commit(); db.close()

@app.route('/') 
def index(): return render_template('index.html')
@app.route('/faculty') 
def faculty_page(): return render_template('faculty.html')
@app.route('/add') 
def add_page(): return render_template('add.html')
@app.route('/view') 
def view_page(): return render_template('view.html')

@app.route('/api/faculty', methods=['GET'])
def get_faculty():
    rows = get_db().execute("""
        SELECT f.*, COUNT(p.id) as publication_count FROM faculty f
        LEFT JOIN publication p ON p.faculty_id = f.id GROUP BY f.id ORDER BY f.name
    """).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/faculty', methods=['POST'])
def add_faculty():
    data = request.get_json(); db = get_db()
    if db.execute("SELECT id FROM faculty WHERE email = ?", (data['email'],)).fetchone():
        return jsonify({'error': 'A faculty member with this email already exists.'}), 400
    try:
        cur = db.execute("INSERT INTO faculty (name,designation,department,year_of_joining,email) VALUES (?,?,?,?,?)",
            (data['name'],data['designation'],data['department'],int(data['year_of_joining']),data['email']))
        db.commit()
        return jsonify({'success': True, 'id': cur.lastrowid, 'message': 'Faculty member added successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/faculty/<int:fid>', methods=['DELETE'])
def delete_faculty(fid):
    db = get_db(); db.execute("DELETE FROM faculty WHERE id = ?", (fid,)); db.commit()
    return jsonify({'success': True})

@app.route('/api/publications', methods=['GET'])
def get_publications():
    db = get_db()
    q = """SELECT p.*, f.name as faculty_name, f.designation as faculty_designation,
           f.department as faculty_department FROM publication p JOIN faculty f ON p.faculty_id = f.id WHERE 1=1"""
    params = []
    for arg, col in [('faculty_id','p.faculty_id'),('pub_type','p.pub_type'),('year','p.pub_year')]:
        if request.args.get(arg):
            q += f" AND {col} = ?"; params.append(request.args[arg])
    if request.args.get('search','').strip():
        s = f"%{request.args['search'].strip()}%"; q += " AND (p.title LIKE ? OR p.publication_name LIKE ? OR f.name LIKE ?)"; params += [s,s,s]
    q += " ORDER BY p.pub_year DESC"
    return jsonify([dict(r) for r in db.execute(q, params).fetchall()])

@app.route('/api/publications', methods=['POST'])
def add_publication():
    data = request.get_json(); db = get_db()
    try:
        cur = db.execute("""INSERT INTO publication (faculty_id,title,pub_type,publication_name,issn_isbn,pub_year,pub_month,doi)
               VALUES (?,?,?,?,?,?,?,?)""",
            (int(data['faculty_id']),data['title'],data['pub_type'],data['publication_name'],
             data.get('issn_isbn',''),int(data['pub_year']),data['pub_month'],data.get('doi','')))
        db.commit()
        return jsonify({'success': True, 'id': cur.lastrowid, 'message': 'Publication saved successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/publications/<int:pid>', methods=['DELETE'])
def delete_publication(pid):
    db = get_db(); db.execute("DELETE FROM publication WHERE id = ?", (pid,)); db.commit()
    return jsonify({'success': True})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    db = get_db()
    return jsonify({
        'total_faculty': db.execute("SELECT COUNT(*) FROM faculty").fetchone()[0],
        'total_publications': db.execute("SELECT COUNT(*) FROM publication").fetchone()[0],
        'journals': db.execute("SELECT COUNT(*) FROM publication WHERE pub_type='journal'").fetchone()[0],
        'conferences': db.execute("SELECT COUNT(*) FROM publication WHERE pub_type='conference'").fetchone()[0],
        'book_chapters': db.execute("SELECT COUNT(*) FROM publication WHERE pub_type='book_chapter'").fetchone()[0],
        'books': db.execute("SELECT COUNT(*) FROM publication WHERE pub_type='book'").fetchone()[0],
        'years': [r[0] for r in db.execute("SELECT DISTINCT pub_year FROM publication ORDER BY pub_year DESC").fetchall()]
    })

if __name__ == '__main__':
    init_db(); app.run(debug=True, port=5000)
