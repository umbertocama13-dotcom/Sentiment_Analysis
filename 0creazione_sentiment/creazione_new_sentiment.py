import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle
import sys


# 1. Caricamento
df = pd.read_csv("dataset.csv")

# Check delle label
#print(df["label"].unique())

# 1.1 Accorciamento del database
df = df.sample(n=7000, random_state=42)

# 1.2 Cambio da 1 a "negative" e da 2 a "positive" 
df["label"] = df["label"].map({1: "negative", 2: "positive"})

# 2. Scelta colonne
X = df["review"]
y = df["label"]

# 2.1 controllo 
#print(df["label"].value_counts())
#print(df.head())
# stop per controllo
#sys.exit("Stop qui per controllo")

# 3. Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 4. Pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression(max_iter=1000))
])

# 5. Training
model.fit(X_train, y_train)

# 6. Valutazione
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 7. Salvataggio
with open("new_sentiment_analysis.pkl", "wb") as f:
    pickle.dump(model, f)