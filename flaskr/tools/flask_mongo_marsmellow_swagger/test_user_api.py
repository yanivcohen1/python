import requests
import unittest
import time
import subprocess
import os
import signal

class TestUserAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/user"

    def test_post_and_get_user(self):
        # 1. Create a new user
        new_user = {
            "name": "Test User",
            "email": "test@example.com"
        }
        post_response = requests.post(self.BASE_URL, json=new_user)
        self.assertEqual(post_response.status_code, 201)
        created_user = post_response.json()
        self.assertEqual(created_user["name"], new_user["name"])
        self.assertIn("id", created_user)

        # 2. Get all users and check if the new user is there
        get_response = requests.get(self.BASE_URL)
        self.assertEqual(get_response.status_code, 200)
        users = get_response.json()
        self.assertTrue(any(u["email"] == new_user["email"] for u in users))

if __name__ == "__main__":
    unittest.main()
