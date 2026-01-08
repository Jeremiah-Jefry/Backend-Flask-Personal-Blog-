# My Blog - Flask Tutorial

A simple blog application built with Flask to learn web development.

## Setup

1. Install Flask:
```bash
pip install Flask
```

2. Create the database:
```bash
python init_db.py
```

3. Run the app:
```bash
python app.py
```

4. Open in browser: `http://localhost:5000`

## Features

- Create new posts
- View all posts
- Edit posts
- Delete posts
- Persistent database storage

## How It Works

- **app.py** - Main Flask application with routes
- **templates/** - HTML pages
- **static/style.css** - Styling
- **blog.db** - SQLite database