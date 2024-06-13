from django.db import models
from users.models import User

class Dictionary(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=255, null=False)
    phonetic = models.CharField(max_length=255, null=True)
    heteronyms = models.BooleanField(default=False)
    pos = models.CharField(max_length=30, null=True)
    translation = models.CharField(max_length=255, null=False)
    sentences = models.TextField(null=True)
    associate = models.TextField(null=True)
    classification = models.TextField(null=True)

class Quiz(models.Model):
    wordid = models.ForeignKey(Dictionary, on_delete=models.CASCADE, db_column='wordid')
    word = models.CharField(max_length=255, null=False)
    quiz = models.TextField(null=False)

class Answer(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid')
    wordid = models.ForeignKey(Quiz, on_delete=models.CASCADE, db_column='wordid')
    word = models.CharField(max_length=255, null=False)
    correct = models.IntegerField(default=0)
    trials = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('userid', 'wordid')

class Frequency(models.Model):
    word = models.CharField(max_length=255, null=False)
    frequency = models.IntegerField()

class SearchGuest(models.Model):
    search = models.TextField(null=False)
    word = models.CharField(max_length=255, null=True)
    exist = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

class SearchWords(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid')
    search = models.TextField(null=False)
    word = models.CharField(max_length=255, null=True)
    exist = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

class SearchWord(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid'
    wordid = models.ForeignKey(Dictionary, on_delete=models.CASCADE, db_column='wordid')
    count = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('userid', 'wordid')