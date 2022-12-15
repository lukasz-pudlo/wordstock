from rest_framework import serializers
from wordstock.models import Wordcollection, Word, Synonym, Example

from django.utils.html import escape


class ExampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Example
        fields = '__all__'


class SynonymSerializer(serializers.ModelSerializer):
    # examples = ExampleSerializer(many=True)

    class Meta:
        model = Synonym
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    # synonyms = SynonymSerializer(many=True)

    class Meta:
        model = Word
        fields = '__all__'


class WordcollectionSerializer(serializers.ModelSerializer):
    # words = WordSerializer(many=True)

    class Meta:
        model = Wordcollection
        fields = '__all__'
