import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.logging_config import setup_logging, LOG_FILE
from app.routes.predict import router as predict_router
from app.routes.metrics import router as metrics_router
from app.services.sentiment_service import load_model
 

# Ingloba tutta la fastAPI permettendo lo unittest su "startup_event" senza side effects
# (altrimenti il logger e il caricamento del modello verrebbero eseguiti al momento dell'importazione)
def create_app() -> FastAPI:
    load_dotenv()
 
    # Inizializzazione logger
    logger = setup_logging()
    logger.info("Logging inizializzato correttamente.")
    logger.info(f"File di log: {LOG_FILE}")
 
    # Creazione app FastAPI
    app = FastAPI()
 
    # Inclusione router
    app.include_router(predict_router)
    app.include_router(metrics_router)
 
    # Caricamento modello Sentiment Analysis
    @app.on_event("startup")
    def startup_event():
        try:
            model_path = os.getenv("MODEL_PATH")
            load_model(model_path)
            logger.info("Modello di Sentiment analysis caricato correttamente.")
        except Exception as e:
            logger.error(f"Errore durante il caricamento del modello: {str(e)}")
 
    return app
 
 
# Entry point reale usato da uvicorn
app = create_app()