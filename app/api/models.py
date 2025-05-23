from django.db import models
from users.models import User

class Dictionary(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=255, null=False, blank=False)
    phonetic = models.CharField(max_length=255, null=True, blank=True)
    heteronyms = models.BooleanField(default=False)
    pos = models.CharField(max_length=30, null=True)
    translation = models.CharField(max_length=255, null=False, blank=False)
    sentences = models.TextField(null=True, blank=True)
    associate = models.TextField(null=True, blank=True)
    classification = models.TextField(null=True, blank=True)
    auther = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

class DictionaryVersion(models.Model):
    id = models.AutoField(primary_key=True)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    word = models.CharField(max_length=255, null=False, blank=False)
    phonetic = models.CharField(max_length=255, null=True, blank=True)
    heteronyms = models.BooleanField(default=False)
    pos = models.CharField(max_length=30, null=True)
    translation = models.CharField(max_length=255, null=False, blank=False)
    sentences = models.TextField(null=True, blank=True)
    associate = models.TextField(null=True, blank=True)
    classification = models.TextField(null=True, blank=True)
    auther = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'api_dictionary_version'

class Quiz(models.Model):
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    word = models.CharField(max_length=255, null=False)
    quiz = models.TextField(null=False)
    auther = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

class QuizVersion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    word = models.CharField(max_length=255, null=False)
    quiz = models.TextField(null=False)
    auther = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'api_quiz_version'

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    word = models.CharField(max_length=255, null=False)
    correct = models.IntegerField(default=0)
    trials = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'dictionary')

class Frequency(models.Model):
    word = models.CharField(max_length=255, null=False)
    frequency = models.IntegerField()

#Guest search word
class SearchWordGuest(models.Model):
    search = models.TextField(null=False)
    word = models.CharField(max_length=255, null=True)
    exist = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_search_guest'

#User search word
class SearchWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search = models.TextField(null=False)
    word = models.CharField(max_length=255, null=True)
    exist = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_search_word'

#User access word
class AccessWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    word = models.CharField(max_length=255, null=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_access_word'