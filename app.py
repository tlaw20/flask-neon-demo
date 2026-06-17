from flask import Flask, request 
import psycopg 
import os
from dotenv import load_dotenv 
DATABASE_URL = os.getenv("DATABASE_URL") 
load_dotenv() 
app = Flask(__name__) 
DATABASE_URL = os.environ["DATABASE_URL"] 
@app.route("/", methods=["GET", "POST"]) 
def home(): 
    with psycopg.connect(DATABASE_URL) as conn: 
        with conn.cursor() as cur: 
            cur.execute(""" 
                CREATE TABLE IF NOT EXISTS notes ( 
                    id SERIAL PRIMARY KEY, 
                    content TEXT 
                ) 
            """) 
            if request.method == "POST": 
                note = request.form["note"] 
                cur.execute( 
                    "INSERT INTO notes (content) VALUES (%s)", 
                    (note,) 
                ) 
            cur.execute( 
                "SELECT id, content FROM notes ORDER BY id DESC"
            ) 
            notes = cur.fetchall() 
        html = "<h1>Notes</h1>" 
        html += """ 
        <form method='post'> 
            <input name='note'> 
            <button>Add Note</button> 
        </form> 
        """ 
        for note in notes:
            html += f"<p>{note[1]}</p>" 
        return html 
        
if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=3000, debug=True) 
