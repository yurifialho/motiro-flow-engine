from django.db import models


class Criteria(models.Model):
    level = models.IntegerField()
    sigla = models.CharField(max_length=3)
    criteria = models.CharField(max_length=100)


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    quiz = models.ForeignKey(Quiz,
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True)
    criteria = models.ForeignKey(Criteria,
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True)
    answer = models.CharField(max_length=2)
