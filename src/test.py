from threading import Thread
from queue import Queue


class Downloader(Thread):
    def __init__(self, queue, folder):
        Thread.__init__(self)
        self.queue = queue
        self.folder = folder

    def run(self):
        while True:
            url = self.queue.get()
            #print("SALAM")
            self.queue.task_done()


thread_count = 4

queue = Queue()

downloader = Downloader(queue, 'images')
downloader.daemon = True
downloader.start()

for x in range(4):
    queue.put(x)

queue.join()