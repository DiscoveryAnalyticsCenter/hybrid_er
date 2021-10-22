from django.contrib import admin

from .models import Cluster, Canonical, Candidate, Result, Score


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = ('id', 'cluster')


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'cluster', 'text')
    list_filter = ('cluster',)


@admin.register(Canonical)
class CanonicalAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'cluster', 'user', 'updated')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'vote',
        'text',
        'candidate',
        'user',
        'better_cluster',
        'updated',
    )
    list_filter = ('candidate', 'user', 'better_cluster', 'updated')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'score', 'cluster', 'candidate')
    list_filter = ('cluster', 'candidate')
