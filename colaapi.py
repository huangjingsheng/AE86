import requests
import json
class ColaApi():
    def __init__(self):
        headers = {}
        headers['accept'] = 'application/json, text/plain, */*'
        headers['content-type'] = 'application/json;charset=UTF-8'
        headers['origin'] = 'https://mall.huishoubao.com'
        headers['content-length'] = '39'
        headers['accept-language'] = 'zh-cn'
        headers['user-agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 ' \
                                '(KHTML, like Gecko) Mobile/15G77'
        headers['referer'] = 'https://mall.huishoubao.com/index.html'
        headers['accept-encoding'] = 'br, gzip, deflate'
        self.headers = headers
        self.url = {}
    def login(self,parame):
        #r = requests.post(self.url["LoginUrl"],header = self.headers,data = json.dumps(parame))
        r = requests.post(self.url["LoginUrl"], headers=self.headers, json=parame,verify=False)
        return r.text
