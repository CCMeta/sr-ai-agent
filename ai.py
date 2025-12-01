import os
import json
from openai import OpenAI

def run(content):
    client = OpenAI(
        api_key="sk-Oo8q5QYIGSVtxHOomiBpUqJNyVSGS4yif7iGhhRsUCEyybu5",
        base_url="https://api.lkeap.cloud.tencent.com/v1",
    )

    completion = client.chat.completions.create(
        model="deepseek-r1-0528",
        messages=[
            {'role': 'user', 'content': content}
        ]
    )
    print(json.dumps(completion.to_dict(), indent=2, ensure_ascii=False))
    
    return completion.choices[0].message.content