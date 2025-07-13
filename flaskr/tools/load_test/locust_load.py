from locust import HttpUser, TaskSet, task, between
import json

class UserBehavior(TaskSet): # for every user

    def on_start(self): # on new user (total of -u <users> times)
        # Login and obtain JWT token
        response = self.client.post("/login", json={"username": "user", "password": "pass"}, cookies={"cookie_name": "cookie_value"}  )
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(1)
    def create_item(self):
        self.client.post("/items", json={"name": "item1", "description": "An item"}, headers=self.headers)

    @task(2)
    def read_item(self):
        response = self.client.get("/items/1", headers=self.headers)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        assert "expected_content" in response.text, "Expected content not found in response"

    @task(3)
    def update_item(self):
        self.client.put("/items/1", json={"name": "item1_updated", "description": "An updated item"}, headers=self.headers)

    @task(4)
    def delete_item(self):
        self.client.delete("/items/1", headers=self.headers)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5) # wait between 1 and 5 seconds after each task
    host = "http://your-api-url.com"  # Replace with your API URL
    min_wait = 1000  # Minimum wait time in milliseconds
    max_wait = 5000  # Maximum wait time in milliseconds

def run_locust():
    import os
    import subprocess

    # Define the number of users and spawn rate
    # in 10 sec all users run (100 users = 10 users/sec * 10 sec)
    num_users = 100 # 100 users
    spawn_rate = 10 # 10 users per second

    # Command to run Locust with specified options
    cmd = [
        "locust",
        "-f", "./flaskr/tools/load_test/locustfile.py",
        "--headless",
        "-u", str(num_users),
        "-r", str(spawn_rate),
        "--run-time", "1m",  # Duration of the test for timeout
        "--html", "./flaskr/tools/load_test/locust_report.html",  # Prefix for the CSV report files
        "--host", "http://your-api-url.com"  # Replace with your API URL
    ]

    subprocess.run(cmd)

if __name__ == "__main__":
    run_locust()

# to run locust with gui: http://localhost:8089 run for 1m
# locust -f ./flaskr/tools/load_test/locustfile.py -u 10 -r 2 -H http://localhost:8000 --web --run-time 1m

# to run locust witout his web page live info run for 1m
# locust -f ./flaskr/tools/load_test/locustfile.py -u 10 -r 2  -H http://localhost:8000 --headless --run-time 1m --html ./flaskr/tools/load_test/locust_report.html
