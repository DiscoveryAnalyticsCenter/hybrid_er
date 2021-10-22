import csv
import json
import pandas as pd

from django.conf import settings
from django.core.management.base import BaseCommand

from hybrid_er.entities.models import Cluster, Candidate


class Command(BaseCommand):
    """Populates database of entity clusters and candidates

    Example:
    ./manage.py populate_clusters data/clusters.json
    """

    help = 'Populate database of entity clusters and candidates'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        cluster_count = 0
        candidate_count = 0

        with open(options['path']) as cluster_file:
            data = json.load(cluster_file)
            df = pd.DataFrame.from_records([
                    [k, v] for k, v in data.items()
                ],
                columns=["text", "cluster"]
            )

            for cluster_number in set(data.values()):
                cluster = Cluster.objects.create(
                    cluster=cluster_number,
                    text=", ".join(df[df["cluster"] == cluster_number].text.to_list())
                )
                cluster_count += 1

                for text in df[df["cluster"] == cluster_number].text:
                    Candidate.objects.create(
                        cluster=cluster,
                        text=text
                    )
                    candidate_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully populated {} clusters and {} entities from file {}'.format(
                    cluster_count,
                    candidate_count,
                    options["path"]
                )
            )
        )
