from time import time, sleep
import re
from config import BEEMIND_DATA_FILE, BEEMIND_AUTH_TOKEN
           
pat = re.compile(r'^(start|stop) \[(\w+)\]: ([0-9]+\.[0-9]+)$')

def parse_files(inputf):
    from collections import defaultdict
    total = defaultdict(float)
    startp = {}
    for line in inputf:
        m = pat.match(line)
        if m is None:
            raise ValueError("Could not parse line {}".format(line))
        code,goal,timestamp = m.groups()
        timestamp = float(timestamp)
        if code == 'start':
            if goal not in startp:
                startp[goal] = timestamp
        elif code == 'stop':
            if goal in startp:
                total[goal] += timestamp - startp[goal]
                del startp[goal]
    for k,v in startp.items():
        total[k] += time() - v
    return dict(total)

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

def fsync_all(fnames):
    import os
    for f in fnames:
        fd = None
        try:
            fd = os.open(f, os.O_RDONLY)
            os.fsync(fd)
        finally:
            if fd is not None:
                os.close(fd)

def remove_goal_data(inputf, target):
    from os import rename
    with open(inputf) as orig:
        with open(inputf + '.tmp', 'w') as tmp_file:
            for line in orig:
                _,goal,_ = pat.match(line).groups()
                if goal != target:
                    tmp_file.write(line)
    fsync_all([inputf + '.tmp'])
    rename(inputf + '.tmp', inputf)

def usage():
    print("beemind GOAL start")
    print("beemind GOAL stop")
    print("beemind GOAL submit")
    print("beemind GOAL status")

def main(argv):
    now = time()
    goal = argv[1]
    action = argv[2]
    if action == 'start':
        with open(BEEMIND_DATA_FILE, 'a+') as output:
            output.write('start [{}]: {}\n'.format(goal, now))
    elif action == 'stop':
        with open(BEEMIND_DATA_FILE, 'a+') as output:
            output.write('stop [{}]: {}\n'.format(goal, now))
    elif action == 'status':
        total = parse_files(open(BEEMIND_DATA_FILE))
        for k,tm in total.items():
            tm /= 3600.
            print('{:16}\t{:.3}'.format(k,tm))
    elif action == 'submit':
        total = parse_files(open(BEEMIND_DATA_FILE))
        if goal not in total:
            print("Nothing to do.")
            return
        total = total[goal]
        total /= 3600
        print("Submitting {:.4}... (2 seconds to cancel)".format(total))
        sleep(2)
        post_data(BEEMIND_AUTH_TOKEN, goal, '{:.4}'.format(total), "from command line")
        remove_goal_data(BEEMIND_DATA_FILE, goal)
    else:
        from sys import stderr
        stderr.write("Unknown sub-command: {}\n".format(action))
        usage()

if __name__ == '__main__':
    from sys import argv
    main(argv)
