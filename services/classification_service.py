import os
from datetime import datetime, timezone

import requests

from config import CLASSIFICATION_URL


class ClassificationService:

    def __init__(self, mongo_service):
        self.mongo = mongo_service

    def classify(self, file_path):

        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                f"Audio file not found: {file_path}"
            )

        print(
            f"Sending '{os.path.basename(file_path)}' "
            f"to classification API..."
        )

        with open(file_path, "rb") as audio_file:

            files = {
                "file": (
                    os.path.basename(file_path),
                    audio_file
                )
            }

            response = requests.post(
                CLASSIFICATION_URL,
                files=files,
                timeout=120
            )

        print(
            f"Classification API status: "
            f"{response.status_code}"
        )

        if not response.ok:
            print(response.text)
            response.raise_for_status()

        return response.json()

        

    def classify_and_save(self, audio):

        response = self.classify(
            audio["file_path"]
        )

        results = response.get("results", [])

        if not results:
            print(
                f"No birds detected in "
                f"{audio['file_name']}."
            )
            return

        for result in results:

            scientific_name = result.get(
                "scientific_name"
            )

            bird = (
                self.mongo
                .get_bird_by_scientific_name(
                    scientific_name
                )
            )

            if bird is None:
                print(
                    f"Bird '{scientific_name}' "
                    f"not found in taxonomy."
                )
                continue

            classification_document = {

                "audio_file_id":
                    audio["audio_id"],

                "bird_id":
                    bird["_id"],

                "bird_key":
                    bird["key"],

                "scientific_name":
                    scientific_name,

                "common_name":
                    result.get("common_name"),

                "confidence":
                    result.get("confidence"),

                "start_time":
                    result.get("start_time"),

                "end_time":
                    result.get("end_time"),

                "label":
                    result.get("label"),

                "classified_at":
                    datetime.now(timezone.utc)
            }

            self.mongo.save_classification(
                classification_document
            )

            print(
                f"Classification stored: "
                f"{scientific_name} "
                f"({result.get('confidence'):.2%})"
            )