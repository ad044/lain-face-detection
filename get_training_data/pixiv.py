from pathlib import Path
from pixivapi import Client
from pixivapi import Size
import multiprocessing
import multiprocessing.pool

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

client = Client()
client.login('', '')

current_dir = Path.cwd()
last_offset = 300

def get_illustrations(offset=0):
    global last_entry
    global last_offset
    json_res = client.search_illustrations('serial experiments lain', offset=offset)
    last_entry = json_res['illustrations'][-1].title
    last_offset += 30
    return json_res

def download_worker(illust):
    print(last_offset)
    if illust.title == last_entry:
        print(last_offset)
        start_workers(get_illustrations(last_offset))
    illust.download(directory=current_dir, size=Size.ORIGINAL)

def start_workers(illust_list):
    pool = NonDaemonPool()
    pool.map(download_worker, illust_list['illustrations'])
    pool.close()

def main():
    start_workers(get_illustrations(300))

main()
