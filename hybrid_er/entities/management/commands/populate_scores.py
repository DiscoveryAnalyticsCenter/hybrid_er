import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from hybrid_er.entities.models import Cluster, Candidate, Score


class Command(BaseCommand):
    """Populates database of entity clusters and candidates

    Example:
    ./manage.py populate_clusters data/clusters.json
    """

    help = 'Populate database of scores'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        cluster_db = {}
        candidate_db = {}
        score_count = 0

        with open(options['path']) as score_file:
            reader = csv.reader(score_file)
            for candidate, cluster_member, score in reader:
                if cluster_member not in cluster_db:
                    try:
                        cluster_db[cluster_member] = Candidate.objects.get(text=cluster_member).cluster
                    except Candidate.DoesNotExist:
                        continue

                if candidate not in candidate_db:
                    try:
                        candidate_db[candidate] = Candidate.objects.get(text=candidate)
                    except Candidate.DoesNotExist:
                        print("Don't have this candidate {}".format(candidate))

                score_count += 1
                Score.objects.create(
                    cluster=cluster_db[cluster_member],
                    candidate=candidate_db[candidate],
                    score=score
                )

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully populated {} scores from file {}'.format(
                    score_count,
                    options["path"]
                )
            )
        )
