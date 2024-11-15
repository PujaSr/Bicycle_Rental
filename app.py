from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
import hashlib
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Puja2024'
app.config['MYSQL_DB'] = 'bicycle_rental'

mysql = MySQL(app)

# Home route (Landing page)
@app.route('/')
def home():
    return render_template('home.html')

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = str(uuid.uuid4())
        name = request.form['name']
        mobile_number = request.form['mobile_number']
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (id, name, mobile_number, email, password, is_admin) VALUES (%s, %s, %s, %s, %s, %s)', 
                       (user_id, name, mobile_number, email, hashed_password, False))  # By default, users are not admins
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
            session['user_id'] = user[0]
            session['name'] = user[1]
            session['is_admin'] = user[5]  # Assuming is_admin is at index 5 in the user record
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
    cursor.close()
    return render_template('dashboard.html', cycles=cycles)

# Cycle booking
@app.route('/book/<cycle_id>', methods=['POST'])
def book_cycle(cycle_id):
    if 'user_id' not in session:
        flash('Please log in to book a cycle.', 'danger')
        return redirect(url_for('login'))

    try:
        rental_days = int(request.form['rental_days'])
        cursor = mysql.connection.cursor()

        # Check if the cycle is available
        cursor.execute('SELECT status FROM cycles WHERE cycle_id = %s', (cycle_id,))
        cycle = cursor.fetchone()
        if not cycle or cycle[0] != 'Available':
            flash('Cycle is not available for booking.', 'danger')
            cursor.close()
            return redirect(url_for('dashboard'))

        # Check if the user already has an active booking
        cursor.execute('SELECT * FROM bookings WHERE user_id = %s AND return_time IS NULL', (session['user_id'],))
        active_booking = cursor.fetchone()
        if active_booking:
            flash('You already have an active booking. Please return the cycle before booking another.', 'danger')
            cursor.close()
            return redirect(url_for('dashboard'))

        # Calculate the return time based on rental days
        return_time = datetime.now() + timedelta(days=rental_days)
        cursor.execute('UPDATE cycles SET status = %s, user_id = %s WHERE cycle_id = %s', ('Not Available', session['user_id'], cycle_id))
        cursor.execute('INSERT INTO bookings (user_id, cycle_id, rental_days, return_time) VALUES (%s, %s, %s, %s)',
                       (session['user_id'], cycle_id, rental_days, return_time))
        mysql.connection.commit()
        cursor.close()
        flash(f'Cycle successfully booked for {rental_days} days!', 'success')
        return redirect(url_for('dashboard'))

    except Exception as e:
        print(f"Error during booking process: {str(e)}")
        flash(f'Error in booking cycle: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

# Admin route to return a cycle
@app.route('/return/<cycle_id>', methods=['POST'])
def return_cycle(cycle_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Only admins can return cycles.', 'danger')
        return redirect(url_for('dashboard'))

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE cycles SET status = %s, user_id = NULL WHERE cycle_id = %s', ('Available', cycle_id))
        cursor.execute('UPDATE bookings SET return_time = %s WHERE cycle_id = %s AND return_time IS NULL', 
                       (datetime.now(), cycle_id))
        mysql.connection.commit()
        cursor.close()
        flash('Cycle returned successfully!', 'success')
    except Exception as e:
        print(f"Error during cycle return process: {str(e)}")
        flash(f'Error in returning cycle: {str(e)}', 'danger')

    return redirect(url_for('dashboard'))

# Logging out
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!', 'info')
    return redirect(url_for('home'))

# Start the Flask app without debug mode
if __name__ == '__main__':
    app.run()
