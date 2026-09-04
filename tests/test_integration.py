from fastapi.testclient import TestClient
import app.main as main

# Test the /predict endpoint with valid text
def test_predict_valid_text(monkeypatch):
    monkeypatch.setattr("app.routes.predict.is_english", lambda text: True)
    monkeypatch.setattr("app.routes.predict.predict_sentiment", lambda text: ["positive"])
    monkeypatch.setattr("app.routes.predict.increment_in_progress", lambda: None)
    monkeypatch.setattr("app.routes.predict.decrement_in_progress", lambda: None)
    monkeypatch.setattr("app.routes.predict.record_request", lambda endpoint, status_code: None)
    monkeypatch.setattr("app.routes.predict.record_latency", lambda duration: None)

    app = main.create_app()
    client = TestClient(app)

    response = client.post("/predict", json={"text": "This is a great movie"})

    assert response.status_code == 200
    assert response.json() == ["positive"]


# Test the /predict endpoint with non-English text
def test_predict_non_english_text(monkeypatch):
    monkeypatch.setattr("app.routes.predict.is_english", lambda text: False)
    monkeypatch.setattr("app.routes.predict.increment_in_progress", lambda: None)
    monkeypatch.setattr("app.routes.predict.decrement_in_progress", lambda: None)
    monkeypatch.setattr("app.routes.predict.record_request", lambda endpoint, status_code: None)
    monkeypatch.setattr("app.routes.predict.record_prediction_error", lambda: None)

    app = main.create_app()
    client = TestClient(app)

    response = client.post("/predict", json={"text": "Ciao come stai"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Il testo deve essere in lingua inglese"}


# Test the /metrics endpoint
def test_get_metrics(monkeypatch):
    monkeypatch.setattr("app.routes.metrics.get_metrics", lambda: b"fake_metrics_output")

    app = main.create_app()
    client = TestClient(app)

    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.content == b"fake_metrics_output"
    assert response.headers["content-type"].startswith("text/plain")


# Test the /predict endpoint with missing text
def test_predict_missing_text(monkeypatch):
    monkeypatch.setattr("app.routes.predict.is_english", lambda text: True)
    monkeypatch.setattr("app.routes.predict.predict_sentiment", lambda text: ["positive"])
    monkeypatch.setattr("app.routes.predict.increment_in_progress", lambda: None)
    monkeypatch.setattr("app.routes.predict.decrement_in_progress", lambda: None)
    monkeypatch.setattr("app.routes.predict.record_request", lambda endpoint, status_code: None)
    monkeypatch.setattr("app.routes.predict.record_latency", lambda duration: None)

    app = main.create_app()
    client = TestClient(app)

    response = client.post("/predict", json={})

    assert response.status_code == 422