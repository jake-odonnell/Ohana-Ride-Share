from Flask_app import app
from Flask_app.controllers import login
from Flask_app.controllers import rides

if __name__ == '__main__':
    app.run(debug = True)