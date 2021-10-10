import requests
import json
import time
import qrcode
import io
import qrcode_terminal as qt
from PIL import Image, ImageTk
import threading

headers = ''
img = ''

def init():
    response = requests.get('http://passport.bilibili.com/qrcode/getLoginUrl')
    data = json.loads(response.content)['data']
    url = data['url']
    oauthkey = data['oauthKey']

    f = io.StringIO()
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.border = 2
    qr.print_ascii(invert=True, out=f)

    f.seek(0)

    return {'img': f.read(), 'oauth': oauthkey}

def check(oauthkey):
    global headers
    oauth = ''.join(oauthkey)
    postdata = {
        'oauthKey': oauth
    }
    verify = requests.post('http://passport.bilibili.com/qrcode/getLoginInfo', data=postdata)
    vdata = json.loads(verify.content)
    while vdata['status'] == False:
        time.sleep(1)
        verify = requests.post('http://passport.bilibili.com/qrcode/getLoginInfo', data=postdata)
        vdata = json.loads(verify.content)
    headers = verify.headers

def login():
    global img
    d = init()
    img = d['img']
    oauth = d['oauth']
    print(img)
    check(oauth)
    cookies = headers['Set-Cookie'].split(';')
    sessdata = ''
    jct = ''
    for c in cookies:
        if 'SESSDATA' in c:
            sessdata = c.split('SESSDATA=')[1].replace('%2C', ',')
        if 'bili_jct' in c:
            jct = c.split('bili_jct=')[1]
    with open('token.txt', 'w') as file:
        file.write(sessdata + "\n" + jct)
    # return {'sess': sessdata, 'bili_jct': jct}
