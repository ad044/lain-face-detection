import requests

import urllib.request

# links from https://github.com/J-Yash/Hotdog-Not-Hotdog/blob/master/GetData.py
links = [
#    'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n01318894',
#    'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n03405725',
#    'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152',
#    'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00021265',
#    'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07690019',
    'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07697537']

for link in links:
    r = requests.get(link, timeout=5)
    for line in r.text.splitlines():
        print(line)
        try:
            urllib.request.urlretrieve(line, line[-10:])
        except:
            pass
