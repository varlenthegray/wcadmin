from django.db import models


class VersionLog(models.Model):
    version = models.CharField(max_length=15)
    details = models.TextField()
    when = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.version}'
