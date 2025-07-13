# !pip install openai aiohttp

import asyncio
import json
import openai
import aiohttp

openai.api_key = 'lm-studio'

async def fetch_completion(my_msg):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://localhost:1234/v1/completions', # no dialog history only this one
            headers={
                # 'Authorization': f'Bearer {openai.api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'meta-llama-3.1-8b-instruct',
                "prompt": my_msg,
                'temperature': 0.7,
                "max_tokens": 50, # -1 for unlimited
                "stream": True
            }
        ) as response:
            result = ""
            async for line in response.content:
                line = line.decode('utf-8').strip()
                if line.startswith("data: "):
                    data = line[len("data: "):]
                    if data != '[DONE]':
                        json_data = json.loads(data)
                        msg = json_data['choices'][0]['text']
                        print(msg, end='')
                        result += msg
            return result.strip()

prompt = "Once upon a time"
full_ans = asyncio.run(fetch_completion(prompt))
print("\n\n Full Answer:")
print(full_ans)
