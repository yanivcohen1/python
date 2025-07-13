# !pip install openai aiohttp

import asyncio
import json
import openai
import aiohttp

openai.api_key = 'lm-studio'
code_highlight = ", the code in response will be like this ```{program_language_name}"

async def fetch_completion(my_msg, code_highlights = False):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://localhost:1234/v1/chat/completions', # for remembering dialog history
            headers={
                # 'Authorization': f'Bearer {openai.api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'meta-llama-3.1-8b-instruct',
                "messages": [
                  { "role": "system", "content": "if code is in response add the code like this ```{program_language_name}" },
                  { "role": "user", "content": my_msg if not code_highlights else my_msg + code_highlight }
                ],
                'temperature': 0.7,
                "max_tokens": -1, # -1 for unlimited
                "stream": True
            }
        ) as response:
            content = ""
            # display_handle = display(to_markdown(content), display_id=True)
            async for line in response.content:
                line = line.decode('utf-8').strip()
                if line.startswith("data: "):
                    data = line[len("data: "):]
                    if data != '[DONE]':
                        json_data = json.loads(data)
                        delta = json_data['choices'][0]['delta']
                        if 'content' in delta:
                            msg = delta['content']
                            print(msg, end='')
                            content += msg
                            # display_handle.update(to_markdown(content))
            return content

prompt = "Once upon a time"
full_ans = asyncio.run(fetch_completion(prompt))
# print("\n\n Full Answer:")
# print(full_ans)
