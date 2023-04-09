import os

Lux = "./lux"
Cookie = "./cookies"
com = [Lux, "-c", Cookie, '-o', './download']

def proxy_setup():
    # Proxy Setup
    os.environ['https_proxy'] = '127.0.0.1:7890'
    os.environ['http_proxy'] = '127.0.0.1:7891'



def download(url: str, playlist: bool = False, threads: int = 10):
    global com
    if playlist:
        com.append('-p')

    com.append('-n')
    com.append(str(threads))

    com.append(url)

    proxy_setup()

    com = ' '.join(com)
    os.system(com)


download("https://www.bilibili.com/video/BV1et411t7Cm", False, 10)
