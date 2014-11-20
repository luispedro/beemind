from time import time
import re
from config import BEEMIND_DATA_FILE, BEEMIND_GOAL, BEEMIND_AUTH_TOKEN
           
pat = re.compile('^(start|stop): ([0-9]+\.[0-9]+)$')

def parse_files(inputf):
    total = 0
    startp = None
    for line in inputf:
        m = pat.match(line)
        if m is None:
            raise ValueError("Could not parse line {}".format(line))
        code,timestamp = m.groups()
        timestamp = float(timestamp)
        if code == 'start':
            if not startp:
                startp = timestamp
        elif code == 'stop':
            if startp:
                total += timestamp - startp
                startp = False
    if startp:
        total += time() - startp
    return total

def build_post_data(auth_token, goal, value, comment):
    from urllib.parse import urlencode
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

def main(argv):
    now = time()
    if argv[1] == 'start':
        with open(BEEMIND_DATA_FILE, 'a+') as output:
            output.write('start: {}\n'.format(now))
    elif argv[1] == 'stop':
        with open(BEEMIND_DATA_FILE, 'a+') as output:
            output.write('stop: {}\n'.format(now))
    elif argv[1] == 'submit':
        from os import unlink
        total = parse_files(open(BEEMIND_DATA_FILE))
        total /= 3600
        post_data(BEEMIND_AUTH_TOKEN, BEEMIND_GOAL, '{:.4}'.format(total), "from command line")
        unlink(BEEMIND_DATA_FILE)
        

if __name__ == '__main__':
    from sys import argv
    main(argv)
