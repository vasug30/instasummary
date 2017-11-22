from django.db import models


class Summarize(models.Model):
    url = models.CharField(max_length=1000)
    summarized = models.CharField(max_length=3000000)

    def __str__(self):
        return self.url
