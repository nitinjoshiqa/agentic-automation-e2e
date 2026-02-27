import requests
import sys

url = 'http://localhost:11434/api/generate'
payload = {
    'model': 'mistral',
    'prompt': 'Say hello',
    'max_tokens': 10
}
try:
    r = requests.post(url, json=payload, timeout=5)
    print('STATUS', r.status_code)
    try:
        print('BODY', r.text[:1000])
    except Exception as e:
        print('BODY_READ_ERROR', e)
except Exception as e:
    print('ERROR', e)
    sys.exit(1)

