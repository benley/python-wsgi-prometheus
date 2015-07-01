"""Minimal WSGI app."""

import prometheus_client as prom
import werkzeug.wrappers


@werkzeug.wrappers.Request.application
def wsgi_app(_):
    """wsgi app that can be used for a /metrics endpoint."""
    return werkzeug.wrappers.Response(prom.generate_latest(),
                                      mimetype=prom.CONTENT_TYPE_LATEST)
