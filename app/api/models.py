from django.db import models

class Dictionary(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=255, null=False)
    phonetic = models.CharField(max_length=255, null=True)
    pos = models.CharField(max_length=30, null=True)
    translation = models.CharField(max_length=255, null=False)
    sentences = models.TextField(null=True)
    associate = models.TextField(null=True)
    
class Quiz(models.Model):
    wordid = models.ForeignKey(Dictionary, on_delete=models.CASCADE, db_column='wordid')
    word = models.CharField(max_length=255, null=False)
    quiz = models.TextField(null=False)

class Frequency(models.Model):
    word = models.CharField(max_length=255, null=False)
    frequency = models.IntegerField()