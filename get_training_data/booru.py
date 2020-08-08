from __future__ import unicode_literals
from pybooru import Danbooru
from pybooru import Moebooru
from random import randint
import multiprocessing
import multiprocessing.pool
import urllib.request

class NonDaemonPool(multiprocessing.pool.Pool):
    def Process(self, *args, **kwds):
        proc = super(NonDaemonPool, self).Process(*args, **kwds)

        class NonDaemonProcess(proc.__class__):
            @property
            def daemon(self):
                return False

            @daemon.setter
            def daemon(self, val):
                pass

        proc.__class__ = NonDaemonProcess

        return proc

img_urls = []

#konachan, yandere, danbooru
site = ''

#client = Danbooru('danbooru',
#                  username='',
#                  api_key='')

#client = Moebooru('yandere',
#                  username='',
#                  password='')

#client = Moebooru('konachan',
#                  username='',
#                  password='')

def generate_pages(startpage, endpage):
    for i in range(startpage, endpage+1):
        posts = client.post_list(tags='iwakura_lain -nude', page=i, limit=200)
        for post in posts:
            try:
                fileurl = post['file_url']
            except:
                fileurl = 'https://{}.com'.format(site) + post['source']
            img_urls.append(fileurl)

def download_img(img):
    randomint = randint(1, 10000000)
    urllib.request.urlretrieve(img, "{}_{}".format(site, randomint))

def start_workers():
    pool = NonDaemonPool()
    pool.map(download_img, img_urls)
    pool.close()

def main():
    generate_pages(1,17)
    start_workers()

main()
