from bs4 import BeautifulSoup
import multiprocessing
import multiprocessing.pool
import requests
import sys
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


sys.setrecursionlimit(25000)

site = "https://www.zerochan.net"
r = requests.get('{}/Serial+Experiments+Lain'.format(site))
soup = BeautifulSoup(r.content)

anchor_list = []
page_count = 1


def populate_anchor_list(source):
    global last_entry
    main_container = source.find_all('ul', {'id': 'thumbs2'})
    for elem in main_container:
        for li in elem.find_all('li'):
            anchor = li.find('a')['href']
            anchor_list.append(anchor)
    last_entry = anchor_list[-1]


def img_download_worker(anchor):
    global page_count
    if anchor == last_entry:
        page_count += 1
        r = requests.get('{}/Serial+Experiments+Lain?p={}'.format(site, page_count))
        soup = BeautifulSoup(r.content)
        populate_anchor_list(soup)
        start_workers()
    try:
        post_soup = BeautifulSoup(requests.get(site + anchor).content)
        post_preview = post_soup.find('a', {'class': 'preview'})
        post_img = post_preview.find('img')['src']
        urllib.request.urlretrieve(post_img, 'zerochan_{}'.format(anchor[-4:]))
    except:
        # pass "member-only" posts
        pass


def start_workers():
    pool = NonDaemonPool()
    pool.map(img_download_worker, anchor_list)
    pool.close()


def main():
    populate_anchor_list(soup)
    start_workers()


main()
