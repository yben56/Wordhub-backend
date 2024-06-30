from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import Dictionary

@registry.register_document
class WordDocument(Document):
    class Index:
        name = 'words'
        settings = {'number_of_shards':1, 'number_of_replicas':0}

    class Django:
        model = Dictionary
        fields = ['id', 'word', 'heteronyms', 'pos', 'translation']