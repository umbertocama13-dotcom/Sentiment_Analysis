import time
from fastapi import APIRouter, HTTPException

from app.schemas.request import SentimentRequest
from app.services.check_language import is_english
from app.services.sentiment_service import predict_sentiment
from app.services.metrics_service import (
    increment_in_progress,
    decrement_in_progress,
    record_request,
    record_prediction_error,
    record_latency,
)

router = APIRouter()

@router.post("/predict")
def route_predict_sentiment(request: SentimentRequest):
    
    increment_in_progress()
    start_time = time.time()
    text = request.text

    try:
        if not is_english(text):
            record_request(endpoint="/predict", status_code="400")
            record_prediction_error()
            raise HTTPException(
                status_code=400,
                detail="Il testo deve essere in lingua inglese"
            )

        result = predict_sentiment(text)

        record_request(endpoint="/predict", status_code="200")
        record_latency(duration=time.time() - start_time)

        return result

    except HTTPException:
        raise

    except Exception as e:
        record_request(endpoint="/predict", status_code="500")
        record_prediction_error()
        record_latency(duration=time.time() - start_time)
        raise HTTPException(
            status_code=500,
            detail=f"Errore durante l'analisi del sentiment: {str(e)}"
        )

    finally:
        decrement_in_progress()