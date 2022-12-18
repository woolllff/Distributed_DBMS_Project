from django.contrib import admin
from .models import localSchemaModel , globalSchemaModel
# Register your models here.

admin.site.register(localSchemaModel)
admin.site.register(globalSchemaModel)

