from flask import Flask
from app import app

app = Flask(__name__, template_folder='templates')

if __name__ == '__main__':
    app.run()
