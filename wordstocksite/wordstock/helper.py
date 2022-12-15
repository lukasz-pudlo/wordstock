from django.shortcuts import render

import requests
from bs4 import BeautifulSoup
import re

from .models import Wordcollection, Word, Synonym, Example


def scrapeUrl(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    headings = soup.find_all(
        "div", {"class": "article-details-text u-space-bottom-xl"})
    headings = headings[0:20]

    articles = []

    for heading in headings:
        articles.append(heading.text.strip())
    return articles


def getCollectionName(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    headline_title = soup.find("span", {"class": "headline-title"})
    wordcollection_name = headline_title.text.strip()

    return wordcollection_name


def getMostFrequentWords(articleList):
    oneList = []
    for entry in articleList:
        words = entry.split(" ")
        for word in words:
            oneList.append(word)
    newList = []
    for word in oneList:
        wordWithoutPunctuationMarks = re.sub(r'[^\w\s]', '', word)
        newList.append(wordWithoutPunctuationMarks)
    finalList = orderWordsByFrequency(newList)

    return finalList


def orderWordsByFrequency(unorderedWords):
    # Create a list without duplicates based on the input list
    setOfWords = list(set(unorderedWords))
    wordsListWithFrequency = []
    # Check if the word from the list without duplicates exists in the lists with duplicates
    for word in setOfWords:
        wordsListWithFrequency.append({'word': word, 'frequency': 0})
    idx = 0
    for uniqueWord in setOfWords:
        for word in unorderedWords:
            # If the word from the list without duplicates exists in the list with dupicates, then update the frequency in a dictionary
            if uniqueWord == word:
                wordsListWithFrequency[idx]['frequency'] += 1
        idx += 1

    def frequencyValues(x):
        return x['frequency']
    wordsListWithFrequency.sort(reverse=True, key=frequencyValues)

    finalList = []
    for i in range(len(wordsListWithFrequency)):
        finalList.append(wordsListWithFrequency[i]['word'])
    finalListAlpha = [i for i in finalList if not i.isdigit()]
    return finalListAlpha


def search_definition(request):
    searchTerm = request.GET.get('searchTerm')
    if searchTerm:
        response = requests.get(
            'https://german-english-dictionary-api.uc.r.appspot.com/translate?term=%s&limit=1' % searchTerm)
        data = response.json()
        english_translation = data['results'][0]['english']['term']
        return render(request, 'search_definition.html', {'english_translation': english_translation})
    else:
        return render(request, 'search_definition.html')


def search_english_definition(word):
    response = requests.get(
        'https://german-english-dictionary-api.uc.r.appspot.com/translate?term=%s&limit=10' % word)
    data = response.json()
    if data['count'] != 0:
        english_translation = data['results'][0]['english']['term']
    else:
        english_translation = 'no translation found'
    return english_translation


class WordData(object):
    def __init__(self, word):
        response = requests.get(
            'https://german-english-dictionary-api.uc.r.appspot.com/translate?term=%s&limit=5' % word)
        data = response.json()
        self.data = data

        if data['count'] != 0:
            self.english_translation = data['results'][0]['english']['term']
        else:
            self.english_translation = 'no translation found'


def getWordData(word):
    return WordData(word)


def create_list_of_articles():
    r = requests.get('https://www.deutschlandfunk.de/')
    soup = BeautifulSoup(r.content, 'html.parser')

    titles = []
    links = []
    titles_and_links = {}
    articles = soup.find_all("article")
    for article in articles:
        url = article.find('a', href=True)
        title = article.find('a', title=True)
        if url and title:
            link = url['href']
            links.append(link)
            headline = title['title']
            titles.append(headline)
            titles_and_links[headline] = link

    return titles_and_links
