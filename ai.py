import os
import json
from openai import OpenAI


# run
def run(content, token = None):
    if token is None:
        # default token for No token call
        token = "sk-Oo8q5QYIGSVtxHOomiBpUqJNyVSGS4yif7iGhhRsUCEyybu5"

    client = OpenAI(
        api_key = token,
        base_url = "https://api.lkeap.cloud.tencent.com/v1",
    )

    try:
        completion = client.chat.completions.create(
            model = "deepseek-r1-0528",
            messages = [
                {'role': 'user', 'content': content}
            ]
        )
        # dump(completion)
        result = completion.choices[0].message.content.strip()
        status = 1
        raw = dump(completion)
    except Exception as e:
        result = str(e)
        status = 3
        raw = None

    return {"result": result, "status": status, "raw": raw}


# dump
def dump(completion):
    return json.dumps(completion.to_dict(), indent=2, ensure_ascii=False)
