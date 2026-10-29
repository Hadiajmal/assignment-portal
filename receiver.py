from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/report", methods=["POST"])
def report():
    data = request.get_json(force=True)
    with open("test-report.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Report saved:", data.get("overall_status"))
    return jsonify(saved=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)