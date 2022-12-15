from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from wordstock.models import Wordcollection, Word, Synonym, Example
from .serializers import WordcollectionSerializer, WordSerializer, SynonymSerializer, ExampleSerializer

from rest_framework.authentication import BasicAuthentication
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

# Create your views here.


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def apiOverview(request):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    api_urls = {
        'Wordcollection List': '/wordcollection-list',
        'Wordcollection Detail View': '/wordcollection-detail/<int:wordcollection_id>',
        'Wordcollection Create': '/wordcollection-create',
        'Wordcollection Update': '/wordcollection-update/<int:wordcollection_id>',
        'Wordcollection Delete': '/wordcollection-delete/<int:wordcollection_id>',
    }

    return Response(api_urls)

# Wordcollection Rest APIs.


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def restWordcollectionList(request):
    wordcollections = Wordcollection.objects.all()
    serializer = WordcollectionSerializer(wordcollections, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def restWordcollectionDetail(request, wordcollection_id):
    wordcollection = Wordcollection.objects.get(pk=wordcollection_id)
    serializer = WordcollectionSerializer(wordcollection, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def restWordcollectionCreate(request):
    serializer = WordcollectionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def restWordcollectionUpdate(request, wordcollection_id):
    wordcollection = Wordcollection.objects.get(pk=wordcollection_id)
    serializer = WordcollectionSerializer(
        instance=wordcollection, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((permissions.AllowAny,))
def restWordcollectionDelete(request, wordcollection_id):
    wordcollection = Wordcollection.objects.get(pk=wordcollection_id)
    wordcollection.delete()
    return Response('Wordcollection successfully deleted.')


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def restWordcollectionWords(request, wordcollection_id):
    wordcollection = Wordcollection.objects.get(pk=wordcollection_id)
    words = Word.objects.filter(wordcollection=wordcollection)
    serializer = WordSerializer(words, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def restWordDetail(request, wordcollection_id, word_id):
    word = Word.objects.get(pk=word_id)
    serializer = WordSerializer(word, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def restWordCreate(request):
    serializer = WordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def restWordUpdate(request, wordcollection_id, word_id):
    word = Word.objects.get(pk=word_id)
    serializer = WordSerializer(
        instance=word, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((permissions.AllowAny,))
def restWordDelete(request, word_id):
    word = Word.objects.get(pk=word_id)
    word.delete()
    return Response('Word successfully deleted.')


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def restWordSynonyms(request, wordcollection_id, word_id):
    word = Word.objects.get(pk=word_id)
    synonyms = Synonym.objects.filter(word=word)
    serializer = SynonymSerializer(synonyms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def restSynonymDetail(request, wordcollection_id, word_id, synonym_id):
    synonym = Synonym.objects.get(pk=synonym_id)
    serializer = SynonymSerializer(synonym, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def restSynonymCreate(request):
    serializer = SynonymSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def restSynonymUpdate(request, wordcollection_id, word_id, synonym_id):
    synonym = Synonym.objects.get(pk=synonym_id)
    serializer = SynonymSerializer(
        instance=synonym, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((permissions.AllowAny,))
def restSynonymDelete(request, synonym_id):
    synonym = Synonym.objects.get(pk=synonym_id)
    synonym.delete()
    return Response('Synonym successfully deleted.')


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def restSynonymExamples(request, wordcollection_id, word_id, synonym_id):
    synonym = Synonym.objects.get(pk=synonym_id)
    examples = Example.objects.filter(synonym=synonym)
    serializer = ExampleSerializer(examples, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def restExampleDetail(request, wordcollection_id, word_id, synonym_id, example_id):
    example = Example.objects.get(pk=example_id)
    serializer = ExampleSerializer(example, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def restExampleCreate(request):
    serializer = ExampleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def restExampleUpdate(request, wordcollection_id, word_id, synonym_id, example_id):
    example = Example.objects.get(pk=example_id)
    serializer = ExampleSerializer(
        instance=example, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((permissions.AllowAny,))
def restExampleDelete(request, example_id):
    example = Example.objects.get(pk=example_id)
    example.delete()
    return Response('Example successfully deleted.')
