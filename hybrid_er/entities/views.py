import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Cluster, Candidate, Canonical, Result, Score
from .forms import CanonicalForm, ResultForm



class ClusterDetailView(LoginRequiredMixin, DetailView):

    model = Cluster
    slug_field = "cluster"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        formset = context["formset"]
        canon_form = context["canon_form"]

        if formset.is_valid():
            formset.save(commit=False)
            for instance in formset.new_objects:
                instance.user = request.user
            formset.save()

            if canon_form.is_valid():
                instance = canon_form.save(commit=False)
                instance.user = request.user
                instance.cluster = self.object
                instance.save()
        else:
            print(formset.errors)

        return HttpResponseRedirect(reverse("entities:detail", kwargs={"slug": self.object.cluster}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        candidates = list(self.object.candidate_set.all())

        new_one = not Result.objects.filter(
            user=self.request.user,
            candidate__cluster=self.object
        ).exists()

        initials = []
        if new_one:
            initials = [{
                "candidate": candidate.pk,
                "user": self.request.user,
            } for candidate in candidates]

        cf_kwargs = {}
        try:
            old_canon = Canonical.objects.get(
                user=self.request.user,
                cluster=self.object
            )
            cf_kwargs["instance"] = old_canon
        except Canonical.DoesNotExist:
            pass

        if self.request.POST:
            ResultFormSet = modelformset_factory(
                Result,
                form=ResultForm,
                extra=len(initials)
            )

            formset = ResultFormSet(
                self.request.POST,
                queryset=Result.objects.filter(
                    user=self.request.user,
                    candidate__cluster=self.object
                )
            )
            canon_form = CanonicalForm(self.request.POST, **cf_kwargs)
        else:
            ResultFormSet = modelformset_factory(
                Result,
                form=ResultForm,
                extra=len(initials)
            )

            formset = ResultFormSet(
                initial=initials,
                queryset=Result.objects.filter(
                    user=self.request.user,
                    candidate__cluster=self.object
                )
            )
            canon_form = CanonicalForm(**cf_kwargs)

        canon_form.fields["candidate"].queryset = (
            Candidate.objects.filter(
                cluster=self.object)
        )

        ctx_candidates = []
        for i, form in enumerate(formset):
            form.fields["better_cluster"].queryset = Cluster.objects.filter(
                score__candidate=candidates[i]).order_by("-score__score")

            ctx_candidates.append({
                "candidate": candidates[i],
                "form": form,
                "clusters": Score.objects.filter(candidate=candidates[i]).order_by("-score"),
            })
        context["candidates"] = ctx_candidates
        context["formset"] = formset
        context["canon_form"] = canon_form
        return context


class ClusterListView(LoginRequiredMixin, ListView):

    model = Cluster

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset.filter(user=self.request.user)
        return queryset

    # paginate_by = 100  # if pagination is desired

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context
