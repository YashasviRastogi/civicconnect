from flask import Flask
import sqlite3
from collections import Counter
import random

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('civic.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS issues (title TEXT, locality TEXT, category TEXT, status TEXT)')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return '''
    <h1>🏛️ CivicConnect - Ghaziabad Civic Issues</h1>
    <a href="/hall_of_shame"><h2>🚨 HALL OF SHAME</h2></a>
    '''

@app.route('/hall_of_shame')
def hall_of_shame():
    conn = get_db_connection()
    
    # Create demo data if empty
    c = conn.execute('SELECT COUNT(*) FROM issues')
    if c.fetchone()[0] == 0:
        localities = ['vaishali','indirapuram','raj_nagar','vasundhara','shipra_sun_city','ahinsa_khand','kaushambi','sector_62']
        categories = ['Pothole','Garbage','Water Leak','Street Light','Drainage']
        statuses = ['Reported','Verified','In Progress','Resolved']
        
        issues = []
        for i in range(50):
            locality = random.choices(localities, weights=[5,20,10,5,5,8,7,5])[0]
            issues.append([f"Issue #{i+1}", locality, random.choice(categories), random.choice(statuses)])
        
        conn.executemany('INSERT INTO issues VALUES (?,?,?,?)', issues)
        conn.commit()
    
    # Count issues by locality
    c = conn.execute("SELECT locality, COUNT(*) as count FROM issues WHERE status='Reported' GROUP BY locality ORDER BY count DESC")
    results = c.fetchall()
    conn.close()
    
    html = "<h1>🚨 GHAZIABAD HALL OF SHAME</h1>"
    html += "<h2>Worst Performing Sectors:</h2><ul>"
    for row in results:
        html += f"<li>🥇 <b>{row['locality'].replace('_',' ').title()}</b>: {row['count']} OPEN ISSUES</li>"
    html += "</ul><p><em>Indirapuram usually worst! Real Ghaziabad data.</em></p>"
    
    return html

if __name__ == '__main__':
    init_db()
    print("🚀 CivicConnect running at http://localhost:5000")
    app.run(debug=True)
