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

#class Associate(models.Model):
#    word = models.CharField(max_length=255, null=False)
#    associate = models.TextField(null=True)

class Quiz(models.Model):
    wordid = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    word = models.CharField(max_length=255, null=False)
    quiz = models.TextField(null=False)

class Frequency(models.Model):
    word = models.CharField(max_length=255, null=False)
    frequency = models.IntegerField()

class SearchGuest(models.Model):
    search = models.TextField(null=False)
    word = models.CharField(max_length=255, null=True)
    exist = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

class SearchWords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search = models.TextField(null=False)
    word = models.CharField(max_length=255, null=True)
    exist = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

class SearchWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wordid = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    word = models.CharField(max_length=255, null=False)
    date = models.DateTimeField(auto_now_add=True)