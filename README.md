# prometheus_exporter
The basic framework of prometheus exporter by python

# reference
https://prometheus.io/docs/instrumenting/writing_exporters/
https://github.com/prometheus/client_python#custom-collectors


# Four types of metric
# Counter, Gauge, Summary, Histogram

# Counter类型，计数器, 带标签
c = Counter('my_requests_total', 'HTTP Failures', ['method', 'endpoint'])
c.labels(method='get', endpoint='/').inc()
c.labels(method='post', endpoint='/submit').inc()


# Gauge类型，可上下波动, 带标签
g = Gauge('my_inprogress_requests', 'Description of gauge', ['name', 'type'])
g.labels(name='init', type='ready').inc()  # Increment by 1
g.labels(name='init', type='ready').dec(10)  # Decrement by given value
g.labels(type='failed').set(4.2)  # Set to a given value


# Histogram类型，一种累积直方图，它通常用来描述监控项的长尾效应, 带标签
h = Histogram('request_latency_seconds', 'Description of histogram', ['labels1'])
h.observe(4.7)    # Observe 4.7 (seconds in this case)
h.labels(labels1='histogram').observe(4.7)    # Observe 4.7 (seconds in this case)


# Summary类型，Summary 和 Histogram 类似，它记录的是监控项的分位数, 带标签
s = Summary('request_latency_seconds', 'Description of summary', ['labels1', 'labels2'])
s.observe(4.7)    # Observe 4.7 (seconds in this case)


# There are several options for exporting metrics.
# 常见的有： HTTP，Twisted，WSGI，ASGI，Flask
# 方法：
from prometheus_client import start_http_server
start_http_server(8000)
