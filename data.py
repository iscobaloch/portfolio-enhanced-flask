from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  import Config
from models import db, db2  # Import db from models.py

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the databases
db.init_app(app)  # Default db
db2.init_app(app)  # Second db for 'wali'

# Create all tables for the default database (db)
with app.app_context():
    db.create_all()  # Creates all tables for the default database
    db2.create_all(bind='wali')  # Creates all tables for the 'wali' database

if __name__ == '__main__':
    app.run(debug=True)
