import pytest
from fastapi.testclient import TestClient

from app.main import app
import app.routes.predict as sentiment_route

client = TestClient(app)


################################################
## Test per il modulo predict.py

### Test per la funzione route_predict_sentiment: esito positivo
def test_predict_success(monkeypatch):
    called = {
        "predict_sentiment": False,
        "decrement_in_progress": False,
    }

    # Simula la funzione is_english per restituire True
    def fake_is_english(text):
        return True

    # Simula la funzione predict_sentiment per restituire un risultato fittizio
    def fake_predict_sentiment(text):
        called["predict_sentiment"] = True
        return "positive"

    # Simula le funzioni di metrics_service per non fare nulla
    def fake_increment_in_progress():
        pass

    # Simula la funzione decrement_in_progress per registrare che è stata chiamata
    def fake_decrement_in_progress():
        called["decrement_in_progress"] = True

    # Simula le funzioni di metrics_service per non fare nulla
    def fake_record_request(endpoint, status_code):
        pass

    # Simula le funzioni di metrics_service per non fare nulla
    def fake_record_prediction_error():
        pass

    # Simula le funzioni di metrics_service per non fare nulla
    def fake_record_latency(duration):
        pass

    # monckeypatch delle funzioni nel modulo sentiment_route: sostituisce le funzioni reali con quelle fittizie
    monkeypatch.setattr(sentiment_route, "is_english", fake_is_english)
    monkeypatch.setattr(sentiment_route, "predict_sentiment", fake_predict_sentiment)
    monkeypatch.setattr(sentiment_route, "increment_in_progress", fake_increment_in_progress)
    monkeypatch.setattr(sentiment_route, "decrement_in_progress", fake_decrement_in_progress)
    monkeypatch.setattr(sentiment_route, "record_request", fake_record_request)
    monkeypatch.setattr(sentiment_route, "record_prediction_error", fake_record_prediction_error)
    monkeypatch.setattr(sentiment_route, "record_latency", fake_record_latency)

    response = client.post("/predict", json={"text": "I love this product"})

    # Verifica che la risposta sia corretta e che le funzioni siano state chiamate come previsto
    assert response.status_code == 200
    assert response.json() == "positive"
    assert called["predict_sentiment"] is True
    assert called["decrement_in_progress"] is True


### Test per la funzione route_predict_sentiment: testo non in inglese
def test_predict_not_english(monkeypatch):
    called = {
        "predict_sentiment": False,
        "decrement_in_progress": False,
        "record_request": False,
        "record_prediction_error": False,
    }

    # Simula la funzione is_english per restituire False
    def fake_is_english(text):
        return False

    # Simula la funzione predict_sentiment per restituire un risultato fittizio
    def fake_predict_sentiment(text):
        called["predict_sentiment"] = True
        return "positive"

    # Simula le funzioni di metrics_service per non fare nulla
    def fake_increment_in_progress():
        pass

    # Simula la funzione decrement_in_progress per registrare che è stata chiamata
    def fake_decrement_in_progress():
        called["decrement_in_progress"] = True

    # Simula le funzioni di metrics_service per non fare nulla
    def fake_record_request(endpoint, status_code):
        called["record_request"] = True
        assert endpoint == "/predict"
        assert status_code == "400"

    # Simula le funzioni di metrics_service per non fare nulla
    def fake_record_prediction_error():
        called["record_prediction_error"] = True

    # Simula le funzioni di metrics_service per non fare nulla
    def fake_record_latency(duration):
        pass

    # monckeypatch delle funzioni nel modulo sentiment_route: sostituisce le funzioni reali con quelle fittizie
    monkeypatch.setattr(sentiment_route, "is_english", fake_is_english)
    monkeypatch.setattr(sentiment_route, "predict_sentiment", fake_predict_sentiment)
    monkeypatch.setattr(sentiment_route, "increment_in_progress", fake_increment_in_progress)
    monkeypatch.setattr(sentiment_route, "decrement_in_progress", fake_decrement_in_progress)
    monkeypatch.setattr(sentiment_route, "record_request", fake_record_request)
    monkeypatch.setattr(sentiment_route, "record_prediction_error", fake_record_prediction_error)
    monkeypatch.setattr(sentiment_route, "record_latency", fake_record_latency)

    response = client.post("/predict", json={"text": "Questo testo non è inglese"})

    # Verifica che la risposta sia corretta e che le funzioni siano state chiamate come previsto
    assert response.status_code == 400
    assert response.json()["detail"] == "Il testo deve essere in lingua inglese"
    assert called["predict_sentiment"] is False
    assert called["record_request"] is True
    assert called["record_prediction_error"] is True
    assert called["decrement_in_progress"] is True


# Test per la funzione route_predict_sentiment: errore interno del modello
def test_predict_internal_error(monkeypatch):
    called = {
        "predict_sentiment": False,
        "decrement_in_progress": False,
        "record_request": False,
        "record_prediction_error": False,
        "record_latency": False,
    }

    # Simula la funzione is_english per restituire True
    def fake_is_english(text):
        return True

    # Simula la funzione predict_sentiment per sollevare un'eccezione
    def fake_predict_sentiment(text):
        called["predict_sentiment"] = True
        raise Exception("errore del modello")

    # Simula le funzioni di metrics_service per non fare nulla
    def fake_increment_in_progress():
        pass

    # Simula la funzione decrement_in_progress per registrare che è stata chiamata
    def fake_decrement_in_progress():
        called["decrement_in_progress"] = True

    # Simula le funzioni di metrics_service per non fare nulla
    def fake_record_request(endpoint, status_code):
        called["record_request"] = True
        assert endpoint == "/predict"
        assert status_code == "500"

    # Simula le funzioni di metrics_service per non fare nulla
    def fake_record_prediction_error():
        called["record_prediction_error"] = True

    # Simula le funzioni di metrics_service per non fare nulla
    def fake_record_latency(duration):
        called["record_latency"] = True

    # monckeypatch delle funzioni nel modulo sentiment_route: sostituisce le funzioni reali con quelle fittizie
    monkeypatch.setattr(sentiment_route, "is_english", fake_is_english)
    monkeypatch.setattr(sentiment_route, "predict_sentiment", fake_predict_sentiment)
    monkeypatch.setattr(sentiment_route, "increment_in_progress", fake_increment_in_progress)
    monkeypatch.setattr(sentiment_route, "decrement_in_progress", fake_decrement_in_progress)
    monkeypatch.setattr(sentiment_route, "record_request", fake_record_request)
    monkeypatch.setattr(sentiment_route, "record_prediction_error", fake_record_prediction_error)
    monkeypatch.setattr(sentiment_route, "record_latency", fake_record_latency)

    response = client.post("/predict", json={"text": "I love this product"})

    # Verifica che la risposta sia corretta e che le funzioni siano state chiamate come previsto
    assert response.status_code == 500
    assert "Errore durante l'analisi del sentiment" in response.json()["detail"]
    assert called["predict_sentiment"] is True
    assert called["decrement_in_progress"] is True
    assert called["record_request"] is True
    assert called["record_prediction_error"] is True
    assert called["record_latency"] is True



################################################
## Test per il modulo metrics.py

import app.routes.metrics as metrics_route
from prometheus_client import CONTENT_TYPE_LATEST


# Test per la funzione metrics: esito positivo
def test_metrics_success(monkeypatch):
    def fake_get_metrics():
        return "metriche simulate"

    monkeypatch.setattr(metrics_route, "get_metrics", fake_get_metrics)

    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.text == "metriche simulate"
    assert response.headers["content-type"] == CONTENT_TYPE_LATEST


# Test per la funzione metrics: errore interno
def test_metrics_error(monkeypatch):
    def fake_get_metrics():
        raise Exception("errore nel recupero")

    monkeypatch.setattr(metrics_route, "get_metrics", fake_get_metrics)

    response = client.get("/metrics")

    assert response.status_code == 500
    assert response.json()["detail"] == "Errore nel recupero delle metriche"