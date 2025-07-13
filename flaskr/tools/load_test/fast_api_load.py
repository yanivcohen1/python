import random
import datetime
from locust import HttpUser, task, between

# https://www.youtube.com/watch?v=esIEW0aEKqk

sentences = [
    "That's just what I needed today",
    "I love coding in python",
    "Well what a surprise",
    "James hates eating onions",
]
# host = "http://127.0.0.1:8000"


class AppUser(HttpUser): # for every user

    wait_time = between(1, 5)  # wait between 1 and 5 seconds after each task

    def on_start(self): # on new user (total of -u <users> times)
        # Login and obtain JWT token
        now = datetime.datetime.now()
        print("start new user:", now)

    @task
    def index_page(self):
        response = self.client.get("/")
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        assert "Hello FastAPI" in response.text, "Expected content not found in response"

    @task
    def sentiment_page(self):
        mytext = random.choice(sentences)
        self.client.get("/sentiment/" + str(mytext))

# for help: locust -h

# for debug brackpoint
# select "Python:Locust" in debug

# run with gui: http://localhost:8089 1m run time
# locust -f ./flaskr/tools/load_test/fast_api_load.py -u 10 -r 2 -H http://localhost:8000 --run-time 1m

# run without gui 1m run time
# locust -f ./flaskr/tools/load_test/fast_api_load.py -u 10 -r 2 -H http://localhost:8000 --headless --run-time 1m --html flaskr/tools/load_test/locust_report.html
