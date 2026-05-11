from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import JsonResponse
from django.core.cache import cache
from django.db import connection
from elasticsearch import Elasticsearch
from django.conf import settings


def health_check(request):
    # Check all 4 services: Database, Elasticsearch, Celery, and Redis
    # Return 503 if any service is down, otherwise return 200
    status = {}

    # Check Database
    try:
        connection.ensure_connection()
        status["postgres"] = "ok"
    except Exception as e:
        status["postgres"] = f"error: {str(e)}"

    # Check redis
    try:
        cache.set("health_check", "ok", timeout=5)
        val = cache.get("health_check")
        status["redis"] = "ok" if val == "ok" else "error: unable to set/get cache"
    except Exception as e:
        status["redis"] = f"error: {str(e)}"
    
    # Check Elasticsearch
    try:
        es = Elasticsearch(settings.ELASTICSEARCH_DSL["default"]["hosts"])
        info = es.cluster.health()
        status["elasticsearch"] = "ok" if info["status"] in ["green", "yellow"] else f"error: cluster status {info['status']}"
    except Exception as e:
        status["elasticsearch"] = f"error: {str(e)}"

    # Check Celery
    try:
        from celery import Celery
        app = Celery()
        app.conf.broker_url = settings.CELERY_BROKER_URL
        app.conf.result_backend = settings.CELERY_RESULT_BACKEND
        app.control.ping(timeout=1)
        status["celery"] = "ok"
    except Exception as e:
        status["celery"] = f"error: {str(e)}"

    all_ok = all (
        "ok" in str(v) or "green" in str(v) or "yellow" in str(v)
        for v in status.values()
    )

    return JsonResponse(
        {"status": "healthy" if all_ok else "degraded", 
         "services": status},
        status=200 if all_ok else 503,
    )

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.users.urls")),
    path("health/", health_check, name="health_check"),
]

