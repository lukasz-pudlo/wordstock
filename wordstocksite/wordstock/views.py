from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.decorators import login_required
from .models import Wordcollection, Word, Synonym, Example
from .forms import WordcollectionForm

from wordstock.helper import *
from .tasks import createWordcollectionModels

from django.http import JsonResponse

import json

from rest_api.serializers import ExampleSerializer

from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import UserRegistrationForm


@login_required
def create_wordcollection(request):
    # Obtain a list of current articles on the main page of Deutschlandfunk
    articles_titles_and_links = create_list_of_articles()

    if request.method == 'GET':
        print(request.user)

        return render(request, 'create_wordcollection.html', {'form': WordcollectionForm(), 'articles_titles_and_links': articles_titles_and_links, 'section': 'home'})
    else:
        try:
            form = WordcollectionForm(request.POST)
            newWordcollection = form.save(commit=False)
            newWordcollection.user = request.user
            urlToScrape = newWordcollection.url
            articles = scrapeUrl(urlToScrape)
            words = getMostFrequentWords(articles)

            newWordcollection.name = getCollectionName(urlToScrape)
            newWordcollection.save()
            createWordcollectionModels.delay(newWordcollection.id, words)

            return redirect('wordstock:wordcollection_detail', newWordcollection.id)

        except ValueError:
            return render(request, 'create_wordcollection.html', {'form': WordcollectionForm(), 'error': 'Incorrect input', 'articles_titles_and_links': articles_titles_and_links})


@login_required
def wordcollection_detail(request, wordcollection_id):
    wordcollection = get_object_or_404(Wordcollection, pk=wordcollection_id)
    words = Word.objects.filter(wordcollection=wordcollection)
    return render(request, 'wordcollection_detail.html', {'wordcollection': wordcollection, 'words': words, 'section': 'wordstock'})


@login_required
def wordcollection_list(request):
    wordcollections = Wordcollection.objects.filter(user=request.user)

    return render(request, 'wordcollection_list.html', {'wordcollections': wordcollections, 'section': 'wordstock'})


@login_required
def word_detail(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    synonyms = Synonym.objects.filter(word=word)
    return render(request, 'word_detail.html', {'word': word, 'synonyms': synonyms, 'section': 'wordstock'})


@login_required
def synonym_detail(request, synonym_id):
    synonym = get_object_or_404(Synonym, pk=synonym_id)
    examples = Example.objects.filter(synonym=synonym)
    return render(request, 'synonym_detail.html', {'synonym': synonym, 'examples': examples, 'section': 'wordstock'})


@login_required
def learn_words(request, wordcollection_id):

    wordcollection = get_object_or_404(Wordcollection, pk=wordcollection_id)
    words = Word.objects.filter(wordcollection=wordcollection)

    return render(request, 'learn.html', {'wordcollection': wordcollection, 'words': words, 'section': 'learn', 'learn_section': 'words'})


@login_required
def learn_synonyms(request, word_id):

    word = get_object_or_404(Word, pk=word_id)
    synonyms = Synonym.objects.filter(word=word)

    return render(request, 'learn.html', {'word': word, 'synonyms': synonyms, 'section': 'learn', 'learn_section': 'synonyms'})


@login_required
def learn_examples(request, synonym_id):

    synonym = get_object_or_404(Synonym, pk=synonym_id)
    examples = Example.objects.filter(synonym=synonym)

    return render(request, 'learn.html', {'synonym': synonym, 'examples': examples, 'section': 'learn', 'learn_section': 'examples'})
