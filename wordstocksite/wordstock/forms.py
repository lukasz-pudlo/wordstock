from django import forms
from .models import Wordcollection, Word


class WordcollectionForm(forms.ModelForm):
    class Meta:
        model = Wordcollection
        fields = ['url']


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['source_word', 'target_word']
