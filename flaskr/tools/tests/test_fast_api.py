
import unittest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from flaskr.tools.ai_chat.ollama_proxy_stream import app

class TestFastAPIApp(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.client = TestClient(app)
        self.ac = AsyncClient(base_url="http://localhost:11434", timeout=60)

    async def asyncTearDown(self):
        await self.ac.aclose()

    async def test_proxy_stream(self):
        request_body = {
                    'model': 'deepseek-r1:8b',
                    'messages': [
                        { "role": "system", "content": "" },
                        { "role": "user", "content": "hi" }
                    ],
                    'temperature': 0.7,
                    'max_tokens': -1,
                    'stream': True
                }
        response = await self.ac.post("/v1/chat/completions", json=request_body)
        self.assertEqual(response.status_code, 200)
        # Additional checks based on your response content

    async def test_non_stream_proxy_get(self):
        response = await self.ac.get("/v1/models")  # Replace with an actual endpoint
        self.assertEqual(response.status_code, 200)
        # Additional checks based on your response content

    async def test_non_stream_proxy_post(self):
        request_body = {"key": "value"}  # Add appropriate request body for your test
        response = await self.ac.post("/v1/models", json=request_body)  # Replace with an actual endpoint
        self.assertEqual(response.status_code, 200)
        # Additional checks based on your response content

    async def test_non_stream_proxy_options(self):
        response = await self.ac.options("/v1/models")  # Replace with an actual endpoint
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"message": "Method Not Allowed"})

if __name__ == "__main__":
    unittest.main()
