# Example of an endpoint handler on Flask

from flask import Flask, request
import datetime
import os


class LogManager:
    def __init__(self, logs_dir="klgrr_logs"):
        self.path_for_logs = os.path.join(os.path.dirname(__file__), logs_dir)
        if not os.path.exists(self.path_for_logs):
            os.makedirs(self.path_for_logs, exist_ok=True)
    
    def write_log(self, username, computer_name, text):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(os.path.join(self.path_for_logs, f"{username}.{computer_name}.log"),
                  "a", encoding="utf-8") as f:
            f.write(f"[{current_time}] {username}.{computer_name}: {text}\n")


class POSTKLgrrApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.log_manager = LogManager()
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/', methods=['POST'])
        def receive_data():
            data = request.get_json()
            computer_name = data.get('computer_name', 'Unknown')
            username = data.get('username', 'User')
            text = data.get('text', '')
            self.log_manager.write_log(username, computer_name, text)
            return "200"
    
    def run(self, **kwargs):
        self.app.run(threaded=True, **kwargs)


if __name__ == '__main__':
    app = POSTKLgrrApp()
    app.run()
