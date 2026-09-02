from services.mongo_service import MongoService
from services.minio_service import MinioService
from services.audio_service import AudioService
from services.taxonomy_service import TaxonomyService
from services.classification_service import ClassificationService


def main():

    print("============================")
    print("     BIRD DATA PIPELINE")
    print("============================")
    print()

    try:
        mongo = MongoService()
        mongo.ping()

        print("MongoDB OK")

    except Exception as ex:
        print(f"MongoDB error: {ex}")
        return

    try:
        minio = MinioService()

        print("MinIO OK")

    except Exception as ex:
        print(f"MinIO error: {ex}")
        return

    print()
    print("Checking bird taxonomy...")

    try:
        taxonomy_service = TaxonomyService(
            mongo
        )

        taxonomy_service.import_taxonomy()

    except Exception as ex:
        print(f"Taxonomy error: {ex}")
        return

    print()
    print("Processing audio files...")

    audio_service = AudioService(
        mongo,
        minio
    )

    processed_files = (
        audio_service.process_files()
    )

    print()
    print(
        f"Processed files: "
        f"{len(processed_files)}"
    )

    print()
    print("Classifying audio files...")

    classification_service = (
        ClassificationService(mongo)
    )

    for audio in processed_files:

        try:
            classification_service.classify_and_save(
                audio
            )

        except Exception as ex:
            print(
                f"Classification error for "
                f"{audio['file_name']}: {ex}"
            )


if __name__ == "__main__":
    main()