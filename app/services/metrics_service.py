from prometheus_client import Counter, Histogram, Gauge, generate_latest
import psutil
import os

# Metriche applicative
REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Tempo di risposta delle richieste"
)

PREDICTION_ERRORS = Counter(
    "prediction_errors_total",
    "Numero totale di errori di predizione"
)

REQUESTS_TOTAL = Counter(
    "requests_total",
    "Numero totale di richieste",
    ["endpoint", "status_code"]
)

REQUESTS_IN_PROGRESS = Gauge(
    "requests_in_progress",
    "Numero di richieste in corso"
)

# Metriche di sistema
CPU_USAGE = Gauge(
    "cpu_usage_percent",
    "Utilizzo CPU in percentuale"
)

MEMORY_USAGE = Gauge(
    "memory_usage_percent",
    "Utilizzo memoria in percentuale"
)


def record_request(endpoint: str, status_code: str):
    REQUESTS_TOTAL.labels(endpoint=endpoint, status_code=status_code).inc()


def record_prediction_error():
    PREDICTION_ERRORS.inc()


def record_latency(duration: float):
    REQUEST_LATENCY.observe(duration)


def increment_in_progress():
    REQUESTS_IN_PROGRESS.inc()


def decrement_in_progress():
    REQUESTS_IN_PROGRESS.dec()


def update_system_metrics():
    process = psutil.Process(os.getpid())
    CPU_USAGE.set(process.cpu_percent())
    MEMORY_USAGE.set(process.memory_percent())


def get_metrics():
    update_system_metrics()
    return generate_latest()