import requests
import json

def make_todo_request():
    request_url = 'http://localhost:1087/api/todo/'
    headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }

    request_body = {
                        "title": "Testing",
                        "description": "Just to test the Request", 
                    }

    res = requests.post(request_url, headers=headers, data=json.dumps(request_body))
    requests.put
    if res.ok:
        print(res.json())

make_todo_request()
