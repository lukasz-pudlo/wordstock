from django.urls import path
from . import views

app_name = 'wordstock'

urlpatterns = [
    path('', views.wordcollection_list, name='wordcollection_list'),
    path('create', views.create_wordcollection, name='create'),
    path('search', views.search_definition, name='search'),
    path('wordcollection/<int:wordcollection_id>', views.wordcollection_detail,
         name='wordcollection_detail'),
    path('word/<int:word_id>',
         views.word_detail, name='word_detail'),
    path('synonym/<int:synonym_id>', views.synonym_detail, name='synonym_detail'),
    path('learn-words/<int:wordcollection_id>',
         views.learn_words, name='learn_words'),
    path('learn-synonyms/<int:word_id>',
         views.learn_synonyms, name='learn_synonyms'),
    path('learn-examples/<int:synonym_id>',
         views.learn_examples, name='learn_examples'),
]
