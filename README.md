# Password Manager Django Project

A secure Django-based password manager for storing and managing passwords with encryption and user authentication.

---

## 🚀 Features

- **Encrypted password storage** for enhanced security  
- **User authentication** and admin panel  
- **Easy setup** with SQLite (default) or other databases  
- **Environment variable support** for sensitive settings  

---

## 📦 Prerequisites

- **Python 3.12+**  
- **pip** (Python package manager)  
- **Git**  
- **virtualenv** (recommended, but optional)  

---

## 🛠️ Installation

### 1. Clone the Repository

```
git clone https://github.com/your_username/your_repository.git
cd your_repository
```

### 2. Create and Activate a Virtual Environment (Recommended)

**On Linux/macOS:**

```
python3 -m venv env
source env/bin/activate
```

**On Windows (PowerShell):**

```
python -m venv env
.\env\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Set Environment Variables

For security, set sensitive values (like the Django secret key and master password) as environment variables.

**On Linux/macOS:**

```
export DJANGO_SECRET_KEY='your_secret_key_here'
export MASTER_PASSWORD='your_master_password_here'
```

**On Windows (PowerShell):**

```
setx DJANGO_SECRET_KEY "your_secret_key_here"
setx MASTER_PASSWORD "your_master_password_here"
```

> **Note:** Make sure these variables are set before running the project.

### 5. Initialize the Database

If using SQLite (default), the database file will be created locally.

```
python manage.py migrate
```

### 6. Create a Superuser (Admin Account)

```
python manage.py createsuperuser
```

Follow the prompts to set your admin username and password.

---

## 🚦 Usage

### Run the Development Server

```
python manage.py runserver
```

Open your browser and go to: http://127.0.0.1:8000

### Access the Admin Panel

Visit http://127.0.0.1:8000/admin and log in with your superuser credentials.

---

## 🔒 Security & Sensitive Files

- The local database file (e.g., `db.sqlite3`) contains sensitive data. **Add it to `.gitignore`** to avoid pushing it to public repositories.  
- **Never commit your environment variables or secret keys.**

**Example `.gitignore` entry:**

```
# SQLite database
db.sqlite3
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository  
2. Create your feature branch (`git checkout -b feature/YourFeature`)  
3. Commit your changes (`git commit -am 'Add some feature'`)  
4. Push to the branch (`git push origin feature/YourFeature`)  
5. Open a Pull Request  

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

## ❓ Questions?

If you have any questions or need support, feel free to contact me.

---

> _Inspired by best practices for Django project documentation._
