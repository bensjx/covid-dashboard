import urllib.request

# url = 'https://data.gov.sg/api/action/datastore_search'
# fileobj = urllib.request.urlopen(url)
# print (fileobj.read())
req = urllib.request.Request("https://data.gov.sg/api/action/datastore_search?resource_id=0e185366-f2a0-489f-bce8-17b4a24ea339&limit=5&q=title:jones", headers={"User-Agent": "Chrome"})
res = urllib.request.urlopen(req)
print(res)
