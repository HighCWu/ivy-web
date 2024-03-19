import os
import glob
import json
import time
import threading
import webbrowser

CUR_DIR = os.path.abspath(os.path.dirname(__file__))


def _strip(line):
    return line.split(" ")[0].split("#")[0].split(",")[0].split("\r\n")[0].split("\n")[0]

files = sorted(glob.glob(f'{CUR_DIR}/ivy_web/**/*.py', recursive=True))
files = [os.path.relpath(path, CUR_DIR).replace('\\', '/') for path in files]

with open(f'{CUR_DIR}/../ivy/requirements/requirements.txt', "r", encoding="utf-8") as f:
    packages = [
        _strip(line)
        for line in f if _strip(line) not in ['psutil', 'nvidia-ml-py'] and 'ml-dtypes' not in line
    ]

template = rf'''
packages = {json.dumps(packages, indent=4, ensure_ascii=False)}

[[fetch]]
    files = {json.dumps(files, indent=4, ensure_ascii=False)}
'''

with open(f'{CUR_DIR}/pyscript.dev.toml', 'w', encoding='utf-8') as f:
    f.write(template)


# create a dev server

from http import server

class DevHTTPRequestHandler(server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=CUR_DIR, **kwargs)

    def end_headers(self):
        self.send_my_headers()

        server.SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")

def open_browser(url):
    time.sleep(1)
    webbrowser.open(url, new=2)

def run(server_class=server.HTTPServer, handler_class=DevHTTPRequestHandler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    url = 'http://localhost:8080/index.dev.html'
    print(f'Dev server run on {url}')
    t = threading.Thread(target=open_browser, args=(url,))
    t.start()
    httpd.serve_forever()
    t.join()

if __name__ == '__main__':
    run()
