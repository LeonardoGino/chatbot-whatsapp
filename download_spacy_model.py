import spacy
import subprocess

def download_model():
    try:
        subprocess.run(["python", "-m", "spacy", "download", "es_core_news_sm"], check=True)
        print("Modelo de spaCy descargado exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al descargar el modelo de spaCy: {e}")

if __name__ == "__main__":
    download_model()
