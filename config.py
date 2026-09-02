import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

CLASSIFICATION_URL = os.getenv("CLASSIFICATION_URL")
TAXONOMY_URL = os.getenv("TAXONOMY_URL")

AUDIO_DIRECTORY = "data/audio"

LOCATION = {
    "latitude": 45.8150,
    "longitude": 15.9819
}