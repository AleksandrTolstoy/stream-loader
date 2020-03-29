#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import logging

import threading
from queue import Queue

import os
import urllib.request


class Downloader(threading.Thread):
    """Stream file downloader"""

    def __init__(self, number: int, queue: Queue):
        threading.Thread.__init__(self)
        self.number = number
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()
            logging.info(f'Thread {self.number}: %s', f'got URL - {url}')
            self.download_file(url)
            self.queue.task_done()

    def download_file(self, url: str):
        handle = urllib.request.urlopen(url)
        file_name = os.path.basename(url)
        logging.info(f'Thread {self.number}: %s', f'starts to downloading file: {file_name}')
        with open(file_name, 'wb') as f:
            while True:
                chunk = handle.read(1024)
                if not chunk:
                    logging.info(f'Thread {self.number}: %s', f'file {file_name} was downloaded')
                    break
                f.write(chunk)


def main(urls):
    queue = Queue()

    for number in range(len(urls)):
        t = Downloader(number, queue)
        t.setDaemon(True)
        t.start()

    for url in urls:
        queue.put(url)

    # waiting for the completion of the queue
    queue.join()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

    urls = ['http://www.irs.gov/pub/irs-pdf/f1040.pdf',
            'https://www.irs.gov/pub/irs-prior/f1040a--2015.pdf',
            'https://www.irs.gov/pub/irs-prior/i1040a--2015.pdf',
            'https://www.irs.gov/pub/irs-prior/i1040a--2016.pdf',
            'https://www.irs.gov/pub/irs-prior/i1040a--2017.pdf']

    main(urls)
