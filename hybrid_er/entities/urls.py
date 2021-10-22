from django.urls import path

from hybrid_er.entities.views import (
    ClusterDetailView,
    ClusterListView,
)

app_name = "entities"
urlpatterns = [
    path("detail/<int:slug>", view=ClusterDetailView.as_view(), name="detail"),
    path("list/", view=ClusterListView.as_view(), name="list"),
]
