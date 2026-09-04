from fastapi import APIRouter, Response, HTTPException
from prometheus_client import CONTENT_TYPE_LATEST
from app.services.metrics_service import get_metrics

router = APIRouter()

@router.get("/metrics")
def metrics():
    try:
        return Response(
            content=get_metrics(),
            media_type=CONTENT_TYPE_LATEST
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Errore nel recupero delle metriche")