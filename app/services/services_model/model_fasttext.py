from huggingface_hub import hf_hub_download
import fasttext

# import del modello da huggingface
model_path = hf_hub_download(
    repo_id="facebook/fasttext-language-identification",
    filename="model.bin"
)

# definizione di model come variabile globale
model = fasttext.load_model(model_path)
