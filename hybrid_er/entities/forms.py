from django import forms

from .models import Canonical, Result


class ResultForm(forms.ModelForm):
    # vote = forms.ChoiceField(choices=Result.Vote, widget=forms.RadioSelect())

    class Meta:
        model = Result
        fields = ['candidate', 'vote', 'better_cluster']
        # fields = ['candidate', 'user', 'text', 'vote']

        widgets = {
            "candidate": forms.HiddenInput(),
            "vote": forms.RadioSelect(),
            "better_cluster": forms.RadioSelect()
        }


class CanonicalForm(forms.ModelForm):
    class Meta:
        model = Canonical
        fields = ['candidate']

        widgets = {
            "candidate": forms.RadioSelect(),
        }
