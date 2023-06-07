from flask import jsonify

def get_app():
    from flask_app import app
    return app

app = get_app()

@app.route("/", methods=["GET"])
def hello():
    return jsonify({"Hello": "Welcome to the Doe Vida API"})