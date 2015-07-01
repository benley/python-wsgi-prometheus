"""Metric definitions."""

import prometheus_client as prom

from wsgi_prometheus import util

Counter = prom.Counter
Histogram = prom.Histogram


class Metrics(object):
    RequestCounter = Counter(
        'http_requests_total', 'Total number of HTTP requests.',
        ['method', 'scheme'])
    ResponseCounter = Counter(
        'http_responses_total', 'Total number of HTTP responses.',
        ['status'])
    LatencyHistogram = Histogram(
        'http_latency_seconds', 'Overall HTTP transaction latency.')
    RequestSizeHistogram = Histogram(
        'http_requests_body_bytes',
        'Breakdown of HTTP requests by content length.',
        buckets=util.powers_of(2, 30))
    ResponseSizeHistogram = Histogram(
        'http_responses_body_bytes',
        'Breakdown of HTTP responses by content length.',
        buckets=util.powers_of(2, 30))
