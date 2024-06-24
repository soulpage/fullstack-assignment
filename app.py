from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize extensions
db = SQLAlchemy(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

if __name__ == '__main__':
    app.run(debug=True)
