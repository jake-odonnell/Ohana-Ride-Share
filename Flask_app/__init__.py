from flask import Flask
app = Flask(__name__)
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

app.secret_key = 'saodngjw5i0'