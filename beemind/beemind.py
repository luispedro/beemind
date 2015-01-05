def build_post_data(auth_token, goal, value, comment):
    from urllib.parse import urlencode
    from time import time
    post_data = {
            'auth_token': auth_token,
            'timestamp': round(time()),
            'value': value,
            'comment': comment,
            }
    params = urlencode(post_data).encode('utf-8')
    url = 'https://www.beeminder.com/api/v1/users/me/goals/{}/datapoints.json'.format(goal)
    return url, params

def post_data(auth_token, goal, value, comment):
    from urllib.request import urlopen
    import json
    url, params = build_post_data(auth_token, goal, value, comment)
    data = urlopen(url, params).readall()
    output = json.loads(data.decode('utf-8'))
    print(output)
    return output
