from django.urls import path
from . import views as restApiViews

app_name = 'rest_api'

urlpatterns = [
    path('', restApiViews.apiOverview, name='api-overview'),

    # Wordcollection urls patterns.
    path('wordcollection-list', restApiViews.restWordcollectionList,
         name='rest-wordcollection-list'),
    path('wordcollection-detail/<int:wordcollection_id>', restApiViews.restWordcollectionDetail,
         name='rest-wordcollection-detail'),
    path('wordcollection-create',
         restApiViews.restWordcollectionCreate, name='rest-wordcollection-create'),
    path('wordcollection-update/<int:wordcollection_id>', restApiViews.restWordcollectionUpdate,
         name='rest-wordcollection-update'),
    path('wordcollection-delete/<int:wordcollection_id>', restApiViews.restWordcollectionDelete,
         name='rest-wordcollection-delete'),

    # Word url patterns.

    path('wordcollection/<int:wordcollection_id>/words',
         restApiViews.restWordcollectionWords, name="rest-wordcollection-words"),
    path('wordcollection/<int:wordcollection_id>/word-detail/<int:word_id>',
         restApiViews.restWordDetail, name="rest-word-detail"),
    path('word-create',
         restApiViews.restWordCreate, name='rest-word-create'),
    path('wordcollection/<int:wordcollection_id>/word-update/<int:word_id>', restApiViews.restWordUpdate,
         name='rest-word-update'),
    path('word-delete/<int:word_id>', restApiViews.restWordDelete,
         name='rest-word-delete'),

    # Synonym url patterns.

    path('wordcollection/<int:wordcollection_id>/word/<int:word_id>/synonyms',
         restApiViews.restWordSynonyms, name="rest-word-synonyms"),
    path('wordcollection/<int:wordcollection_id>/word/<int:word_id>/synonym-detail/<int:synonym_id>',
         restApiViews.restSynonymDetail, name="rest-synonym-detail"),
    path('synonym-create',
         restApiViews.restSynonymCreate, name='rest-synonym-create'),
    path('wordcollection/<int:wordcollection_id>/word/<int:word_id>/synonym-update/<int:synonym_id>', restApiViews.restSynonymUpdate,
         name='rest-synonym-update'),
    path('synonym-delete/<int:synonym_id>', restApiViews.restSynonymDelete,
         name='rest-synonym-delete'),

    # Example url patterns.

    path('wordcollection/<int:wordcollection_id>/word/<int:word_id>/synonym/<int:synonym_id>/examples',
         restApiViews.restSynonymExamples, name="rest-synonym-examples"),
    path('wordcollection/<int:wordcollection_id>/word/<int:word_id>/synonym/<int:synonym_id>/example-detail/<int:example_id>',
         restApiViews.restExampleDetail, name="rest-example-detail"),
    path('example-create',
         restApiViews.restExampleCreate, name='rest-example-create'),
    path('wordcollection/<int:wordcollection_id>/word/<int:word_id>/synonym/<int:synonym_id>/example-update/<int:example_id>', restApiViews.restExampleUpdate,
         name='rest-example-update'),
    path('example-delete/<int:example_id>', restApiViews.restExampleDelete,
         name='rest-example-delete'),
]
