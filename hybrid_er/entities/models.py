from django.conf import settings
from django.db import models


class Cluster(models.Model):

    cluster = models.IntegerField()
    text = models.TextField(blank=True)

    class Meta:
        verbose_name = "Cluster"
        verbose_name_plural = "Clusters"

    def __str__(self):
        return "{}".format(self.cluster)


class Candidate(models.Model):

    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"

    def __str__(self):
        return "{}".format(self.text)


class Result(models.Model):

    class Vote(models.TextChoices):
        YES = 'Y', 'Yes'
        NO = 'N', 'No'
        IDK = 'U', 'Unknown'

    vote = models.CharField(
        max_length=1,
        choices=Vote.choices,
        default=Vote.YES,
    )
    text = models.TextField()

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    better_cluster = models.ForeignKey(Cluster, null=True, blank=True, on_delete=models.DO_NOTHING)

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "Results"

    def __str__(self):
        return "({}) {} {}".format(self.user, self.candidate, self.vote)


class Score(models.Model):
    score = models.FloatField()
    cluster = models.ForeignKey(Cluster, on_delete=models.DO_NOTHING)
    candidate = models.ForeignKey(Candidate, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Score"
        verbose_name_plural = "Scores"

    def __str__(self):
        return "({} -> {}) {}".format(self.candidate, self.cluster, self.score)


class Canonical(models.Model):
    cluster = models.ForeignKey(Cluster, on_delete=models.DO_NOTHING)
    candidate = models.ForeignKey(Candidate, on_delete=models.DO_NOTHING)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
