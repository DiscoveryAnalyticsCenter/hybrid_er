import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from hybrid_er.entities.models import Result


class Command(BaseCommand):
    """Export results

    Example:
    ./manage.py populate_clusters data/outfile.csv
    """

    help = 'Export results'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        results_count = 0

        with open(options['path'], 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([
                "cluster",
                "candidate",
                "vote",
                "better_cluster",
                "user",
                "updated"
            ])
            for r in Result.objects.all().select_related("candidate", "user", "better_cluster", "candidate__cluster"):
                writer.writerow([
                    r.candidate.cluster.cluster,
                    r.candidate.text,
                    r.vote,
                    r.better_cluster.cluster if r.better_cluster else "",
                    r.user.username,
                    r.updated.isoformat()
                ])
                results_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully wrote {} results to file {}'.format(
                    results_count,
                    options["path"]
                )
            )
        )
