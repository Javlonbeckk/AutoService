from flask import Flask, render_template
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"
load_dotenv()


DB_HOST = str(os.getenv("ip"))
DB_NAME = str(os.getenv("DATABASE"))
DB_USER = str(os.getenv("PGUSER"))
DB_PASS = str(os.getenv("PGPASSWORD"))

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT service, date, time, customer_phone, price FROM reservations where accepted=1 ORDER BY date"
    cur.execute(s)  # Execute the SQL
    list_users = cur.fetchall()
    return render_template('index.html', list_users=list_users)


if __name__ == "__main__":
    app.run(debug=True)


