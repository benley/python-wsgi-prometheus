#!/usr/bin/env python
"""bottlepy plugin for prometheus metrics."""

import functools

import bottle
import wsgi_prometheus.metrics

Metrics = wsgi_prometheus.metrics.Metrics


class MetricsPlugin(object):
    """Generic Prometheus metrics plugin for BottlePy."""

    name = 'PrometheusMetrics'

    def apply(self, callback, route):
        @Metrics.LatencyHistogram.time()
        @functools.wraps(callback)
        def wrapped_callback(*args, **kwargs):

            Metrics.RequestCounter.labels(
                bottle.request.method,
                bottle.request.get('wsgi.url_scheme')).inc()
            if bottle.request.content_length is not None:
                Metrics.RequestSizeHistogram.observe(
                    bottle.request.content_length)

            body = callback(*args, **kwargs)

            status_code = bottle.response.status_code
            Metrics.ResponseCounter.labels(status_code).inc()

            try:
                content_length = len(body)
                Metrics.ResponseSizeHistogram.observe(content_length)
            except (ValueError, TypeError):
                pass

            return body
        return wrapped_callback
