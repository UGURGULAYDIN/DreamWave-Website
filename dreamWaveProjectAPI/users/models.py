from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)  # ID
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username
