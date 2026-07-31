# Student Project

A Django REST Framework API for managing student records with Swagger UI integration.

## Setup & Running the Project

### 1. Navigate to Project Directory
```powershell
cd student_project
```

### 2. Activate Virtual Environment (`venv`)

Depending on your shell/OS, run one of the following commands:

- **Windows PowerShell**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(If execution policies block scripts, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first)*

- **Windows Command Prompt (cmd)**:
  ```cmd
  venv\Scripts\activate.bat
  ```

- **Git Bash / Linux / macOS**:
  ```bash
  source venv/Scripts/activate
  ```

### 3. Run Migrations
```powershell
python manage.py migrate
```

### 4. Start the Development Server
```powershell
python manage.py runserver
```

---

## API Documentation & Testing (Swagger UI)

Once the server is running, access Swagger UI in your browser at:
👉 **[http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)**

### Available Endpoints
- `GET /api/students/` - List all students
- `POST /api/students/` - Create a student
- `GET /api/students/all/` - Dedicated endpoint to get all students
- `GET /api/students/<id>/` - Retrieve student details by ID
- `PUT /api/students/<id>/update/` - Update student by ID
- `DELETE /api/students/<id>/delete/` - Delete student by ID