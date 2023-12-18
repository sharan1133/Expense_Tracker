from flask import Flask, render_template, request, redirect, url_for , flash
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = 'expenses.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def init_db():
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                Date TEXT PRIMARY KEY,
                Food REAL,
                Travel REAL,
                House REAL,
                Internet_Payments REAL,
                Necessities REAL,
                Extras REAL,
                Investments REAL
            )
        ''')
        db.commit()

init_db()

@app.route('/')
def index():
    status_message = request.args.get('message')
    success = request.args.get('success')
    return render_template('index.html' , message = status_message , success = success)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        date_option = request.form['date_option']

        if date_option == 'today':
            current_date = datetime.now().strftime('%Y-%m-%d')
        else:
            current_date = request.form['custom_date']

        expenses = [
            request.form['food'],
            request.form['travel'],
            request.form['house'],
            request.form['internet_payments'],
            request.form['necessities'],
            request.form['extras'],
            request.form['investments']
        ]

        expenses_with_date = [current_date] + [float(expense) if expense else 0.0 for expense in expenses]

        with connect_db() as db:
            cursor = db.cursor()
            cursor.execute('''
                INSERT INTO expenses (Date, Food, Travel, House, Internet_Payments, Necessities, Extras, Investments)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', expenses_with_date)
            db.commit()
         
        message = "Form submitted successfully!"
        success = True
        
        
        return redirect(url_for('index' , message = message , success = success))
        

    except Exception as e:

        message = f"An error occurred: {str(e)}"
        success = False
    
    return render_template("index.html" , message = message , success = success)

if __name__ == '__main__':
    app.run(debug=True)
