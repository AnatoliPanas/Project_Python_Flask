from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "You are on the HOME page."

if __name__ == "__main__":
    app.run(debug=True)