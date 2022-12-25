from django.db import models
from jsonfield import JSONField

# Create your models here.
class localSchemaModel(models.Model):
    schemaName = models.CharField(max_length=30)
    serverIP = models.CharField(max_length=30)
    serverPort = models.CharField(max_length=30)
    serverUser = models.CharField(max_length=30)
    serverPass = models.CharField(max_length=30)
    dbName = models.CharField(max_length=30)
    schema = JSONField()

class globalSchemaModel(models.Model):
    schemaName = models.CharField(max_length=30)
    schema = JSONField()
    localSchemas = JSONField()



