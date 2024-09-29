
# IIT-Jodhpur Bicycle Rental Management System

## Introduction
The Bicycle Rental Management System is a web-based application designed to facilitate the rental of bicycles on the Indian Institute of Technology Jodhpur campus. The system allows users to register, login, view the availability of bicycles in real-time and book them for a specified duration. The project has been developed as part of a mini-project submission for the course Software and Data engineering which serves as the foundation for future enhancements in the main project.

## Features
- **User Registration**: New users can register by providing their personal information such as their name, mobile number and setting a password. All passwords are securely hashed using SHA-256.
- **User Login**: Registered users can login using their mobile number and password.
- **Cycle Booking**: Users can view available bicycles and book bicycle for a specified number of days for rental.
- **Booking Management**: The system tracks each user's current booking and ensures that only one bicycle is booked at a time.
- **Real-Time Cycle Availability**: The availability of bicycles is updated in real-time as they are rented.
- **Overdue Management**: The system tracks overdue rentals and updates the status of overdue cycles.

## Tech Stack
### Frontend:
- HTML
- CSS

### Backend:
- Python
- Flask

### Database:
- MySQL

### Cloud Platform:
- Google Cloud Platform (GCP)
- App Engine for deployment
- Cloud SQL for database management

## Project Setup (Local)
### 1. Clone the repository:
```bash
git clone https://github.com/PujaSr/Bicycle_Rental/tree/main
cd bicycle_rental
```

### 2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  
```

### 3. Install the dependencies:
```bash
pip install -r requirements.txt
```

### 4. Set up the MySQL database:
Ensure MySQL is installed on your local machine. After installation:
```sql
CREATE DATABASE bicycle_rental;
USE bicycle_rental;
```
- Import the provided `bicycle_rental.sql` file to create the necessary tables:
```bash
mysql -u root -p bicycle_rental < bicycle_rental.sql
```

### 5. Update `app.py` with your local MySQL configurations:
In the `app.py` file, ensure that your MySQL credentials match your local database setup.

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '<your mysql password>'
app.config['MYSQL_DB'] = 'bicycle_rental'
```

### 6. Run the application:
```bash
python app.py
```
The app will be accessible locally at: `http://127.0.0.1:5000`

## Cloud Deployment (GCP)
### 1. Google Cloud Setup:
Ensure that you have a Google Cloud account and have enabled App Engine and Cloud SQL.
- In GCP, create an App Engine instance.
- Set up a Cloud SQL instance and connect it to your application.

### 2. Update `app.yaml`:
In the `app.yaml` file, configure your cloud database credentials:
```yaml
env_variables:
  MYSQL_HOST: '35.244.54.218'
  MYSQL_USER: 'bicycle-rental'
  MYSQL_PASSWORD: '<your cloud sql password>'
  MYSQL_DB: 'bicycle_rental'
```

### 3. Deploy the app:
Deploy the app using Google Cloud SDK:
```bash
gcloud app deploy
```

## Performance Comparison
The performance of the Bicycle Rental Management System was tested both locally and on the cloud. The local setup offers quick response times but is limited by machine resources. The cloud deployment however offers greater scalability, especially during high traffic, by leveraging GCP's App Engine auto-scaling.

### Performance Metrics (Local vs Cloud):
- **Response Time:** Local deployment offers a faster response time due to no network overhead, but cloud deployment is more scalable.
- **Resource Usage:** Cloud deployment automatically scales CPU and memory based on traffic, while local deployment is limited to the machine's hardware.
- **Network Usage:** Network bandwidth usage is optimized in cloud deployment due to GCP's infrastructure.

## Future Enhancements
- **Microservices Architecture**: The main project will migrate the current monolithic architecture into a microservices architecture for better scalability and maintainability.
- **Containerization**: Docker will be used for containerization, allowing the app to run in any environment.
- **Real-time Notifications**: Kafka will be integrated to enable real-time notifications for cycle bookings and availability.
- **Admin Dashboard**: A full-fledged admin dashboard will be implemented to allow admins to manage cycle bookings and availability.



