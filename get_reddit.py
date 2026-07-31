import urllib.request
import json
import urllib.parse

query = urllib.parse.quote("Android auto unknown sources app not showing real car site:reddit.com")
url = f"https://duckduckgo.com/html/?q={query}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req).read().decode('utf-8')
    import re
    urls = set(re.findall(r'href="([^"]+)"', response))
    for u in urls:
        if 'reddit.com' in u:
            print(u)
except Exception as e:
    pass
