def build_post_data(auth_token, goal, value, comment):
    from time import time
    params = {
            'auth_token': auth_token,
            'timestamp': round(time()),
            'value': value,
            'comment': comment,
            }
    url = 'https://www.beeminder.com/api/v1/users/me/goals/{}/datapoints.json'.format(goal)
    return url, params

def post_data(auth_token, goal, value, comment):
    import requests
    import json
    url, params = build_post_data(auth_token, goal, value, comment)
    data = requests.post(url, params).text
    output = json.loads(data.decode('utf-8'))
    print(output)
    return output
