from flask import Flask, request 
import psycopg 
import os
import datetime
from dotenv import load_dotenv 
DATABASE_URL = "postgresql://neondb_owner:npg_CNnwvVKF9Gf1@ep-divine-tree-abq3by4v-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
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
                    content TEXT,
                    date DATE,
                    time TIME
                ) 
            """) 
            if request.method == "POST": 
                note = request.form["note"] 
                currentdatetime=datetime.datetime.now()
                date=currentdatetime.date()
                time=currentdatetime.time()
                cur.execute( 
                    "INSERT INTO notes (content,date,time) VALUES (%s,%s,%s)",
                    (note,date,time) 
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
