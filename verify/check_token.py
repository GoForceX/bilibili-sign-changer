import requests

def check(sessdata):
    resp = requests.get(
        'https://api.bilibili.com/x/space/notice?mid=1',
        cookies={'SESSDATA': sessdata}
    )
    if resp.json()['code'] != 0:
        return False
    return True