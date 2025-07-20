from flask import Flask, request, render_template, jsonify
from main import run_jarvis  # import your logic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    command = data.get("command", "")
    print("Received command:", command)
    run_jarvis(command)  # Your function speaks back
    return jsonify({"message": "Jarvis executed the command"})

if __name__ == '__main__':
    app.run(debug=True)
