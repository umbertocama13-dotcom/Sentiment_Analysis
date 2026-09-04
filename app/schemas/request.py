from pydantic import BaseModel, constr

# Controlla che sia un testo e che non sia vuoto
class SentimentRequest(BaseModel):
    text: constr(min_length=1)