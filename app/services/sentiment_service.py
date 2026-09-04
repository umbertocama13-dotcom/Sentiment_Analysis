import pickle

model = None

# Caricamento del modello FastText per l'analisi del sentiment
def load_model(model_path: str):
    global model
    with open(model_path, "rb") as f:
        model = pickle.load(f)


# Funzione per analizzare il sentiment del testo
def predict_sentiment(text: str):
    if model is None:
        raise RuntimeError("Model not loaded")
    
    prediction = model.predict([text])
    return prediction[0]