# Linkify – Smart URL Shortener

## About the Project

Linkify is a Python Flask-based URL Shortener Web Application developed as part of the CodeAlpha Backend Internship.

It allows users to convert long URLs into short, clean and shareable links. Users can also view their generated URL history and track the number of clicks on each shortened link.

## Features

- Shorten long URLs into unique short links.
- HTTP and HTTPS URL validation.
- Redirect short links to their original URLs.
- Track the number of clicks.
- Store URL records using SQLite.
- View recently generated URLs.
- Handle blank and invalid URL inputs.
- Simple and responsive user interface.

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript

## Project Structure

```text
Task1_URL_Shortener/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── urls.db
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project directory

```bash
cd Task1_URL_Shortener
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

### 7. Open in browser

```text
http://127.0.0.1:5000/
```

## Database

Linkify uses SQLite to store original URLs, shortened URLs and click counts.

## Testing

The following tests were performed:

- URL shortening
- Google URL redirection
- Wikipedia URL redirection
- Click tracking
- Invalid URL validation
- Blank input validation
- Database persistence after server restart
- Homepage navigation

## Internship

Developed as part of the CodeAlpha Backend Development Internship.

**Project Name:** Linkify – Smart URL Shortener
