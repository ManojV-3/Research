# ResearchVault — Faculty Research Publication Management System

A responsive full-stack web application for storing, managing, and browsing faculty research publications.

## Tech Stack

| Layer    | Technology                      |
|----------|---------------------------------|
| Backend  | Python 3.10+ / Flask            |
| Database | MySQL (production) / SQLite (dev)|
| Frontend | HTML5, CSS3, Vanilla JavaScript  |
| ORM      | Flask-SQLAlchemy                |

---

## Project Structure

```
research_pub/
├── app.py                  # Flask app + API routes
├── requirements.txt        # Python dependencies
├── setup_mysql.sql         # MySQL schema + seed data
├── instance/
│   └── research_pub.db     # SQLite DB (auto-created in dev)
├── static/
│   ├── css/style.css       # Design system & responsive styles
│   └── js/main.js          # Shared JS utilities
└── templates/
    ├── base.html           # Navbar, layout, footer
    ├── index.html          # Dashboard with stats
    ├── faculty.html        # Faculty management
    ├── add.html            # Add publication form
    └── view.html           # Browse & filter publications
```

---

## Quick Start (SQLite — no MySQL needed)

```bash
# 1. Navigate to project folder
cd research_pub

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Open your browser at **http://localhost:5000**

---

## Production Setup with MySQL

### Step 1 — Create database & user

```bash
mysql -u root -p < setup_mysql.sql
```

### Step 2 — Set environment variable

```bash
# Linux / macOS
export DATABASE_URL="mysql+pymysql://research_user:ResearchVault@2024@localhost/research_pub"

# Windows PowerShell
$env:DATABASE_URL = "mysql+pymysql://research_user:ResearchVault@2024@localhost/research_pub"
```

### Step 3 — Run the app

```bash
python app.py
```

---

## API Reference

| Method | Endpoint                    | Description                  |
|--------|-----------------------------|------------------------------|
| GET    | `/api/faculty`              | List all faculty             |
| POST   | `/api/faculty`              | Add a faculty member         |
| DELETE | `/api/faculty/<id>`         | Delete faculty (cascades)    |
| GET    | `/api/publications`         | List/filter publications     |
| POST   | `/api/publications`         | Add a publication            |
| DELETE | `/api/publications/<id>`    | Delete a publication         |
| GET    | `/api/stats`                | Dashboard statistics         |

### Filter publications

```
GET /api/publications?faculty_id=1&pub_type=journal&year=2023&search=deep+learning
```

---

## Features

- **Dashboard** — Live statistics: faculty count, publication breakdown by type
- **Faculty Module** — Add, list, and delete faculty profiles with designation, department, year
- **Publication Module** — Record journal articles, conference papers, book chapters, and books
- **Browse Module** — Full-text search + filter by faculty, type, and year
- **Responsive UI** — Works on desktop and mobile
- **Cascade Delete** — Deleting a faculty member removes all their publications

## Publication Types

| Type         | Identifiers  |
|--------------|-------------|
| Journal      | ISSN         |
| Conference   | ISSN         |
| Book Chapter | ISBN         |
| Book         | ISBN         |
