from flask import Flask, render_template, request, jsonify
import sqlite3, os

app = Flask(__name__)

# crea il DB se non esiste
DB_PATH = "valutazioni.db"
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE infermieri (
            id TEXT PRIMARY KEY,
            nome TEXT,
            cognome TEXT,
            esperienza INTEGER,
            matricola TEXT,
            ruolo TEXT,
            valutatore TEXT,
            reparto TEXT,
            classeManuale INTEGER
        )
    """)
    c.execute("""
        CREATE TABLE valutazioni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            infermiere_id TEXT,
            data TEXT,
            reparto TEXT,
            total INTEGER,
            level TEXT,
            FOREIGN KEY(infermiere_id) REFERENCES infermieri(id)
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database creato con tabelle 'infermieri' e 'valutazioni'")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/inserisci', methods=['POST'])
def inserisci():
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT OR REPLACE INTO infermieri 
                 (id, nome, cognome, esperienza, matricola, ruolo, valutatore, reparto, classeManuale)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (data['id'], data['nome'], data['cognome'], data['esperienza'],
               data['matricola'], data['ruolo'], data['valutatore'],
               data['reparto'], data['classeManuale']))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route('/api/lista')
def lista():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT nome, cognome, reparto FROM infermieri")
    results = [{"nome": n, "cognome": c_, "reparto": r} for n, c_, r in c.fetchall()]
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
