# NOTA: I test sono configurati per utilizzare il modulo `monkeypatch` di pytest 
#       per sostituire il modello reale con un modello finto durante i test.


################################################
## Test per il modulo check_language.py

import app.services.check_language as module_to_test

class FakeModelEnglish:
    def predict(self, text, k=1):
        return (["__label__eng_Latn"], [0.85])


def test_is_english_true(monkeypatch):

    fake_model = FakeModelEnglish()
    monkeypatch.setattr(module_to_test, "model", fake_model)

    result = module_to_test.is_english("Hello world, this is a test sentence.")

    assert result is True


class FakeModelNonEnglish:
    def predict(self, text, k=1):
        return (["__label__ita_Latn"], [0.99])

def test_is_english_false(monkeypatch):

    fake_model = FakeModelNonEnglish()
    monkeypatch.setattr(module_to_test, "model", fake_model)

    result = module_to_test.is_english("Ciao mondo, questa è una frase di test.")

    assert result is False



#################################################
## Test per il modulo sentiment_service.py

# IMPORTANTE
# Controllare quale modello viene caricato e adattare il test di conseguenza
# IMPORTANTE


import app.services.sentiment_service as sentiment

# Finto modello che simula model.predict(texts)
class FakeModel:
    def __init__(self, result):
        self._result = result

    def predict(self, texts):
        return [self._result]


# Test per la funzione predict_sentiment: esito positivo
def test_predict_positive_sentiment(monkeypatch):
    monkeypatch.setattr(sentiment, "model", FakeModel("positive"))
    result = sentiment.predict_sentiment("I love this product")
    assert result == "positive"

# Test per la funzione predict_sentiment: esito negativo
def test_predict_negative_sentiment(monkeypatch):
    monkeypatch.setattr(sentiment, "model", FakeModel("negative"))
    result = sentiment.predict_sentiment("I hate this product")
    assert result == "negative"

# Test per la funzione predict_sentiment: esito neutro
def test_predict_neutral_sentiment(monkeypatch):
    monkeypatch.setattr(sentiment, "model", FakeModel("neutral"))
    result = sentiment.predict_sentiment("This is a neutral statement.")
    assert result == "neutral"


# Test per il caso in cui il modello non è ancora stato caricato
def test_predict_sentiment_raises_if_model_not_loaded(monkeypatch):
    monkeypatch.setattr(sentiment, "model", None)

    import pytest
    with pytest.raises(RuntimeError, match="Model not loaded"):
        sentiment.predict_sentiment("qualsiasi testo")



#################################################
## Test per il modulo main.py

from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import importlib

# Test che verifica che lo startup event chiami correttamente la funzione load_model con il path corretto
def test_startup_event_calls_load_model(monkeypatch):
    # 1) imposto la variabile d'ambiente usata dallo startup
    monkeypatch.setenv("MODEL_PATH", "/tmp/fake_model.pkl")

    # 2) preparo un logger finto
    fake_logger = MagicMock()

    # 3) patcho prima dell'import le dipendenze usate in create_app()
    with patch("app.logging_config.setup_logging", return_value=fake_logger), \
         patch("app.services.sentiment_service.load_model") as mock_load_model:

        # 4) importo il modulo solo dopo i patch
        import app.main as main
        importlib.reload(main)

        # 5) creo il client, così parte lo startup event
        with TestClient(main.app):
            pass

    # 6) verifico che il modello sia stato caricato con il path corretto
    mock_load_model.assert_called_once_with("/tmp/fake_model.pkl")

    # 7) verifico il log di successo
    fake_logger.info.assert_any_call("Modello di Sentiment analysis caricato correttamente.")


# Test che verifica che lo startup event logghi un errore se il caricamento del modello fallisce
def test_startup_event_logs_error_when_load_model_fails(monkeypatch):
    monkeypatch.setenv("MODEL_PATH", "/tmp/fake_model.pkl")
    fake_logger = MagicMock()

    with patch("app.logging_config.setup_logging", return_value=fake_logger), \
         patch("app.services.sentiment_service.load_model", side_effect=Exception("model load failed")):

        import app.main as main
        importlib.reload(main)

        with TestClient(main.app):
            pass

    fake_logger.error.assert_any_call(
        "Errore durante il caricamento del modello: model load failed"
    )


# Test che verifica che i router siano inclusi correttamente nell'app FastAPI
def test_routers_are_included(monkeypatch):
    fake_logger = MagicMock()

    with patch("app.logging_config.setup_logging", return_value=fake_logger), \
         patch("app.services.sentiment_service.load_model"):

        import app.main as main
        importlib.reload(main)

        paths = main.app.openapi()["paths"].keys()

    assert "/predict" in paths
    assert "/metrics" in paths



