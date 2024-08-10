from flask import Flask, render_template, request
from flask import jsonify
from service.user_service import UserService
from service.auth_service import AuthenticationService
app = Flask(__name__)


auth_service = AuthenticationService(secret_key="tomas_o_trem")


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user_service = UserService()
    user = user_service.check_user_credentials(username, password)
    if user:
        token = auth_service.generate_token(username)
        return jsonify(status="success",
                       message="Logged in successfully",
                       token=token)
    else:
        return jsonify(status="error", message="Invalid username or password"), 401


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    user_service = UserService()

    # Here, add logic to check if the user already exists to prevent duplicates
    user_id = user_service.insert_new_user(username, password, email)
    if user_id:
        return jsonify(status="success", message="Signed up successfully")
    else:
        return jsonify(status="error", message="Signup failed"), 400


@app.route('/testauth', methods=['GET'])
def test_auth():
    token = request.headers.get('Authorization')
    if token:
        user = auth_service.verify_token(token)
        if user:
            return jsonify(status="success", message="Authenticated")
        else:
            return jsonify(status="error", message="Invalid token"), 401
    else:
        return jsonify(status="error", message="No token provided"), 401


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
