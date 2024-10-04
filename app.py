from flask import Flask
from api.authentication import auth_blueprint

app = Flask(__name__)

# Register the blueprint with the app
app.register_blueprint(auth_blueprint, url_prefix='/auth')

@app.route('/')
def home():
    return "Welcome to the Flask API!"

if __name__ == '__main__':
    app.run(debug=True)
