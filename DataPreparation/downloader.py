import os

Lux = "./lux"
Cookie = "./cookies"
com = [Lux, "-c", Cookie]


def proxy_setup():
    # Proxy Setup
    os.environ['https_proxy'] = '127.0.0.1:7890'
    os.environ['http_proxy'] = '127.0.0.1:7891'


def download(url: str, playlist: bool = False, threads: int = 10, proxy: bool = False, path: str = None, name: str = None):
    global com

    cmd = com
    if name:
        cmd.append('-O')
        cmd.append(name)

    if path:
        cmd.append('-o')
        cmd.append(path)

    if playlist:
        cmd.append('-p')

    cmd.append('-n')
    cmd.append(str(threads))

    cmd.append(url)

    if proxy:
        proxy_setup()

    cmd = ' '.join(cmd)
    r = os.popen(cmd)
    text = r.read()
    r.close()
    ll = text.split('\n')
    title = ll[-2]
    title = title[title.rfind("/")+1:title.rfind(".mp4")+4]
    return title


