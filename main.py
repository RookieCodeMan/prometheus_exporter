# coding: utf-8
# 需求：对公网IP监控，检查其情况(状态码，响应时间)
import time

import requests
import threading
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import start_http_server

url_http_code = Gauge("url_http_code", "request http_code of the url", ['url'])
url_http_request_time = Gauge("url_http_request_time", "request http_request_time of the url", ['code', 'url'])
http_request_total = Counter("http_request_total", "request request total of the url", ['code', 'url'])

MONITOR_WEB_SITES = ['https://www.bilibili.com/',
                     'https://www.baidu.com/',
                     'https://github.com/',
                     'https://www.google.com/',
                     'https://github.com/RookieCodeMan/prometheus_exporter_']


def monitor_web_site_condition(url):
    try:
        r = requests.get(url, timeout=5)
        return r.status_code, r.elapsed.microseconds
    except Exception:
        return '500', -1


def create_metric(url):
    while True:
        http_status, resp_time = monitor_web_site_condition(url)
        url_http_code.labels(url=url).set(http_status)
        url_http_request_time.labels(code=http_status, url=url).set(resp_time)
        http_request_total.labels(code=http_status, url=url).inc()
        time.sleep(5)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8018)
    threads = []
    for url in MONITOR_WEB_SITES:
        threads.append(threading.Thread(target=create_metric, args=(url,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
