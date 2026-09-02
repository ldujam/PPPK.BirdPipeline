from pymongo import MongoClient

from config import MONGO_URI, MONGO_DATABASE


class MongoService:

    def __init__(self):
        self.client = MongoClient(MONGO_URI)

        self.db = self.client[MONGO_DATABASE]

        self.birds = self.db["birds"]
        self.audio_files = self.db["audio_files"]
        self.classifications = self.db["classifications"]

        self._create_indexes()

    def _create_indexes(self):
        self.birds.create_index(
            "key",
            unique=True
        )

        self.audio_files.create_index(
            "object_name",
            unique=True
        )

    def ping(self):
        self.client.admin.command("ping")

    def save_audio_file(self, audio_data):
        result = self.audio_files.insert_one(audio_data)
        return result.inserted_id

    def save_classification(self, classification_data):
        result = self.classifications.insert_one(
            classification_data
        )
        return result.inserted_id

    def upsert_bird(self, bird):
        self.birds.update_one(
            {
                "key": bird["key"]
            },
            {
                "$set": bird
            },
            upsert=True
        )

    def taxonomy_exists(self):
        return self.birds.count_documents({}) > 0


    def get_bird_by_scientific_name(self, scientific_name):
        return self.birds.find_one(
            {
                "scientificName": {
                    "$regex": f"^{scientific_name}",
                    "$options": "i"
                }
            }
        )