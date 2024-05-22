<h1 align="center" id="title">Attendance Management System Using Face Recognition</h1>

<p id="description">Welcome to the Attendance Management System An innovative solution for marking student attendance using face recognition technology. This system leverages Django for the backend and Python's face-recognition library to provide an efficient and reliable way to manage attendance in a college setting.</p>

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Face Recognition-Based Attendance: Students can mark their attendance using facial recognition ensuring a seamless and secure process.
*   Admin Dashboard: Admins can monitor student attendance manage registered students add courses and appoint new admins.
*   Single Attendance Per Day: The system ensures that each student's attendance is marked only once per day.
*   Student Registration: New students can register by providing their name course section and a photo.
*   Face Encoding: The system encodes and stores students' facial data during registration for future attendance verification.

<h2>🛠️ Installation Steps:</h2>

<p>1. Clone the Repository</p>

<p>2. Install Dependencies:</p>

```
pip install -r requirements.txt
```

<p>3. Apply Migrations:</p>

```
python manage.py makemigrations
```

```
python manage.py migrate
```

<p>5. Create a Superuser:</p>

```
python manage.py createsuperuser
```

<p>6. Run the Server:</p>

```
python manage.py runserver
```

<h2>🍰 Contribution Guidelines:</h2>

We welcome contributions to enhance this project. Feel free to fork the repository make your changes and submit a pull request. For major changes please open an issue first to discuss what you would like to change.

  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   Backend: Django
*   Face Recognition: face-recognition library (Python)
*   Database: SQLite (default for Django can be configured for other databases)
*   Frontend: HTML CSS JavaScript

