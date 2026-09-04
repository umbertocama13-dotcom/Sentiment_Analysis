# Questi unit test testano unicamente le funzioni dentro metrics_service.py


from unittest.mock import MagicMock

import app.services.metrics_service as metrics_service

# Test the record_request function
def test_record_request(monkeypatch):
    fake_metric = MagicMock()
    fake_child = MagicMock()
    fake_metric.labels.return_value = fake_child

    monkeypatch.setattr(metrics_service, "REQUESTS_TOTAL", fake_metric)

    metrics_service.record_request("/predict", "200")

    fake_metric.labels.assert_called_once_with(endpoint="/predict", status_code="200")
    fake_child.inc.assert_called_once()


# Test the record_prediction_error function
def test_record_prediction_error(monkeypatch):
    fake_counter = MagicMock()

    monkeypatch.setattr(metrics_service, "PREDICTION_ERRORS", fake_counter)

    metrics_service.record_prediction_error()

    fake_counter.inc.assert_called_once()


# Test the record_latency function
def test_record_latency(monkeypatch):
    fake_histogram = MagicMock()

    monkeypatch.setattr(metrics_service, "REQUEST_LATENCY", fake_histogram)

    metrics_service.record_latency(0.25)

    fake_histogram.observe.assert_called_once_with(0.25)


# Test the increment_in_progress function
def test_increment_in_progress(monkeypatch):
    fake_gauge = MagicMock()

    monkeypatch.setattr(metrics_service, "REQUESTS_IN_PROGRESS", fake_gauge)

    metrics_service.increment_in_progress()

    fake_gauge.inc.assert_called_once()


# Test the decrement_in_progress function
def test_decrement_in_progress(monkeypatch):
    fake_gauge = MagicMock()

    monkeypatch.setattr(metrics_service, "REQUESTS_IN_PROGRESS", fake_gauge)

    metrics_service.decrement_in_progress()

    fake_gauge.dec.assert_called_once()


# Test the update_system_metrics function
def test_update_system_metrics(monkeypatch):
    fake_process = MagicMock()
    fake_process.cpu_percent.return_value = 12.5
    fake_process.memory_percent.return_value = 33.3

    fake_cpu_gauge = MagicMock()
    fake_memory_gauge = MagicMock()

    monkeypatch.setattr(metrics_service.os, "getpid", lambda: 1234)
    monkeypatch.setattr(metrics_service.psutil, "Process", lambda pid: fake_process)
    monkeypatch.setattr(metrics_service, "CPU_USAGE", fake_cpu_gauge)
    monkeypatch.setattr(metrics_service, "MEMORY_USAGE", fake_memory_gauge)

    metrics_service.update_system_metrics()

    fake_cpu_gauge.set.assert_called_once_with(12.5)
    fake_memory_gauge.set.assert_called_once_with(33.3)


# Test the get_metrics function
def test_get_metrics(monkeypatch):
    fake_generate_latest = MagicMock(return_value=b"fake_metrics")

    monkeypatch.setattr(metrics_service, "update_system_metrics", MagicMock())
    monkeypatch.setattr(metrics_service, "generate_latest", fake_generate_latest)

    result = metrics_service.get_metrics()

    metrics_service.update_system_metrics.assert_called_once()
    fake_generate_latest.assert_called_once()
    assert result == b"fake_metrics"

