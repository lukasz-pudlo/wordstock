from django.contrib import admin

from .models import Wordcollection, Word, Synonym, Example


@admin.register(Wordcollection)
class WordcollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url', 'user', 'created']


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['id', 'source_word', 'target_word', 'wordcollection']


@admin.register(Synonym)
class SynonymAdmin(admin.ModelAdmin):
    list_display = ['id', 'source_synonym', 'target_synonym', 'word']


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ['id', 'source_example', 'target_example', 'synonym']
