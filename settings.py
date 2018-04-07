import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database file path
DATABASE = os.path.join(BASE_DIR, os.environ.get('DATABASE', default='db.sqlite3'))
