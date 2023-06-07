import functools

import requests

__session_pools__ = {}

RETRY_COUNT = 3

DEFAULT_COOKIE = ""

WEB_SITE = "http://www.huanxiangji.com"

User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"


def set_headers():
    return {
        "User-Agent": User_Agent,
        "Host": WEB_SITE.replace("http://", ""),
        "Origin": WEB_SITE,
        "cookie": DEFAULT_COOKIE,
        "Accept-Encoding": "gzip, deflate",
    }

def max_retry(max_retry_count: int):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for retry_count in range(max_retry_count):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if retry_count >= max_retry_count - 1:
                        raise e
                    else:
                        print(f'Request failed: {str(e)}')

        return wrapper

    return decorator


def request(method: str, url: str, **kwargs) -> requests.Response:
    global __session_pools__
    if not __session_pools__.get("session"):
        __session_pools__["session"] = requests.Session()
    headers = set_headers()
    if method == "post":
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    response = __session_pools__["session"].request(method=method, url=WEB_SITE + url, headers=headers,
                                                    data=kwargs.get("data"), params=kwargs.get("params"))
    response.encoding = 'gbk'
    response.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
    return response


@max_retry(RETRY_COUNT)
def get(url: str, params=None, **kwargs) -> requests.Response:
    return request('get', url, params=params, **kwargs)


@max_retry(RETRY_COUNT)
def post(url: str, data=None, **kwargs) -> requests.Response:
    return request('post', url, data=data, **kwargs)
