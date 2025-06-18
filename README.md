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

> **Note:** Setting these variables is optional — the application will fall back to default values if they are not defined.


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

## 🧭 Application Usage Flow

### User Perspective

1. **Register and Login:**  
   Users create an account and log in with their credentials.

2. **Master Password Input:**  
   After login, users enter their Master Password, which is never stored but used during the session to encrypt/decrypt passwords.

3. **Manage Password Entries:**  
   - Add new password entries, which get encrypted with a key derived from the Master Password and a unique user-specific salt.  
   - View and copy decrypted passwords on demand.  
   - Edit and delete entries (as implemented).

4. **Session Security:**  
   Master Password is kept only in the session and cleared upon logout to keep data safe.

### Developer Perspective

1. **Models and Encryption:**  
   - `PasswordEntry` model stores encrypted passwords; the `user` foreign key links entries to users.  
   - Encryption uses Fernet symmetric encryption; the key is derived from the user’s Master Password plus a per-user salt stored in a `VaultSettings` model using PBKDF2 HMAC SHA256.

2. **Form Handling:**  
   - Custom forms accept the Master Password temporarily to encrypt/decrypt password fields without storing the master password.  
   - The form's `save(commit=False)` method allows setting the `user` before saving to the database.

3. **Session Management:**  
   - Master Password is stored securely in the Django session during user activity to enable encryption/decryption.  
   - It is never persisted in the database or logs.

4. **Security Measures:**  
   - The salt per user ensures unique encryption keys, preventing cross-user key reuse.  
   - The app avoids exposing password lengths or raw encrypted data in UI or logs, using dummy placeholders when necessary.  
   - Sensitive data such as the database file and environment variables are excluded from source control via `.gitignore`.

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

## ⚙️ Scalability

This project is designed to run locally with SQLite and Django’s built-in development server, but it can be scaled for production in the following ways:

## 🔼 Vertical Scaling
More powerful server: Run the Django app on a server with more CPU, RAM, and storage.

Database upgrade: Switch from SQLite to PostgreSQL or MySQL for better performance, reliability, and concurrency support.

Gunicorn/Uvicorn: Replace Django's development server with a production-ready WSGI/ASGI server like Gunicorn (for synchronous apps) or Uvicorn (for async support).

## 🌐 Horizontal Scaling
Multiple app instances: Deploy multiple instances of the Django application behind a reverse proxy.

Load balancing with Nginx: Use Nginx to distribute incoming requests across app instances. This improves availability and supports more simultaneous users.

Shared database: All app instances should connect to the same external database (e.g., PostgreSQL on a managed cloud service or a dedicated DB server).

Static/media file handling: Serve static and uploaded files via a shared file system (like NFS) or object storage (e.g., AWS S3).

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ❓ Questions?

If you have any questions or need support, feel free to contact me.

---

> _Inspired by best practices for Django project documentation._
