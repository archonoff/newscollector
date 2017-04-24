import stem.process
import requests
from grab import Grab
from stem.control import Controller
from stem import Signal

from stem.util import term

SOCKS_PORT = 9150

def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print(term.format(line, term.Color.BLUE))


print(term.format("Starting Tor:\n", term.Attr.BOLD))
tor_process = stem.process.launch_tor_with_config(
  config = {
    'SocksPort': str(SOCKS_PORT),
    'ExitNodes': '{ru}',
    'ControlPort': str(9051),
    'GeoIPFile': r'C:\Users\Oleg\Desktop\tor-win32-0.2.8.9\Data\Tor\geoip',
    'GeoIPv6File': r'C:\Users\Oleg\Desktop\tor-win32-0.2.8.9\Data\Tor\geoip6',
  },
  init_msg_handler = print_bootstrap_lines,
  tor_cmd = 'C:\\Users\\Oleg\\Desktop\\tor-win32-0.2.8.9\\Tor\\tor.exe',
)


print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))

# Через requests
# print(term.format(query("https://www.atagar.com/echo.php"), term.Color.BLUE))
# print(query("http://ya.ru"))
# proxies = {
#     'http': 'socks5://127.0.0.1:{}'.format(SOCKS_PORT),
#     'https': 'socks5://127.0.0.1:{}'.format(SOCKS_PORT)
# }
# resp = requests.get('http://icanhazip.com/', proxies=proxies)
# print(resp.headers)
# print(resp.content)

# Через Grab
g = Grab(proxy='127.0.0.1:{}'.format(SOCKS_PORT), proxy_type='socks5', timeout=90, connect_timeout=30)
c = Controller.from_port()
c.authenticate()
for i in range(10):
    g.go('http://icanhazip.com/')
    print(i)
    print(g.doc.head)
    print(g.doc.body)
    print()
    c.signal(Signal.NEWNYM)

tor_process.kill()  # stops tor