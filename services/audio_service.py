import os

from datetime import datetime, timezone

from config import (
    AUDIO_DIRECTORY,
    LOCATION
)


class AudioService:

    def __init__(
        self,
        mongo_service,
        minio_service
    ):
        self.mongo = mongo_service
        self.minio = minio_service

    def process_files(self):

        if not os.path.exists(
            AUDIO_DIRECTORY
        ):
            print(
                f"Directory does not exist: "
                f"{AUDIO_DIRECTORY}"
            )
            return []

        processed_files = []

        for file_name in os.listdir(
            AUDIO_DIRECTORY
        ):

            file_path = os.path.join(
                AUDIO_DIRECTORY,
                file_name
            )

            if not os.path.isfile(file_path):
                continue

            print()
            print(f"Processing: {file_name}")

            object_name = (
                self.minio.upload_file(
                    file_path
                )
            )

            audio_document = {

                "file_name": file_name,

                "object_name": object_name,

                "bucket":
                    self.minio.bucket_name,

                "location": {
                    "latitude":
                        LOCATION["latitude"],

                    "longitude":
                        LOCATION["longitude"]
                },

                "uploaded_at":
                    datetime.now(timezone.utc)
            }

            audio_id = (
                self.mongo.save_audio_file(
                    audio_document
                )
            )

            processed_files.append(
                {
                    "audio_id": audio_id,
                    "file_name": file_name,
                    "file_path": file_path,
                    "object_name": object_name
                }
            )

            print(
                f"Uploaded to MinIO: "
                f"{object_name}"
            )

            print(
                f"Metadata stored in MongoDB."
            )

        return processed_files