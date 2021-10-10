import os

def get_token():
    if os.path.exists('token.txt'):
        with open('token.txt', 'r') as file:
            sess, jct = file.read().split('\n')
            return {'SESSDATA': sess, 'bili_jct': jct}
    else:
        return {}