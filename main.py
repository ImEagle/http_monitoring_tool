# encoding: utf-8
from __future__ import unicode_literals

import asyncio
import json
import logging

import requests
from requests import RequestException

logging.basicConfig(filename='log.log', level=logging.INFO)


class PeriodicVerify(object):
    def __init__(self, url, content=None, delay=None):
        self._url = url
        self._content = content
        self._delay = delay

        self._loop = asyncio.get_event_loop()

    def check_site(self):
        try:
            response = requests.get(self._url)
        except RequestException as e:
            logging.info(e)
            return

        is_valid_content = True

        if self._content:
            if self._content not in str(response.content):
                is_valid_content = False

        log_msg = "{url} {response_code} {elapsed_sec} Content valid: {is_valid_content}".format(
            url=self._url,
            response_code=response.status_code,
            is_valid_content=is_valid_content,
            elapsed_sec=response.elapsed.total_seconds()
        )

        logging.info(log_msg)

    def _run(self):
        self.check_site()

        if self._delay:
            self._loop.call_later(self._delay, self._run)

    @asyncio.coroutine
    def run(self):
        self._run()


@asyncio.coroutine
def main():
    config_json = open('config.json').read()
    config = json.loads(config_json)

    interval = config['interval']
    urls = config['urls']

    for index, url_data in enumerate(urls):
        pv = PeriodicVerify(url_data['url'], url_data.get('content'), interval)
        yield from pv.run()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
