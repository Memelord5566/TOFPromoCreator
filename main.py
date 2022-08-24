# We 💓 Floppa

import os, sys, time, json, random, string, hashlib, ctypes; from threading import Thread, Lock, active_count

try:
    import requests
except ModuleNotFoundError:
    os.system('pip install requests >nul')

try:
    import user_agent
except ModuleNotFoundError:
    os.system('pip install user-agent >nul')


start_time = time.time()
colors = {'white': '\x1b[0m', 'red': '\x1b[1;31m', 'cyan': '\x1b[1;36m', 'yellow': '\x1b[1;33m'}

config = json.load(open("Config/Config.json", encoding="UTF-8"))


def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name in ('ce', 'nt', 'dos'):
        os.system('cls')
    else:
        for _ in range(120): print('\n')


def update_title(title):
    if os.name in ('ce', 'nt', 'dos'):
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        print('\33]0;%s\a' % title, end='', flush=True)


lock = Lock()


def print_function(color, text_in_brackets, text):
    lock.acquire()
    sys.stdout.flush()
    print(' %s[%s%s%s] %s' % (colors['white'], color, text_in_brackets, colors['white'], text))
    lock.release()


def read_file(filename, method):
    try:
        if os.stat(filename).st_size != 0:
            with open(filename, method, encoding='UTF-8') as f: return [line.rstrip('\n') for line in f]
        else:
            print_function(colors['red'], 'ERROR', '%s IS EMPTY' % filename)
            input(); exit()
    except FileNotFoundError:
        print_function(colors['red'], 'ERROR', 'FILE: %s NOT FOUND' % filename)


def parse(text, first, last):
    try:
        return text.split(first)[1].split(last)[0]
    except Exception as error:
        return error


def total_count(file):
    return len(read_file(r'%s' % file, 'r'))


def get_proxy():
    proxy_file = read_file('Config/Proxies.txt', 'r')
    proxies = {}

    if config["Proxies"]["Use Proxies"] is True:

        proxy = random.choice(proxy_file)
        if config["Proxies"]["Proxy Type"] == "http":
            proxies = {
                "http": "http://{}".format(proxy),
                "https": "http://{}".format(proxy)
            }
        elif config["Proxies"]["Proxy Type"] == "socks4":
            proxies = {
                "http:": "socks4://{}".format(proxy),
                "https:": "socks4://{}".format(proxy)
            }
        elif config["Proxies"]["Proxy Type"] == "socks5":
            proxies = {
                "http:": "socks5://{}".format(proxy),
                "https:": "socks5://{}".format(proxy)
            }

        return proxies


clear()
update_title("[ToF Gen]")

print('''
 ToF Gen
''')


class ToF:
    def __init__(self):

        self.generated = 0
        self.promos = 0
        self.failed = 0
        self.retries = 0
        self.total = 0
        self.session = requests.Session()

    def set_title(self):
        while True:
            update_title('[ToF Gen] | Generated: {}/{} ({}%) | Time Elapsed: {} | Promos: {} | Failed: {} | Retries: {} | Threads: {}'.format(self.generated, config["Config"]["Amount To Generate"], 100 * float(self.total) / float(config["Config"]["Amount To Generate"]), time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time)), self.promos, self.failed, self.retries, active_count() - 1))
            time.sleep(0.4)

    def get_sig(self, endpoint, payload):
        sig = '/account/%s?account_plat_type=113&app_id=a0ca7921668f7d18c096ad85011589fd&lang_type=en&os=3&source=32%s0d88135dd851f81f9601e477b261a137' % (endpoint, payload)
        return str(hashlib.md5(sig.encode()).hexdigest())
    
    def get_code(self, email_username, email_domain):

        try:

            time.sleep(3)

            checking_email_headers = {
                    "Accept": "*/*",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-N950F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.126 Mobile Safari/537.36",
                    "Connection": "keep-alive",
                    "Accept-Encoding": "gzip, deflate, br"
            }

            checking_email_request = self.session.get('https://www.1secmail.com/api/v1/?action=getMessages&login=%s&domain=%s' % (email_username, email_domain), headers=checking_email_headers)
            if '[]' not in checking_email_request.text:
                email_id = checking_email_request.json()[0]['id']

                fetching_email_headers = {
                    "Accept": "*/*",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-N950F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.126 Mobile Safari/537.36",
                    "Connection": "keep-alive",
                    "Accept-Encoding": "gzip, deflate, br"
                }

                fetching_email_request = self.session.get('https://www.1secmail.com/api/v1/?action=readMessage&login=%s&domain=%s&id=%s' % (email_username, email_domain, email_id), headers=fetching_email_headers)
                return parse(fetching_email_request.text, 'Hello, here is your verification code, it is valid for\\n300 seconds: *           ', '           You are receiving this')

        except Exception as error:
            print_function(colors['red'], 'FAILED TO VERIFY', error)

    def get_info(self, token, openid, expire):

        try:

            info_headers = {
                'User-Agent': user_agent.generate_user_agent(),
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Content-Type': 'application/json',
                'Origin': 'https://www.toweroffantasy-global.com',
                'Connection': 'keep-alive',
                'Referer': 'https://www.toweroffantasy-global.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site'
            }

            info_payload = '{"device_info":{"guest_id":null,"lang_type":"en","app_version":"0.1","screen_height":1080,"screen_width":1920,"device_brand":"","device_model":"5.0 (Windows)","ram_total":0,"rom_total":0,"cpu_name":"Win32","android_imei":"","ios_idfa":""},"channel_dis":"00000000","channel_info":{"token":"%s","openid":"%s","account_plat_type":113}}' % (token, openid)

            sig = '/v2/auth/login?channelid=113&conn=0&gameid=29093&os=5&sdk_version=2.0&seq=&source=32&ts=1660585139617%s0d88135dd851f81f9601e477b261a137' % str(info_payload)
            sig = str(hashlib.md5(sig.encode()).hexdigest())

            if config["Proxies"]["Use Proxies"] is True:
                info = self.session.post('https://aws-na.intlgame.com/v2/auth/login?channelid=113&conn=0&gameid=29093&os=5&sdk_version=2.0&seq=&sig=%s&source=32&ts=1660585139617' % sig, headers=info_headers, proxies=get_proxy(), data=info_payload)
            else:
                info = self.session.post('https://aws-na.intlgame.com/v2/auth/login?channelid=113&conn=0&gameid=29093&os=5&sdk_version=2.0&seq=&sig=%s&source=32&ts=1660585139617' % sig, headers=info_headers, data=info_payload)

            _openid = info.json()['openid']
            _token = info.json()['token']

            _info_payload = {
                "mappid": 10109,
                "clienttype": 903,
                "login_info": {
                    "game_id": "29093",
                    "open_id": _openid,
                    "token": _token,
                    "channel_id": 113,
                    "channel_info": "{\"account_plat_type\":113,\"expire_ts\":%s,\"token\":\"%s\"}" % (expire, token)
                }
            }

            if config["Proxies"]["Use Proxies"] is True:
                _info = self.session.post('https://na-community.playerinfinite.com/api/trpc/trpc.wegame_app_global.auth_svr.AuthSvr/LoginByINTL', headers=info_headers, proxies=get_proxy(), json=_info_payload)
            else:
                _info = self.session.post('https://na-community.playerinfinite.com/api/trpc/trpc.wegame_app_global.auth_svr.AuthSvr/LoginByINTL', headers=info_headers, json=_info_payload)
            
            return _info.json()['data']['user_info']['user_id'], _info.json()['data']['wt']
        
        except Exception as error:
            self.retries += 1
            print_function(colors['red'], 'GET INFO', error)

    def claim_promo(self, uid, token):

        attempts = 0

        try:

            promo_headers = {
                'Host': 'www.jupiterlauncher.com',
                'User-Agent': user_agent.generate_user_agent(),
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Content-Type': 'application/json',
                'Origin': 'https://www.toweroffantasy-global.com',
                'Connection': 'keep-alive',
                'Referer': 'https://www.toweroffantasy-global.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site'
            }

            promo_payload = {
                "cookies": "uid=%s;ticket=%s" % (uid, token)
            }

            if config["Proxies"]["Use Proxies"] is True:
                promo = self.session.post('https://www.jupiterlauncher.com/api/v1/fleet.platform.game.GameCommunity/ObtainCdkey', headers=promo_headers, proxies=get_proxy(), json=promo_payload)
            else:
                promo = self.session.post('https://www.jupiterlauncher.com/api/v1/fleet.platform.game.GameCommunity/ObtainCdkey', headers=promo_headers, json=promo_payload)

            while 'transaction handle error' in promo.text and attempts <= 3:

                time.sleep(1.5)

                if config["Proxies"]["Use Proxies"] is True:
                    promo = self.session.post('https://www.jupiterlauncher.com/api/v1/fleet.platform.game.GameCommunity/ObtainCdkey', headers=promo_headers, proxies=get_proxy(), json=promo_payload)
                else:
                    promo = self.session.post('https://www.jupiterlauncher.com/api/v1/fleet.platform.game.GameCommunity/ObtainCdkey', headers=promo_headers, json=promo_payload)
                
                attempts += 1

            if '"error_code":0' in promo.text:

                return promo.json()['cdkey']
        
        except Exception as error:
            self.retries += 1
            print_function(colors['red'], 'PROMO', error)

    def generate(self):

        try:

            email = 'f' + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8)) + '@' + random.choice(['1secmail.com', '1secmail.org', '1secmail.net', 'wwjmp.com', 'esiix.com', 'oosln.com', 'vddaz.com', 'bheps.com', 'dcctb.com'])
            password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16)) + '0$F'

            send_code_headers = {
                'Host': 'aws-na-pass.intlgame.com',
                'User-Agent': user_agent.generate_user_agent(),
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Content-Type': 'application/json;charset=utf-8',
                'Origin': 'https://www.toweroffantasy-global.com',
                'Connection': 'keep-alive',
                'Referer': 'https://www.toweroffantasy-global.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'TE': 'Trailers'
            }

            send_code_payload = '{"account":"%s","account_type":1,"code_type":0}' % email

            if config["Proxies"]["Use Proxies"] is True:
                send_code = self.session.post('https://aws-na-pass.intlgame.com/account/sendcode?account_plat_type=113&app_id=a0ca7921668f7d18c096ad85011589fd&lang_type=en&os=3&sig=%s&source=32' % self.get_sig('sendcode', str(send_code_payload)), headers=send_code_headers, proxies=get_proxy(), data=send_code_payload)
            else:
                send_code = self.session.post('https://aws-na-pass.intlgame.com/account/sendcode?account_plat_type=113&app_id=a0ca7921668f7d18c096ad85011589fd&lang_type=en&os=3&sig=%s&source=32' % self.get_sig('sendcode', str(send_code_payload)), headers=send_code_headers, data=send_code_payload)
            
            if '"msg":"Success"' in send_code.text:

                code = self.get_code(email.split('@')[0], email.split('@')[1])
                
                register_headers = {
                    'Host': 'aws-na-pass.intlgame.com',
                    'User-Agent': user_agent.generate_user_agent(),
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Content-Type': 'application/json;charset=utf-8',
                    'Origin': 'https://www.toweroffantasy-global.com',
                    'Connection': 'keep-alive',
                    'Referer': 'https://www.toweroffantasy-global.com/',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'cross-site',
                    'TE': 'Trailers'
                }

                register_payload = '{"verify_code":"%s","account":"%s","account_type":1,"password":"%s"}' % (code, email, str(hashlib.md5(password.encode()).hexdigest()))

                if config["Proxies"]["Use Proxies"] is True:
                    register = self.session.post('https://aws-na-pass.intlgame.com/account/register?account_plat_type=113&app_id=a0ca7921668f7d18c096ad85011589fd&lang_type=en&os=3&sig=%s&source=32' % self.get_sig('register', str(register_payload)), headers=register_headers, proxies=get_proxy(), data=register_payload)
                else:
                    register = self.session.post('https://aws-na-pass.intlgame.com/account/register?account_plat_type=113&app_id=a0ca7921668f7d18c096ad85011589fd&lang_type=en&os=3&sig=%s&source=32' % self.get_sig('register', str(register_payload)), headers=register_headers, data=register_payload)

                if register.status_code == 200 and 'token' in register.text:
                    
                    uid, token = self.get_info(register.json()['token'], register.json()['uid'], register.json()['expire'])
                    promo = self.claim_promo(uid, token)

                    self.total += 1
                    self.generated += 1

                    if promo == "":

                        print_function(colors['cyan'], 'GENERATED', '%s:%s' % (email, password))
                        with open('Config/Results/Unclaimed.txt', 'a', encoding='UTF-8') as f: f.write('%s:%s\n' % (email, password))

                    else:

                        self.promos += 1

                        print_function(colors['cyan'], 'GENERATED', promo)
                        with open('Config/Results/Generated.txt', 'a', encoding='UTF-8') as f: f.write('%s:%s:%s\n' % (email, password, promo))
                        with open('Config/Results/Promos.txt', 'a', encoding='UTF-8') as f: f.write(str(promo) + '\n')

                else:
                    self.failed += 1
                    print_function(colors['red'], register.status_code, register.text)
                
            else:
                self.failed += 1
                print_function(colors['red'], send_code.status_code, send_code.text)

        except Exception as error:
            self.retries += 1
            print_function(colors['red'], 'FAILED', error)

    def start(self):
        Thread(target=self.set_title, daemon=True).start()
        threads = []
        for _ in range(config["Config"]["Amount To Generate"]):
            run = True

            while run:
                if active_count() <= config["Config"]["Threads"]:
                    thread = Thread(target=self.generate)
                    threads.append(thread)
                    thread.start()
                    run = False

        for x in threads:
            x.join()

        print('')
        print_function(colors['cyan'], '!', 'PROCESS FINISHED. GENERATED %s%s/%s%s ACCOUNTS, %s%s/%s%s PROMOS.' % (colors['cyan'], self.generated, config["Config"]["Amount To Generate"], colors['white'], colors['cyan'], self.promos, self.generated, colors['white']))
        input(); exit()


if __name__ == '__main__':
    ToF().start()
