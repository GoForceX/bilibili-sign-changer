from verify import offline_token, qrlogin, check_token
import requests, time

before_text = '你愿意成为我的第'
after_text = '个粉丝吗？'
follower = -1

if __name__ == '__main__':
    while True:
        time.sleep(30)
        link = "https://api.bilibili.com/x/member/web/sign/update"
        if not check_token.check(offline_token.get_token()['SESSDATA']):
            qrlogin.login()
        token = offline_token.get_token()
        fo_resp = requests.get('https://api.bilibili.com/x/web-interface/nav/stat', cookies=token).json()
        if follower == fo_resp['data']['follower']:
            print(f'当前粉丝数为{follower}，粉丝数未变。')
            continue
        follower = fo_resp['data']['follower']
        change_resp = requests.post(link, cookies=token, data={'user_sign': f'{before_text} {follower + 1} {after_text}', 'csrf': token['bili_jct']}).json()
        if change_resp["code"] == 0:
            print(f'当前粉丝数为{follower}，修改已成功执行。')
    