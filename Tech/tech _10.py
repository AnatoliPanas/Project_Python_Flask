from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/v1/')
def home_page():
    return jsonify({"response": "home_page"})


@app.route('/api/v1/path/<path:fpath>/<string:name>')
def get_path_name(fpath, name):
    return jsonify({"response": f"fpath {fpath} Name:{name}"})


if __name__ == "__main__":
    app.run(debug=True)