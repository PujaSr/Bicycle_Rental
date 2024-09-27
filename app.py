import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
import hashlib
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configurations using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', '35.244.54.218')  # Default to your IP if env variable is missing
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'bicycle-rental')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'Puja2024')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'bicycle_rental')

mysql = MySQL(app)

# Home route (Landing page)
@app.route('/')
def home():
    return render_template('home.html')

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = str(uuid.uuid4())  # Generate unique ID
        name = request.form['name']
        mobile_number = request.form['mobile_number']
        password = request.form['password']

        # Hash the password for security
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert user into the database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (id, name, mobile_number, password) VALUES (%s, %s, %s, %s)', 
                       (user_id, name, mobile_number, hashed_password))
        mysql.connection.commit()
        cursor.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mobile_number = request.form['mobile_number']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE mobile_number = %s AND password = %s', 
                       (mobile_number, hashed_password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['user_id'] = user[0]  # Store user ID in session
            session['name'] = user[1]
            flash(f'Welcome, {user[1]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid login credentials. Please try again.', 'danger')

    return render_template('login.html')

# User dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM cycles')
    cycles = cursor.fetchall()

    # Calculate overdue status and time to return for each cycle
    updated_cycles = []
    for cycle in cycles:
        if cycle[1] == 'Not Available':
            cursor.execute('SELECT rented_time, return_time FROM bookings WHERE cycle_id = %s AND return_time IS NOT NULL', (cycle[0],))
            booking = cursor.fetchone()
            if booking:
                rented_time = booking[0]
                return_time = booking[1]
                current_time = datetime.now()

                if return_time is not None:
                    # Calculate the time to return
                    if return_time > current_time:
                        days_remaining = (return_time - current_time).days
                        overdue_status = 'On Time'
                    else:
                        days_remaining = 0  # If overdue, set days_remaining to 0
                        overdue_days = (current_time - return_time).days
                        overdue_status = f'Overdue by {overdue_days} days'
                else:
                    days_remaining = 'N/A'
                    overdue_status = 'Not Returned Yet'
                
                # Append return time and overdue status to the cycle tuple
                updated_cycles.append(cycle + (days_remaining, overdue_status))
        else:
            updated_cycles.append(cycle + (None, None))

    cursor.close()
    return render_template('dashboard.html', cycles=updated_cycles)

# Cycle booking with rental days
@app.route('/book/<cycle_id>', methods=['POST'])
def book_cycle(cycle_id):
    if 'user_id' not in session:
        flash('Please log in to book a cycle.', 'danger')
        return redirect(url_for('login'))

    try:
        # Get rental days from the form
        rental_days = int(request.form['rental_days'])

        # Check if the user already booked a cycle
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM bookings WHERE user_id = %s AND return_time IS NULL', (session['user_id'],))
        active_booking = cursor.fetchone()

        if active_booking:
            flash('You already have an active booking. Please return the cycle before booking another.', 'danger')
            return redirect(url_for('dashboard'))

        # Calculate the return time based on rental days
        return_time = datetime.now() + timedelta(days=rental_days)

        # Update cycle status and create a booking
        cursor.execute('UPDATE cycles SET status = %s, user_id = %s WHERE cycle_id = %s', ('Not Available', session['user_id'], cycle_id))
        
        cursor.execute('INSERT INTO bookings (user_id, cycle_id, rental_days, return_time) VALUES (%s, %s, %s, %s)', 
                       (session['user_id'], cycle_id, rental_days, return_time))
        mysql.connection.commit()
        
        cursor.close()

        flash(f'Cycle successfully booked for {rental_days} days!', 'success')
        return redirect(url_for('dashboard'))

    except Exception as e:
        flash(f'Error in booking cycle: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

# Logging out
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!', 'info')
    return redirect(url_for('home'))

# Start the Flask app without debug mode
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
