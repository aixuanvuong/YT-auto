import urllib.request
import urllib.parse
import json

query = urllib.parse.quote("Android Auto app not showing in launcher Unknown sources")
url = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={query}&site=stackoverflow"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req).read()
    data = json.loads(response)
    for item in data.get('items', [])[:3]:
        print(item['title'], item['link'])
except Exception as e:
    print(e)
