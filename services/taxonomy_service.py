import requests

from config import TAXONOMY_URL


class TaxonomyService:

    def __init__(self, mongo_service):
        self.mongo = mongo_service

    def import_taxonomy(self):

        if self.mongo.taxonomy_exists():
            print(
                "Taxonomy already exists in MongoDB. "
                "Skipping import."
            )
            return

        print("Downloading bird taxonomy...")

        response = requests.get(
            TAXONOMY_URL,
            timeout=60
        )

        response.raise_for_status()

        birds = response.json()

        print(
            f"Downloaded {len(birds)} bird records."
        )

        inserted = 0

        for bird in birds:

            if "key" not in bird:
                continue

            self.mongo.upsert_bird(bird)

            inserted += 1

        print(
            f"Stored {inserted} bird records in MongoDB."
        )