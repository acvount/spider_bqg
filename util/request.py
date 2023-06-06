import requests
import chardet
import threading
from fake_useragent import UserAgent
from util.color_log import Log
from util.proxy.proxy_lib import *


class Request:
    def __init__(self, headers=None, proxy: Proxy = None, ip_cache=None):
        self.log = Log()
        self._add_new_user_agent()
        self.proxy = proxy
        self.headers = headers if headers is not None else {}
        self.ip_cache = [] if ip_cache is None else ip_cache
        self.lock = threading.Lock()

    def _add_new_user_agent(self):
        self.headers['User-Agent'] = UserAgent().random

    def _check_ip_cache(self):
        if not self.ip_cache:
            with self.lock:  # 加锁
                if not self.ip_cache: self.ip_cache += self.proxy.dynamic_ips()

    def get_request(self, url, encoding=None, params=None, proxy=None):
        if params is None:
            params = {}
        try:
            with requests.Session() as session:
                session.headers = self.headers
                response = session.get(url, params=params, proxies=proxy)
                response.raise_for_status()
                if encoding is not None:
                    encoding = chardet.detect(response.content)['encoding']
                response.encoding = encoding
                return response
        except requests.HTTPError as e:
            if response and response.status_code == 403:
                return response
            elif response and response.status_code == 503:
                return self.get_request(url, encoding, params=params, proxy=proxy)
            else:
                self.log.error(f'HTTP error code: {e.response.status_code}')
        except requests.RequestException as e:
            self.log.error(str(e))
        return None

    def get_request_by_dynamic_proxy(self, url, encoding=None, params=None):
        response = None
        self._check_ip_cache()
        with self.lock:  # 加锁
            if self.ip_cache:
                proxies = {'https': f'https://{self.ip_cache[0]}'}
                try:
                    response = self.get_request(url, encoding, params, proxies)
                except requests.HTTPError as e:
                    if response and response.status_code == 403:
                        self.ip_cache.pop(0)
                        self.log.info('Retrying with a new IP...')
                        return self.get_request_by_dynamic_proxy(url, encoding, params)
                    else:
                        self.log.error(f'HTTP error code: {e.response.status_code}')
        return response
