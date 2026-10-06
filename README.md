# Contact Management System

A beginner-friendly Contact Management System built with Python Flask, Bootstrap, and MySQL.

## Features

- Add contacts
- View all contacts
- Search by name, phone, email, or category
- Edit contacts
- Delete contacts
- Category selection
- Form validation for required fields
- Responsive Bootstrap interface

## Project Structure

```text
contact_management_system/
├── app.py
├── db_setup.sql
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_contact.html
│   ├── edit_contact.html
│   └── 404.html
└── static/
    └── style.css
```

## Setup on Windows

1. Make sure Python and MySQL are installed and MySQL Server is running.
2. Open Command Prompt or PowerShell inside this folder.
3. Create a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

4. Install dependencies:

```powershell
pip install -r requirements.txt
```

5. Create the database and table. Run `db_setup.sql` in MySQL Command Line Client or MySQL Workbench.
6. Copy `.env.example` to `.env` and put your actual MySQL password in `DB_PASSWORD`.
7. Start Flask:

```powershell
python app.py
```

8. Open `http://127.0.0.1:5000/` in your browser.

## Important

Do not upload the `.env` file to GitHub because it contains database credentials.
