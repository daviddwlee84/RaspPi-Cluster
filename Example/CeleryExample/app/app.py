from flask import Flask, jsonify
from tasks import example_task

app = Flask(__name__)


@app.route("/run-task", methods=["GET"])
def run_task():
    result = example_task.delay()
    return jsonify({"task_id": result.id, "status": "Task triggered!"}), 200

# TODO: home page with button trigger "run-task"
