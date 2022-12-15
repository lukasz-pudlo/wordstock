from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Wordcollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    url = models.URLField()
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-id", ]

    def get_absolute_url(self):
        return reverse('wordstock:wordcollection_detail', args=[self.id])


class Word(models.Model):
    wordcollection = models.ForeignKey(
        Wordcollection, on_delete=models.CASCADE, related_name='words')
    source_word = models.CharField(max_length=100, blank=True)
    target_word = models.CharField(max_length=100, blank=True)

    def get_absolute_url(self):
        return reverse('wordstock:word_detail', args=[self.id])

# Subsequent entries in the results list of the API.


class Synonym(models.Model):
    word = models.ForeignKey(
        Word, on_delete=models.CASCADE, related_name='synonyms')
    source_synonym = models.CharField(max_length=100, blank=True)
    target_synonym = models.CharField(max_length=100, blank=True)

    def get_absolute_url(self):
        return reverse('wordstock:synonym_detail', args=[self.id])


class Example(models.Model):
    synonym = models.ForeignKey(
        Synonym, on_delete=models.CASCADE, related_name='examples')
    source_example = models.CharField(max_length=500, blank=True)
    target_example = models.CharField(max_length=500, blank=True)
