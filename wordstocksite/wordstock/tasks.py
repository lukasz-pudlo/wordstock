from celery import shared_task

from .helper import *


@shared_task
def createWordcollectionModels(newWordcollection_id, words):
    newWordcollection = Wordcollection.objects.get(id=newWordcollection_id)
    for word in words:
        word_data = getWordData(word)
        newWord = Word(wordcollection=newWordcollection,
                       source_word=word, target_word=word_data.english_translation)
        newWord.save()
        for synonym in word_data.data['results']:
            newSynonym = Synonym(
                word=newWord, source_synonym=synonym['german']['term'], target_synonym=synonym['english']['term'])
            newSynonym.save()
            exampleIdx = 0
            if synonym['german']['examples'] is not None:
                for example in synonym['german']['examples']:
                    newExample = Example(
                        synonym=newSynonym, source_example=example, target_example=synonym['english']['examples'][exampleIdx])
                    exampleIdx += 1
                    newExample.save()
