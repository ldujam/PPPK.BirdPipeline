import os
import uuid

from minio import Minio

from config import (
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_BUCKET
)


class MinioService:

    def __init__(self):
        self.client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False
        )

        self.bucket_name = MINIO_BUCKET

        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):

        if not self.client.bucket_exists(
            self.bucket_name
        ):
            self.client.make_bucket(
                self.bucket_name
            )

    def upload_file(self, file_path):

        extension = os.path.splitext(file_path)[1]

        object_name = (
            f"{uuid.uuid4()}{extension}"
        )

        self.client.fput_object(
            self.bucket_name,
            object_name,
            file_path
        )

        return object_name

    def file_exists(self, object_name):

        try:
            self.client.stat_object(
                self.bucket_name,
                object_name
            )

            return True

        except Exception:
            return False


    def download_file(self, object_name, destination_path):
        self.client.fget_object(
            self.bucket_name,
            object_name,
            destination_path
        )