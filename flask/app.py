from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "You are on the HOME page."

@app.route('/user/', defaults={'name': 'Anatoli'})
@app.route('/user/<string:name>')
def get_name(name):
    return f"Hello, {name}!"

@app.route('/registrate', methods=['POST'])
def post_request():
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']
    return f"Username: {username}\nPassword: {"*" * len(password)}\nEmail: {email}"

@app.route('/registrate2', methods=['POST'])
def post_request_form():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    return f"Username: {username}\nPassword: {password}\nEmail: {email}"

@app.route('/file/<path:file_path>/<age>')
def get_file(file_path, age):
    return f"MyPath: {file_path} {age}!"

if __name__ == "__main__":
    app.run(debug=True)