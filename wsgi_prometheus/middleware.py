"""Prometheus exporter WSGI middleware."""

import prometheus_client as prom
import werkzeug.wrappers

import wsgi_prometheus.metrics

Metrics = wsgi_prometheus.metrics.Metrics


class MetricsMiddleware(object):
    """WSGI middleware with basic instrumentation."""

    def __init__(self, app):
        self._app = app

    @Metrics.LatencyHistogram.time()
    def __call__(self, environ, start_response):
        request = werkzeug.wrappers.Request(environ)

        Metrics.RequestCounter.labels(request.method, request.scheme).inc()

        content_length = request.content_length
        if content_length is not None:
            Metrics.RequestSizeHistogram.observe(content_length)

        def instrumented_start_response(status, headers, exc_info=None):
            status_code = status.split(None, 1)[0]
            Metrics.ResponseCounter.labels(status_code).inc()
            try:
                content_length = int(dict(headers).get('Content-Length'))
                Metrics.ResponseSizeHistogram.observe(content_length)
            except (ValueError, TypeError):
                pass
            return start_response(status, headers, exc_info)

        response = self._app(environ, instrumented_start_response)
        return response
