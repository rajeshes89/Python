with open('test.json') as f:
    conf = json.load(f)


def get_api_token(url, payload):
    x = requests.post(url, json=payload)
    resp = x.json()
    return resp['auth_token']


def update_dns(token,url,payload):
    try:
        headers = {
            'authorization': f'Bearer {token}',
            'content-type': 'application/json'
        }
        print(url)
        x = requests.put(url, json=payload, headers=headers)
        return x.status_code, x.json()

    except Exception as err:
        print(traceback.format_exc())
        print(err)
        return 0

print(conf)
auth_token = get_api_token(conf["login_url"], conf["login_payload"])
print(auth_token)

status, response = update(auth_token,conf["update_url"],conf["update_payload_1"])
