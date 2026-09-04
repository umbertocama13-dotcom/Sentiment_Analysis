from app.services.services_model.model_fasttext import model

# Verifica se il testo è in lingua inglese utilizzando il modello FastText
def is_english(text: str, threshold: float = 0.8) -> bool:
    # pulizia generale del testo: rimuove newline e spazi iniziali/finali
    cleaned_text = text.replace("\n", " ").strip()
    
    # Utilizo di fasttext per predire la lingua del testo con relativa confidenza
    labels, scores = model.predict(cleaned_text, k=1)
    
    # Separazione di label da confidenza
    predicted_label = labels[0]  
    confidence = scores[0]       
    
    # return True se la lingua predetta è inglese e la confidenza supera la soglia, altrimenti False
    if predicted_label == "__label__eng_Latn" and confidence >= threshold:
        return True
    else:
        return False
